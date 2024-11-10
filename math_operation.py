import random
import operator
import math


class MathOperation:
    def __init__(self, settings):
        self.min_val = settings['min']
        self.max_val = settings['max']
        self.operation_type = settings['operation']

        self.safe_operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '%': operator.mod,
            '**': operator.pow,
            'floor': math.floor,
            'ceil': math.ceil,
            'sqrt': math.sqrt,
        }

    def is_safe_operation(self):
        return self.operation_type in self.safe_operators

    def generate_numbers(self):
        num1 = random.randint(self.min_val, self.max_val)

        if self.operation_type == '/':
            num2 = random.randint(1, self.max_val)
        elif self.operation_type == 'sqrt':
            num1 = abs(num1)
            return [num1]
        else:
            num2 = random.randint(self.min_val, self.max_val)

        return [num1, num2]

    def calculate(self):
        if not self.is_safe_operation():
            raise ValueError(f"Güvenli olmayan operatör: {self.operation_type}")

        numbers = self.generate_numbers()
        operator_func = self.safe_operators[self.operation_type]

        try:
            if len(numbers) == 1:
                result = operator_func(numbers[0])
            else:
                result = operator_func(numbers[0], numbers[1])

            return {
                'numbers': numbers,
                'result': result,
                'operation': self.operation_type,
                'num1': numbers[0],
                'num2': numbers[1] if len(numbers) > 1 else None
            }
        except Exception as e:
            raise ValueError(f"Hesaplama hatası: {str(e)}")