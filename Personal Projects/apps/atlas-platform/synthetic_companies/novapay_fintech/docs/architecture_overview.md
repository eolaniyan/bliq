# NovaPay Architecture Overview

Industry: fintech

Core services:
- api_gateway
- auth_service
- merchant_service
- checkout_service
- payment_service
- fraud_service
- ledger_service
- settlement_service

Known declared relationships:
- api_gateway -> auth_service
- api_gateway -> checkout_service
- api_gateway -> merchant_service
- checkout_service -> payment_service
- checkout_service -> notification_service
- payment_service -> ledger_service
- ledger_service -> settlement_service
- settlement_service -> reporting_service
- merchant_service -> reporting_service
- analytics_service -> reporting_service

Note: runtime architecture may contain additional observed relationships.