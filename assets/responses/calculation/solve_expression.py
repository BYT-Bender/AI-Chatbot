import os
import sys
import re

parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(parent_directory)

from utilities import Utility

class SolveExpression:
    def __init__(self, config):
        self.config = config
        self.utility = Utility(self.config)

    operator_map = {
        '+': ('plus', 'add'),
        '-': ('minus', 'subtract'),
        '*': ('multiply', 'times', 'multiplied by', 'x'),
        '/': ('divided by', 'divide', 'over', 'upon'),
    }

    def get_operator(self, word):
        for operator, synonyms in self.operator_map.items():
            if word in synonyms:
                return operator
        return None

    def map_terms_to_operators(self, expression):
        for operator, terms in self.operator_map.items():
            for term in terms:
                expression = expression.replace(term, operator)
        return expression

    def evaluate_expression(self, expression):
        try:            
            expression = self.map_terms_to_operators(expression)
            
            try:
                result = eval(expression)
                if result is not None:
                    expression = re.sub(r'([-+*/])', r' \1 ', expression)
                    equation = f"{expression} = {result}"
                    self.utility.log_action(f'Chatbot solved `{equation}` and got `{result}`')
                    return equation
            except:
                # self.utility.log_action(f'Error: While elaluting `{expression}`: {error}')
                return None

            tokens = expression.split()
            num1, operator, num2 = None, None, None

            for token in tokens:
                if token.replace('.', '', 1).isdigit():
                    if num1 is None:
                        num1 = float(token)
                    elif num2 is None:
                        num2 = float(token)
                elif token in self.operator_map:
                    operator = token

            if num1 is not None and num2 is not None and operator is not None:
                result = eval(f"{num1} {operator} {num2}")
                equation = f"{num1} {operator} {num2} = {result}"
                self.utility.log_action(f'Chatbot solved `{equation}` and got `{result}`')
                return equation

        except Exception as error:
            # self.utility.log_action(f'Error: While solving `{expression}`: {error}')
            return None

    def generate_response(self, user_message):
        intent_keywords = ["calculate", "evaluate", "what is"]
        for keyword in intent_keywords:
            expression = user_message.replace(keyword, "").strip()

        response = self.evaluate_expression(expression)

        if response is not None:
            return str(response), "calculation"
        else:
            return None, None