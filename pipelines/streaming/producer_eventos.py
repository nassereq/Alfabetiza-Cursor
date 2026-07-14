"""Producer de eventos de atualização do indicador (braço streaming).

Padrão: ETL Pipelines / 02_Kafka + eventos JSON estilo NoSQL (aula Big Data).
Sem Kafka local, grava em data/bronze/events_indicador (simulação file-based).
Com --kafka, publica no tópico configurado.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from pipelines.config import BRONZE, KAFKA, LOGS, RAW, SAMPLE  # noqa: E402
from pipelines.batch.generate_sample_data import build_samples  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
log = logging.getLogger("stream-producer")


def _load_indicador(fonte: str = "sample") -> pd.DataFrame:
    if fonte == "raw":
        path = RAW / "indicador_municipio.csv"
        if not path.exists():
            raise FileNotFoundError(
                f"{path} ausente. Rode: python -m pipelines.batch.fetch_basedosdados"
            )
        return pd.read_csv(path, dtype=str)
    if not (SAMPLE / "indicador_municipio.csv").exists():
        build_samples()
    return pd.read_csv(SAMPLE / "indicador_municipio.csv", dtype=str)


def build_events(n: int = 10, fonte: str = "sample") -> list[dict]:
    df = _load_indicador(fonte=fonte)
    # pega os últimos municípios do ano mais recente e simula micro-atualizações
    latest_ano = df["ano"].astype(int).max()
    base = df[df["ano"].astype(int) == latest_ano].head(n)
    events = []
    ts = datetime.now(timezone.utc).isoformat()
    for i, row in enumerate(base.to_dict(orient="records")):
        pct = float(row["pct_alfabetizados"])
        delta = ((i % 5) - 2) * 0.35
        new_pct = max(5.0, min(99.0, round(pct + delta, 2)))
        n_av = row.get("n_avaliados")
        if n_av is None or str(n_av).strip() in ("", "nan", "None", "<NA>"):
            n_av = "0"
        events.append(
            {
                "eventID": f"evt-{int(time.time())}-{i}",
                "eventName": "MODIFY",
                "eventSource": "alfabetiza.stream",
                "eventTime": ts,
                "NewImage": {
                    "ano": {"N": str(row["ano"])},
                    "id_municipio": {"S": str(row["id_municipio"])},
                    "id_uf": {"S": str(row["id_uf"])},
                    "sigla_uf": {"S": str(row["sigla_uf"])},
                    "nome_municipio": {"S": str(row["nome_municipio"])},
                    "pct_alfabetizados": {"N": str(new_pct)},
                    "ponto_corte": {"N": str(row.get("ponto_corte", 743))},
                    "n_avaliados": {"N": str(n_av)},
                },
            }
        )
    return events


def flatten_event(evt: dict) -> dict:
    img = evt["NewImage"]
    return {
        "ano": img["ano"]["N"],
        "id_municipio": img["id_municipio"]["S"],
        "id_uf": img["id_uf"]["S"],
        "sigla_uf": img["sigla_uf"]["S"],
        "nome_municipio": img["nome_municipio"]["S"],
        "pct_alfabetizados": img["pct_alfabetizados"]["N"],
        "ponto_corte": img["ponto_corte"]["N"],
        "n_avaliados": img["n_avaliados"]["N"],
        "_data_ingestao": evt["eventTime"],
        "_fonte": "streaming:kafka_sim",
        "_entidade": "indicador_municipio",
        "_modo": "streaming",
        "_event_id": evt["eventID"],
    }


def write_file_sink(events: list[dict]) -> Path:
    rows = [flatten_event(e) for e in events]
    df = pd.DataFrame(rows)
    ts = datetime.now(timezone.utc)
    dest = BRONZE / "events_indicador" / f"dt={ts.strftime('%Y-%m-%d')}"
    dest.mkdir(parents=True, exist_ok=True)
    # append-friendly: novo part por execução
    part = dest / f"part-{ts.strftime('%H%M%S')}.parquet"
    df.to_parquet(part, index=False)
    # também JSONL bruto (estilo bronze raw)
    raw = dest / f"events-{ts.strftime('%H%M%S')}.jsonl"
    with raw.open("w", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    return part


def publish_kafka(events: list[dict]) -> None:
    try:
        from kafka import KafkaProducer  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "kafka-python não instalado. Use sem --kafka ou: pip install kafka-python"
        ) from exc

    producer = KafkaProducer(
        bootstrap_servers=KAFKA["bootstrap"],
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8"),
    )
    topic = KAFKA["topic_indicadores"]
    for e in events:
        producer.send(topic, e)
    producer.flush()
    log.info("Publicados %s eventos em %s", len(events), topic)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--fonte", default="sample", choices=["sample", "raw"])
    parser.add_argument("--kafka", action="store_true")
    args = parser.parse_args()
    LOGS.mkdir(parents=True, exist_ok=True)

    events = build_events(n=args.n, fonte=args.fonte)
    path = write_file_sink(events)
    log.info("File sink Bronze: %s (%s eventos)", path, len(events))
    if args.kafka:
        publish_kafka(events)

    report = {
        "component": "streaming_producer",
        "events": len(events),
        "sink": str(path),
        "kafka": bool(args.kafka),
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    (LOGS / "streaming_producer_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
