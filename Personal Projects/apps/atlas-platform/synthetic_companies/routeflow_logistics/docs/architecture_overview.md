# RouteFlow Architecture Overview

Industry: logistics

Core services:
- api_gateway
- auth_service
- shipment_service
- route_planning_service
- warehouse_service
- tracking_service
- fleet_management_service
- billing_service

Known declared relationships:
- api_gateway -> auth_service
- api_gateway -> shipment_service
- api_gateway -> tracking_service
- shipment_service -> route_planning_service
- shipment_service -> tracking_service
- route_planning_service -> fleet_management_service
- warehouse_service -> tracking_service
- tracking_service -> notification_service
- tracking_service -> analytics_service
- shipment_service -> billing_service

Note: runtime architecture may contain additional observed relationships.