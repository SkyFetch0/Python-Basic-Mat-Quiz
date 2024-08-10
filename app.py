import tkinter as tk
from tkinter import messagebox
import random
import threading

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
        self.generate_question()
        self.ask_question_periodically()

    def disable_event(self, event=None):
        if event is None:  
            messagebox.showwarning("Warning", "This window cannot be closed or minimized.")

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
        interval = random.randint(350, 600)
        threading.Timer(interval, self.show_question_window).start()

    def show_question_window(self):
        self.generate_question()
        self.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()
