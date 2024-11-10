import json
from tkinter import messagebox

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Hata", "Soru dosyası bulunamadı!")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Hata", "Soru dosyası hatalı!")
        return None

class Statistics:
    def __init__(self):
        self.total_questions = 0
        self.correct_answers = 0
        self.wrong_answers = 0

    def update(self, is_correct):
        self.total_questions += 1
        if is_correct:
            self.correct_answers += 1
        else:
            self.wrong_answers += 1

    def get_stats_text(self):
        return (f"Doğru: {self.correct_answers} | "
                f"Yanlış: {self.wrong_answers} | "
                f"Toplam: {self.total_questions}")