#!usr/bin/env python3
from collections import deque

class Calculator:
    def __init__(self):
        self.end = False
        self.user_input = None
        self.other_options = ["/exit", "/help"]
        self.variables_dict = dict()
        self.help = "Smart calculator: please insert the expressions with the PEP 8 notation"

    def is_int(self, element):
        try:
            if int(element):
                return True
        except ValueError:
            return False

    def signs_and_coherence(self, expresion):
        is_coherent = True
        new_list = []
        brackets = deque()
        for i in expresion.split():
            minus = i.count('-')
            plus = i.count('+')
            time = i.count('*')
            divide = i.count('/')
            if minus % 2 == 0 and minus > 0:
                new_list.append(i.replace(minus*'-', '+'))
            elif minus % 2 != 0 and minus > 0:
                new_list.append(i.replace(minus*'-', '-'))
            elif minus == 0 and plus == 0:
                new_list.append(i)
            elif plus > 0:
                new_list.append(i.replace(plus*'+', '+'))
            if time > 1 or divide > 1:
                is_coherent = False
                break
        try:
            for element in expresion:
                if element == '(':
                    brackets.append(element)
                elif element == ')':
                    brackets.pop()
            if len(brackets) != 0:
                is_coherent = False
        except IndexError:
            is_coherent = False
        new_expresion = ' '.join(new_list)
        return new_expresion, is_coherent

    def infix_to_postfix(self, user_input):
        user_input = user_input.replace('(', '( ')
        user_input = user_input.replace(')', ' )')
        user_input = deque(user_input.split())
        output_stack = deque()
        operator_stack = deque()
        other_operators = ['(', ')']
        operator_precedence = {'/': 2, '*': 2, '+': 1, '-': 1}
        while user_input:
            element = user_input.popleft()
            if element.isalpha() or self.is_int(element):
                output_stack.append(element)

            elif element in operator_precedence.keys():
                if not operator_stack:
                    operator_stack.append(element)

                elif operator_stack[-1] == other_operators[0]:
                    operator_stack.append(element)

                elif operator_precedence[element] > operator_precedence[operator_stack[-1]]:
                    operator_stack.append(element)

                elif operator_precedence[element] <= operator_precedence[operator_stack[-1]]:
                    end_pop = False
                    while not end_pop and operator_stack:
                        operator = operator_stack.pop()
                        if operator == other_operators[0]:
                            end_pop = True
                            operator_stack.append(operator)
                        elif operator_precedence[element] > operator_precedence[operator]:
                            end_pop = True
                        else:
                            output_stack.append(operator)
                    operator_stack.append(element)

            elif element == other_operators[0]:
                operator_stack.append(element)

            elif element == other_operators[1]:
                end_pop = False
                while not end_pop:
                    operator = operator_stack.pop()
                    if operator == other_operators[0]:
                        end_pop = True
                    elif operator != other_operators[0]:
                        output_stack.append(operator)

        while operator_stack:
            operator = operator_stack.pop()
            output_stack.append(operator)

        return output_stack

    def postfix_to_result(self, postfix_stack):
        result_stack = deque()
        operators = ['/', '*', '+', '-']
        while postfix_stack:
            element = postfix_stack.popleft()
            if self.is_int(element):
                result_stack.append(element)
            elif element in operators:
                try:
                    second_number = int(result_stack.pop())
                    first_number = int(result_stack.pop())
                    if element == operators[0]:
                        result_stack.append(first_number / second_number)

                    elif element == operators[1]:
                        result_stack.append(first_number * second_number)

                    elif element == operators[2]:
                        result_stack.append(first_number + second_number)

                    elif element == operators[3]:
                        result_stack.append(first_number - second_number)
                except IndexError:
                    pass
        try:
            return result_stack[-1]
        except IndexError:
            return 'Unknown variable'


    def calculator_commands(self):
        if self.user_input == self.other_options[1]:
            print(self.help)

        elif self.user_input == self.other_options[0]:
            self.end = True
            print("Bye!")
        elif self.user_input.startswith('/') and self.user_input not in self.other_options:
            print('Unknown command')

    def update_dict(self):
        try:
            key, value = self.user_input.replace(' ', '').split('=')
            if key.isalpha():
                if value not in self.variables_dict.keys() and not value.isalpha():
                    try:
                        self.variables_dict[key] = int(value)
                    except ValueError:
                        print("Invalid assignment")
                elif value not in self.variables_dict.keys() and value.isalpha():
                    print('Unknown variable')
                else:
                    self.variables_dict[key] = self.variables_dict[value]
            else:
                print('Invalid identifier')

        except ValueError:
            print("Invalid assignment")

    def replace_variable(self):
        new_user_input = self.user_input
        for element in self.user_input.split():
            if element in self.variables_dict.keys():
                new_user_input = new_user_input.replace(element, str(self.variables_dict[element]))
        return new_user_input

    def calculator_operation(self):
        if not self.user_input.startswith('/'):
            try:
                user_input = self.replace_variable()
                new_expresion , is_coherent = self.signs_and_coherence(user_input)
                if is_coherent:
                    postfix = self.infix_to_postfix(new_expresion)
                    result = self.postfix_to_result(postfix)
                    print(result)
                else:
                    print('Invalid expression')
            except (ValueError, SyntaxError, NameError):
                print('Unknown variable')

    def main(self):
        while not self.end:
            self.user_input = input()
            if len(self.user_input) > 0:
                if '=' in self.user_input:
                    self.update_dict()
                else:
                    self.calculator_operation()
                    self.calculator_commands()


if __name__ == '__main__':
    Calculator().main()
