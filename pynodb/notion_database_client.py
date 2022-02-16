import requests, json

class NotionDatabaseClient:
    def __init__(self, secret_key, database_id, version="2021-08-16"):
        self.headers = {"Authorization": "Bearer " + secret_key, "Notion-Version": version, "Content-Type": "application/json; charset=utf-8"}
        self.database_query_url = "https://api.notion.com/v1/databases/" + database_id + "/query"
        self.database_patch_url = "https://api.notion.com/v1/databases/" + database_id
        
    def fetch_database(self, limit=None, filter=None):
        has_more = True
        cursor_id = ""
        results = []
        data = {}
        if filter is not None:
            data["filter"] = filter
        
        while has_more:
            if cursor_id != "": 
                data["start_cursor"] = cursor_id
            response = requests.post(self.database_query_url, headers=self.headers, data=json.dumps(data))
            results += response.json()["results"]
            if limit != None and len(results) >= limit:
                break
            if response.json()["has_more"] == True:
                has_more = True
                cursor_id = response.json()["next_cursor"]
            else:
                has_more = False

        if limit != None:
            results = results[:limit]
        
        return results
    
    def update_database(self, data):
        response = requests.patch(self.database_patch_url, data=json.dumps(data), headers=self.headers)
        
        return response

    def update_page(self, page_id, data):
        notion_page_url = 'https://api.notion.com/v1/pages/' + page_id
        response = requests.patch(notion_page_url, data=json.dumps(data), headers=self.headers)

        return response

    def create_page(self, data):
        url = 'https://api.notion.com/v1/pages'
        response = requests.post(url, data=json.dumps(data), headers=self.headers)

        return response
    
    def get_block_children(self, block_id):
        notion_block_url = 'https://api.notion.com/v1/blocks/' + block_id + '/children'
        response = requests.get(url=notion_block_url, headers=self.headers)

        return response
    
    def get_page(self, page_id):
        notion_page_url = 'https://api.notion.com/v1/pages/' + page_id
        response = requests.get(notion_page_url, headers=self.headers)

        return response
    
    def append_block_children(self, block_id, data):
        block_url = 'https://api.notion.com/v1/blocks/' + block_id + '/children'
        response = requests.patch(url=block_url, data=json.dumps(data), headers=self.headers)
        
        return response