class DatabaseParser:
    def __init__(self, database):
        self.raw_database = database
        self.database_len = len(database)
        self.property_names = []
        self._get_property_names()
        self.parsing_value_by_type_dict = {
            "url": lambda x: self._parse_url_value(x),
            "date": lambda x: self._parse_date_value(x),
            "multi_select": lambda x: self._parse_multi_select_value(x),
            "number": lambda x: self._parse_number_value(x),
            "select": lambda x: self._parse_select_value(x),
            "rich_text": lambda x: self._parse_rich_text_value(x),
            "checkbox": lambda x: self._parse_checkbox_value(x),
            "title": lambda x: self._parse_title_value(x),
            "people": lambda x: self._parse_people_value(x),
            "relation": lambda x: self._parse_relation_value(x),
            "rollup": lambda x: self._parse_rollup_value(x),
            "formula": lambda x: self._parse_formula_value(x),
        }
        self.parsed_database = self._parse_database(database)

    def _get_property_names(self):
        if self.database_len != 0:
            for property_key in self.raw_database[0]["properties"].keys():
                self.property_names.append(property_key)

    def _parse_url_value(self, value_data):
        if value_data != None:
            return value_data
        return None

    def _parse_people_value(self, value_data):
        if len(value_data) != 0:
            values = []
            for people in value_data:
                values.append(people["name"])
            return values
        return None

    def _parse_date_value(self, value_data):
        if value_data != None:
            return value_data["start"]
        return None

    def _parse_multi_select_value(self, value_data):
        if len(value_data) != 0:
            values = []
            for value in value_data:
                values.append(value["name"])
            return values
        return None

    def _parse_number_value(self, value_data):
        if value_data != None:
            return value_data   
        return None

    def _parse_select_value(self, value_data):
        if value_data != None:
            return value_data["name"]
        return None

    def _parse_rich_text_value(self, value_data):
        if len(value_data) != 0:
            text = ""
            for value in value_data:
                text += value["plain_text"]
            return text
        return None

    def _parse_checkbox_value(self, value_data):
        return value_data

    def _parse_title_value(self, value_data):
        if len(value_data) != 0:
            text = ""
            for value in value_data:
                if value["type"] == "text":
                    text += value["plain_text"]
            return text
        return None
    
    def _parse_relation_value(self, value_data):
        if len(value_data) != 0:
            values = []
            for relation in value_data:
                values.append(relation["id"])
            return values
        return None
    
    def _parse_rollup_value(self, value_data):
        if value_data:
            if value_data["type"] == "array":
                type = value_data["array"][0]["type"]
                return value_data["array"][0][type]
        return None
    
    def _parse_formula_value(self, value_data):
        if value_data:
            type = value_data["type"]
            return value_data[type]
        return None
    
    def _parse_database(self, database):
        parsed_database = []
        for page in database:
            _temp_page = {}
            _temp_page["page_id"] = page["id"]
            _temp_page["page_url"] = page["url"]
            for property_name in page["properties"]:
                property_data = {}
                property_metadata = page["properties"][property_name]
                type = property_metadata["type"]
                value_data = property_metadata[type]
                property_data["name"] = property_name
                property_data["type"] = type
                property_data["value"] = self._get_property_value(type, value_data)
                _temp_page[property_name] = property_data
            parsed_database.append(_temp_page)
        return parsed_database

    def _get_property_value(self, type, value_data):
        return self.parsing_value_by_type_dict[type](value_data)
