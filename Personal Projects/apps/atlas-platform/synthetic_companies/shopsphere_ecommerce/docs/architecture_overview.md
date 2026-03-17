# ShopSphere Architecture Overview

Industry: ecommerce

Core services:
- api_gateway
- auth_service
- product_catalog_service
- inventory_service
- cart_service
- checkout_service
- payment_service
- order_service

Known declared relationships:
- api_gateway -> auth_service
- api_gateway -> product_catalog_service
- api_gateway -> cart_service
- api_gateway -> checkout_service
- product_catalog_service -> inventory_service
- cart_service -> product_catalog_service
- cart_service -> inventory_service
- checkout_service -> cart_service
- checkout_service -> payment_service
- payment_service -> order_service

Note: runtime architecture may contain additional observed relationships.