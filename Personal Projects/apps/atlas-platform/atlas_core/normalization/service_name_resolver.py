import re


ALIASES = {
    "fraud-service": "fraud_service",
    "fraudservice": "fraud_service",
    "fraudengine": "fraud_service",
    "payment-service": "payment_service",
    "checkout-service": "checkout_service",
    "ledger-service": "ledger_service",
    "settlement-service": "settlement_service",
}


def normalize_service_name(name: str) -> str:
    cleaned = name.strip().lower()
    cleaned = cleaned.replace("-", "_")
    cleaned = re.sub(r"\s+", "_", cleaned)
    return ALIASES.get(cleaned, cleaned)