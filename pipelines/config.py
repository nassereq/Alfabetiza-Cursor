"""Configuração local da pipeline medalhão (Alfabetiza-Cursor)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SAMPLE = DATA / "sample"
RAW = DATA / "raw"
BRONZE = DATA / "bronze"
SILVER = DATA / "silver"
GOLD = DATA / "gold"
LOGS = ROOT / "logs"

# Ponto de corte Saeb — Pesquisa Alfabetiza Brasil (2023)
PONTO_CORTE_ALFABETIZACAO = 743

# Entidades do enunciado
ENTIDADES = [
    "uf",
    "municipio",
    "meta_brasil",
    "meta_uf",
    "meta_municipio",
    "alunos",
    "indicador_municipio",
]

# AWS (espelho da aula Glue SOR/SOT/SPEC) — preencher em deploy
AWS = {
    "bucket_sor": "alfabetiza-data-sor",      # Bronze
    "bucket_sot": "alfabetiza-data-sot",      # Silver
    "bucket_spec": "alfabetiza-data-spec",    # Gold
    "region": "us-east-1",
}

# Kafka
KAFKA = {
    "bootstrap": "localhost:9092",
    "topic_indicadores": "alfabetiza.indicador.updates",
}
