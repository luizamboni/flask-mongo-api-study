import sys
print("DEBUG sys.path:", sys.path)
import json
import asyncio
import argparse
from src.initializers.configurator import Configurator

async def main(env: str):
    config = await Configurator().configure()
    if env == "sandbox":
        ticket_service = config.sandbox.ticket_service
    else:
        ticket_service = config.regular.ticket_service

    tickets = await ticket_service.find_many()
    for ticket in tickets:
        print(json.dumps(ticket.model_dump()))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ticket batch job")
    parser.add_argument("--env", choices=["sandbox", "regular"], default="regular", help="Select environment")
    args = parser.parse_args()
    asyncio.run(main(args.env))
