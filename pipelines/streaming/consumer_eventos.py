"""Consumer Kafka → Bronze (opcional).

Sem broker, use producer_eventos.py (file sink). Este consumer espelha a aula 02_Kafka.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from pipelines.config import BRONZE, KAFKA, LOGS  # noqa: E402
from pipelines.streaming.producer_eventos import flatten_event  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
log = logging.getLogger("stream-consumer")


def consume(max_messages: int = 20, timeout_ms: int = 5000) -> int:
    try:
        from kafka import KafkaConsumer  # type: ignore
    except ImportError as exc:
        raise SystemExit("pip install kafka-python") from exc

    consumer = KafkaConsumer(
        KAFKA["topic_indicadores"],
        bootstrap_servers=KAFKA["bootstrap"],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda b: json.loads(b.decode("utf-8")),
        consumer_timeout_ms=timeout_ms,
    )

    rows = []
    for i, msg in enumerate(consumer):
        rows.append(flatten_event(msg.value))
        if i + 1 >= max_messages:
            break
    consumer.close()

    if not rows:
        log.warning("Nenhuma mensagem consumida")
        return 0

    df = pd.DataFrame(rows)
    ts = datetime.now(timezone.utc)
    dest = BRONZE / "events_indicador" / f"dt={ts.strftime('%Y-%m-%d')}"
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / f"part-kafka-{ts.strftime('%H%M%S')}.parquet"
    df.to_parquet(path, index=False)
    log.info("Gravados %s eventos em %s", len(df), path)
    return len(df)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", type=int, default=20)
    args = parser.parse_args()
    LOGS.mkdir(parents=True, exist_ok=True)
    n = consume(max_messages=args.max)
    (LOGS / "streaming_consumer_report.json").write_text(
        json.dumps(
            {"consumed": n, "ts": datetime.now(timezone.utc).isoformat()},
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
