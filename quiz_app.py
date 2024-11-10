import tkinter as tk
from tkinter import messagebox
import random
import threading
from math_operation import MathOperation
from utils import load_json_file, Statistics
from config import APP_SETTINGS, QUIZ_SETTINGS, PATHS

class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_ui()
        self.initialize_state()
        self.start_quiz()

    def setup_window(self):
        self.root.title(APP_SETTINGS['TITLE'])
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.root.bind('<Alt-F4>', self.disable_event)
        self.root.bind('<Unmap>', self.disable_event)

    def setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True)

        self.question_label = tk.Label(
            main_frame,
            text="",
            font=(APP_SETTINGS['FONT_FAMILY'], APP_SETTINGS['QUESTION_FONT_SIZE'])
        )
        self.question_label.pack(pady=20)

        self.answer_entry = tk.Entry(
            main_frame,
            font=(APP_SETTINGS['FONT_FAMILY'], APP_SETTINGS['QUESTION_FONT_SIZE'])
        )
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind('<Return>', lambda e: self.check_answer())


        self.submit_button = tk.Button(
            main_frame,
            text="Cevapla",
            command=self.check_answer,
            font=(APP_SETTINGS['FONT_FAMILY'], APP_SETTINGS['BUTTON_FONT_SIZE'])
        )
        self.submit_button.pack(pady=10)

        self.message_label = tk.Label(
            main_frame,
            text="",
            font=(APP_SETTINGS['FONT_FAMILY'], APP_SETTINGS['MESSAGE_FONT_SIZE'])
        )
        self.message_label.pack(pady=10)

        self.stats_label = tk.Label(
            main_frame,
            text="",
            font=(APP_SETTINGS['FONT_FAMILY'], 12)
        )
        self.stats_label.pack(pady=5)

    def initialize_state(self):
        self.correct_answer = 0
        self.statistics = Statistics()
        self.active_timers = []
        self.used_questions = set()

    def start_quiz(self):
        self.get_question()
        self.ask_question_periodically()

    def disable_event(self, event=None):
        return "break"

    def get_question(self):
        data = load_json_file(PATHS['QUESTIONS_FILE'])
        if not data:
            return

        available_questions = [q for q in data['quiz']
                               if id(q) not in self.used_questions]

        if not available_questions:
            self.used_questions.clear()
            available_questions = data['quiz']

        question_data = random.choice(available_questions)
        self.used_questions.add(id(question_data))

        if question_data['type'] == 'random':
            settings = question_data['settings']
            math_op = MathOperation(settings)
            result = math_op.calculate()

            self.correct_answer = result['result']
            self.question_label.config(
                text=f"{result['num1']} {result['operation']} {result['num2']}"
            )

    def check_answer(self):
        user_input = self.answer_entry.get().strip()

        if user_input == QUIZ_SETTINGS['EXIT_CODE']:
            self.cleanup()
            return

        if not user_input:
            self.message_label.config(
                text="Lütfen bir cevap girin!",
                fg="orange"
            )
            return

        try:
            user_answer = float(user_input)
            is_correct = abs(user_answer - self.correct_answer) < 0.01

            if is_correct:
                self.message_label.config(text="Doğru Bildin!", fg="green")
                self.statistics.update(True)
                for timer in self.active_timers:
                    timer.cancel()
                self.active_timers.clear()
                self.ask_question_periodically()
                self.root.withdraw()
            else:
                self.message_label.config(text="Yanlış Bildin Tekrar Dene!", fg="red")
                self.statistics.update(False)

            self.stats_label.config(text=self.statistics.get_stats_text())

        except ValueError:
            self.message_label.config(text="Geçerli bir sayı girin.", fg="red")

        self.answer_entry.delete(0, tk.END)

    def ask_question_periodically(self):
        interval = random.randint(
            QUIZ_SETTINGS['MIN_INTERVAL'],
            QUIZ_SETTINGS['MAX_INTERVAL']
        )
        timer = threading.Timer(interval, self.show_question_window)
        self.active_timers.append(timer)
        timer.start()

    def show_question_window(self):
        self.get_question()
        self.root.deiconify()
        self.answer_entry.focus()

    def cleanup(self):
        for timer in self.active_timers:
            timer.cancel()
        self.active_timers.clear()
        self.root.quit()