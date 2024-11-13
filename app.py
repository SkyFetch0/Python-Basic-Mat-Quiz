import tkinter as tk
from tkinter import messagebox
import random
import threading
import json
import operator
import math


class MathOperation:
    def __init__(self, settings):
        self.min_val = settings['min']
        self.max_val = settings['max']
        self.operation_type = settings['operation']

        # Güvenli operatör mapping'i
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
            # Daha fazla math operatörü eklenebilir
        }

    def is_safe_operation(self):
        return self.operation_type in self.safe_operators

    def generate_numbers(self):
        num1 = random.randint(self.min_val, self.max_val)

        # Özel durumlar için kontroller
        if self.operation_type == '/':
            num2 = random.randint(1, self.max_val)  # 0'a bölünmeyi engelle
        elif self.operation_type == 'sqrt':
            num1 = abs(num1)  # Negatif sayının karekökünü engelle
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
                'num2': numbers[1]
            }
        except Exception as e:
            raise ValueError(f"Hesaplama hatası: {str(e)}")


class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matematik Soruları")

        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)

        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.root.bind('<Alt-F4>', self.disable_event)
        self.root.bind('<Unmap>', self.disable_event)

        self.question_label = tk.Label(root, text="", font=("Arial", 24))
        self.question_label.pack(pady=20)
        self.answer_entry = tk.Entry(root, font=("Arial", 24))
        self.answer_entry.pack(pady=10)
        self.submit_button = tk.Button(root, text="Cevapla", command=self.check_answer, font=("Arial", 20))
        self.submit_button.pack(pady=10)
        self.message_label = tk.Label(root, text="", font=("Arial", 18))
        self.message_label.pack(pady=10)
        self.correct_answer = 0
        self.get_question()
        self.ask_question_periodically()

    def disable_event(self, event=None):
        if event is None:
            messagebox.showwarning("Warning", "This window cannot be closed or minimized.")

    def get_question(self):
        with open('data.json') as json_data:
            alldata = json.load(json_data)
            print(alldata)
            data = random.choice(alldata['quiz'])

            name = data['name']
            type = data['type']
            if(type == 'random'):
                settings = data['settings']
                math_op = MathOperation(data['settings'])
                result = math_op.calculate()
                num1 = result['num1']
                num2 = result['num2']
                operator = result['operation']
                print(f"Sayılar: {result['numbers']}")
                print(f"İşlem: {result['operation']}")
                print(f"Sonuç: {result['result']}")
                self.correct_answer = result['result']
                self.question_label.config(text=f"{num1} {operator} {num2}")

    def generate_question(self):
        if random.choice(['add', 'multiply']) == 'add':
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
            self.correct_answer = num1 + num2
            self.question_label.config(text=f"{num1} + {num2} = ?")
        else:
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 20)
            self.correct_answer = num1 * num2
            self.question_label.config(text=f"{num1} x {num2} = ?")

    def check_answer(self):
        user_input = self.answer_entry.get()
        if user_input == "gizliSifre":
            self.root.quit()
        else:
            try:
                user_answer = int(user_input)
                if user_answer == self.correct_answer:
                    self.message_label.config(text="Doğru Bildin!", fg="green")
                    self.root.withdraw()
                    self.ask_question_periodically()
                else:
                    self.message_label.config(text="Yanlış Bildin Tekrar Dene!", fg="red")
            except ValueError:
                self.message_label.config(text="Adam Akıllı Bir Sayı Gir.", fg="red")
            self.answer_entry.delete(0, tk.END)

    def ask_question_periodically(self):
        interval = random.randint(15, 20)
        threading.Timer(interval, self.show_question_window).start()

    def show_question_window(self):
        self.get_question()
        self.root.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()
