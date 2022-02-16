# pynodb

## Introduction
This is a really simple package for easy use of the Notion database.
I developed this package to automate the repetitve in-house tasks using Notion.
We use Notion as frontend and also backend(database table).
When using pure Notion database API, it gives us different structure for each column's data type.
Therefore we have to parse json response for each data type and it is very cumbersome.
With this package, you can get simple and important data which are column name and its value.

## Install
```
pip install pynodb
```

## Requirement
Please follow this guides first to use this package.
https://developers.notion.com/docs#:~:text=Postman%20workspace-,Getting%20started,-Learn%20how%20to

## Usage
If you are ready with Notion configuration, you can start from here.
There are two modules. 

```
from pynodb.notion_database_client import NotionDatabaseClient
from pynodb.database_parser import DatabaseParser
```

### Quick Start
Usually, I create my Notion database in Notion first and get its ID to use API.  
You can get URL and ID of database when you click `Open as page` button from top right of database.
```
https://www.notion.so/myworkspace/a8aec43384f447ed84390e8e42c2e089?v=...  
----------------------------------|--------- Database ID --------|------
```

Let's use this package quickly. This is sample Notion database
![스크린샷 2021-12-10 오후 2 03 01](https://user-images.githubusercontent.com/64149539/145526315-ade3df8a-def3-4376-bc5f-a9f2d24e3cc9.png)

```
secret_key = "<your-secret-key>"
database_id = "<your-database-id>"

notion_database_client = NotionDatabaseClient(secret_key=secret_key, database_id=database_id)
database = notion_database_client.fetch_database()
print(database)

```
You can get original result from Notion API when printing `database`. This result is quite complex to read and parse
![스크린샷 2021-12-10 오후 2 07 03](https://user-images.githubusercontent.com/64149539/145526428-15a50949-5ae6-489e-82fb-1cf2b4172caa.png)

Below is the easy way of parsing your database result.  

```
my_database = DatabaseParser(database)
parsed_database = my_database.parsed_database
print(parsed_database)
```
![스크린샷 2021-12-10 오후 2 10 04](https://user-images.githubusercontent.com/64149539/145526464-d5fd14d4-fa66-4761-b1e7-eda79be5b3f2.png)
Each dictionary in list has 'page_id' and all column names as keys.

You can access each data easily like this.
```
for page in parsed_database:
    page_id = page['page_id']
    date_value = page['DATE']['value']
    select_value = page['SELECT']['value']
    ...
```

### Details

**NotionDatabaseClient**  
This module is for using Notion API. You can fetch, update Notion database and create, update Notion pages using this module.  

| Method                 | Parameter                   | Description                                                                 |
|------------------------|-----------------------------|-----------------------------------------------------------------------------|
| fetch_database()       | `limit(=None)`, `filter(=None)` | Fetch all data from database. You can set limit(number of pages you want) and filter(query condition, please see this [link](https://developers.notion.com/reference/post-database-query)) for this method. |
| update_database()      | `data`(json type body)| Update database. Please see this [link](https://developers.notion.com/reference/update-a-database) for `data` parameter. |
| create_page()          | `data`(json type body)| Create page. Please see this [link](https://developers.notion.com/reference/post-page) for `data` parameter. |
| update_page()          | `page_id`, `data`(json type body)| Update page. Please see this [link](https://developers.notion.com/reference/patch-page) for `data` parameter. |
| get_page()             | `page_id` | Retrieve a page. Please see this [link](https://developers.notion.com/reference/retrieve-a-page). |
| get_block_children()   | `block_id` | Retrieve a block. Please see this [link](https://developers.notion.com/reference/get-block-children). |
| append_block_children()| `block_id`, `data`(json type body)| Append block children. Please see this [link](https://developers.notion.com/reference/patch-block-children) for `data` parameter. |

**DatabaseParser**  
There are only private methods in this class. You can only access varaibles.  

| Variable        | Description                        |
|-----------------|------------------------------------|
| raw_database    | Raw json response from Notion API  |
| parsed_database | Parsed json which is for easy use. |
| property_names  | All property names from database.  |


### Supported Data Types of DatabaseParser 
*This supported data types are only related to DatabaseParser. 
You can get any data type using **NotionDatabaseClient** since it gives you raw json response of Notion API.  

1. TITLE
2. RICH_TEXT
3. NUMBER
4. SELECT
5. MULTI_SELECT
6. PEOPLE
7. DATE
8. URL
9. CHECKBOX
10. RELATION
11. ROLLUP (only array type)
12. FORMULA

