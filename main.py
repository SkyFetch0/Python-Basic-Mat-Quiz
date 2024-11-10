import tkinter as tk
from quiz_app import MathQuizApp

from check import Check


def main():
    check = Check()
    if check.check_libraries():
        root = tk.Tk()
        app = MathQuizApp(root)
        root.mainloop()

if __name__ == "__main__":
    main()