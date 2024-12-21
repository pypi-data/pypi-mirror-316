import asyncio
from dotenv import load_dotenv

from src.salesforce.server import SalesforceClient

async def main():
    # Load environment variables
    load_dotenv()

    # Configure with Salesforce credentials from environment variables
    sf_client = SalesforceClient()
    if not sf_client.connect():
        print("Failed to initialize Salesforce connection")
        return

    # Call get_objects_schema directly
    schema = await sf_client.get_object_fields("Contact")
    print(f"Schema for all objects (JSON):\n{schema}")

if __name__ == "__main__":
    asyncio.run(main())
