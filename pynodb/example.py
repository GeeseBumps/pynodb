from pynodb.notion_database_client import NotionDatabaseClient
from pynodb.database_parser import DatabaseParser


secret_key = "<your-secret-key>"
database_id = "<your-database-id>"


notion_database_client = NotionDatabaseClient(secret_key=secret_key, database_id=database_id)
database = notion_database_client.fetch_database()

my_database = DatabaseParser(database)
parsed_database = my_database.parsed_database
print(parsed_database)