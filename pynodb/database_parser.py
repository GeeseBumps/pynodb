from datetime import datetime


class DatabaseParser:
    def __init__(self, database):
        self.raw_database = database
        self.database_len = len(database)
        self.__get_property_names()
        self.parsing_value_by_type_dict = {
            "url": lambda x: self.__parse_url_value(x),
            "date": lambda x: self.__parse_date_value(x),
            "multi_select": lambda x: self.__parse_multi_select_value(x),
            "number": lambda x: self.__parse_number_value(x),
            "select": lambda x: self.__parse_select_value(x),
            "rich_text": lambda x: self.__parse_rich_text_value(x),
            "checkbox": lambda x: self.__parse_checkbox_value(x),
            "title": lambda x: self.__parse_title_value(x),
            "people": lambda x: self.__parse_people_value(x),
            "relation": lambda x: self.__parse_relation_value(x),
            "rollup": lambda x: self.__parse_rollup_value(x),
            "formula": lambda x: self.__parse_formula_value(x),
            "created_time": lambda x: self.__parse_timestamp_value(x),
            "last_edited_time": lambda x: self.__parse_timestamp_value(x),
            "created_by": lambda x: self.__parse_people_value(x),
            "last_edited_by": lambda x: self.__parse_people_value(x)
        }
        self.parsed_database = self.__parse_database(database)

    def __get_property_names(self):
        if self.database_len != 0:
            self.property_names = [property_key for property_key in self.raw_database[0]["properties"].keys()]

    def __parse_url_value(self, value_data):
        if value_data != None:
            return value_data
        return None

    def __parse_people_value(self, value_data):
        if isinstance(value_data, dict):
            return value_data["name"]
        elif isinstance(value_data, list):
            if len(value_data) != 0:
                values = []
                for people in value_data:
                    values.append(people["name"])
                return values
            return None
        else:
            raise ValueError("Invalid people value. Must be a list or a dict.")

    def __parse_date_value(self, value_data):
        if value_data != None:
            return value_data["start"]
        return None

    def __parse_multi_select_value(self, value_data):
        if len(value_data) != 0:
            values = [value["name"] for value in value_data]
            return values
        return None

    def __parse_number_value(self, value_data):
        if value_data != None:
            return value_data   
        return None

    def __parse_select_value(self, value_data):
        if value_data != None:
            return value_data["name"]
        return None

    def __parse_rich_text_value(self, value_data):
        if len(value_data) != 0:
            text = ""
            for value in value_data:
                text += value["plain_text"]
            return text
        return None

    def __parse_checkbox_value(self, value_data):
        return value_data

    def __parse_title_value(self, value_data):
        if len(value_data) != 0:
            text = ""
            for value in value_data:
                if value["type"] == "text":
                    text += value["plain_text"]
            return text
        return None
    
    def __parse_relation_value(self, value_data):
        if len(value_data) != 0:
            values = [relation["id"] for relation in value_data]
            return values
        return None
    
    def __parse_rollup_value(self, value_data):
        if value_data:
            if value_data["type"] == "array":
                type = value_data["array"][0]["type"]
                return value_data["array"][0][type]
        return None
    
    def __parse_formula_value(self, value_data):
        if value_data:
            type = value_data["type"]
            return value_data[type]
        return None

    def __parse_timestamp_value(self, value_data):
        return datetime.strptime(value_data, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    def __parse_database(self, database):
        parsed_database = []
        for page in database:
            parsed_page = {
                "page_id": page["id"],
                "page_url": page["url"]
            }
            for property_name in page["properties"]:
                property_data = page["properties"][property_name]
                type = property_data["type"]
                value_data = property_data[type]
                parsed_page[property_name] = {
                    "name": property_name,
                    "type": type,
                    "value": self.__get_property_value(type, value_data)
                }

            parsed_database.append(parsed_page)
        return parsed_database

    def __get_property_value(self, type, value_data):
        return self.parsing_value_by_type_dict[type](value_data)
