import json
import os

class SearchElement:
    def __init__(self):
        self.element_data = self.load_json("elements.json")
        self.property_intents = self.load_json("intents.json")
        self.elements = [element['name'] for element in self.element_data['elements']]
        self.property_patterns = {element['tag']: element['patterns'] for element in self.property_intents['intents']}
        self.question_strings = ["what is", "tell me", "do you know", "arre you aware of"]

    def load_json(self, filename):
        file_path = os.path.join("D:\Files\Python\AI\CURRENT_VER\dataset\elements", filename)
        with open(file_path, "r") as file:
            return json.load(file)

    def find_element(self, user_message):
        for element in self.elements:
            if element.lower() in user_message.lower():
                return element

    def find_property_tag(self, user_message):
        for tag, patterns in self.property_patterns.items():
            for prop in patterns:
                if prop.lower() in user_message.lower():
                    return tag

    def get_element_info(self, data, parent_field, field, value):
        for element in data[parent_field]:
            if element[field] == value:
                return element
        return None

    def find_property_value(self, element, property_tag):
        property_value = self.get_element_info(self.element_data, "elements", "name", element.capitalize())
        return property_value[property_tag]

    def get_responses(self, property_tag, element, property_value):
        prop_data = self.get_element_info(self.property_intents, "intents", "tag", property_tag)
        response = prop_data['response'].format(element=element, property=property_value)
        return response

    def generate_response(self, user_message):
        found_question = any(question.lower() in user_message.lower() for question in self.question_strings)

        if found_question:
            element = self.find_element(user_message)
            property_tag = self.find_property_tag(user_message)

            if element and property_tag:
                property_value = self.find_property_value(element, property_tag)
                response = self.get_responses(property_tag, element, property_value)
                return response
            else:
                return None
        else:
            return None

    def main(self):
        pass

if __name__ == "__main__":
    SearchElement().main()
