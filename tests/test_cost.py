from aws_cost import get_cost_by_service

services = get_cost_by_service()

for service in services:

    print(service)