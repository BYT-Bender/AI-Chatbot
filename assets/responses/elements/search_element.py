import os
import sys

parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(parent_directory)

from utilities import Utility

class SearchElement:
    def __init__(self, config):
        self.config = config
        self.utility = Utility(self.config)

        self.load_element_data()
        self.load_property_intents()

    def load_element_data(self):
        element_data_path = os.path.join(self.config["parent_directory"], self.config["data"]["element"]["data"])
        self.element_data = self.utility.load_json("Element Data", element_data_path, show=False)
        self.elements = [element['name'] for element in self.element_data['elements']]

    def load_property_intents(self):
        property_intents_path = os.path.join(self.config["parent_directory"], self.config["data"]["element"]["intents"])
        self.property_intents = self.utility.load_json("Element Intents", property_intents_path, show=False)
        self.property_patterns = {element['tag']: element['patterns'] for element in self.property_intents['intents']}

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
        return property_value.get(property_tag, None)

    def get_responses(self, property_tag, element, property_value):
        prop_data = self.get_element_info(self.property_intents, "intents", "tag", property_tag)
        if prop_data:
            response = prop_data['response'].format(element=element, property=property_value)
            return response
        return None

    def get_description(self, element):
        element = element.capitalize()
        atomic_number = self.find_property_value(element, "atomic_number")
        symbol = self.find_property_value(element, "symbol")
        description = self.find_property_value(element, "description")

        response = f"{element} is a chemical element with the symbol {symbol} and atomic number {atomic_number}. {description.replace(element, 'It')}"
        return response

    def generate_response(self, user_message):
        question_strings = ["what is", "tell me", "do you know", "are you aware of"]
        found_question = any(question.lower() in user_message.lower() for question in question_strings)

        if found_question:
            element = self.find_element(user_message)
            property_tag = self.find_property_tag(user_message)

            if element:
                if property_tag:
                    property_value = self.find_property_value(element, property_tag)
                    if property_value is not None:
                        response = self.get_responses(property_tag, element, property_value)
                        if response:
                            self.utility.log_action(f'Chatbot responded to `{user_message}` with offline dataset search result `{response}`')
                            return response, "element"
                        
                response = self.get_description(element)
                if response:
                    return response, "element"

        return None, None