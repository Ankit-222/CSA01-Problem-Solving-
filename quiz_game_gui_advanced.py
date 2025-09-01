# quiz_game_gui_advanced.py

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
import os
import platform

try:
    # For sound playback (Windows)
    if platform.system() == "Windows":
        import winsound
    else:
        # For other OS, playsound package can be used if installed
        from playsound import playsound
except ImportError:
    pass

questions = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "answer": "Paris",
        "icon": "icons/france.png"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "Mars",
        "icon": "icons/mars.png"
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic", "Indian", "Pacific", "Arctic"],
        "answer": "Pacific",
        "icon": "icons/ocean.png"
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["Charles Dickens", "William Shakespeare", "Mark Twain", "J.K. Rowling"],
        "answer": "William Shakespeare",
        "icon": "icons/book.png"
    },
    {
        "question": "Which gas do plants use for photosynthesis?",
        "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
        "answer": "Carbon Dioxide",
        "icon": "icons/plant.png"
    }
]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌟 Quiz Game 🌟")
        self.root.geometry("650x450")
        self.root.configure(bg="#2c3e50")  # Dark blue background

        self.score = 0
        self.q_index = 0
        self.time_left = 15  # 15 second timer per question
        self.timer_running = False

        # Title label
        self.title_label = tk.Label(root, text="Quiz Game", font=("Helvetica", 26, "bold"), fg="#ecf0f1", bg="#2c3e50")
        self.title_label.pack(pady=10)

        # Frame for question, icon and options
        self.frame = tk.Frame(root, bg="#34495e", bd=5, relief="ridge")
        self.frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Icon for question
        self.icon_label = tk.Label(self.frame, bg="#34495e")
        self.icon_label.pack(side="left", padx=10, pady=10)

        # Frame for question text and options
        self.qa_frame = tk.Frame(self.frame, bg="#34495e")
        self.qa_frame.pack(side="left", fill="both", expand=True, pady=10)

        # Question label
        self.question_label = tk.Label(self.qa_frame, text="", wraplength=450, font=("Helvetica", 16), fg="#ecf0f1", bg="#34495e")
        self.question_label.pack(pady=(0, 20))

        self.var = tk.StringVar()
        self.options = []

        for i in range(4):
            rb = tk.Radiobutton(
                self.qa_frame,
                text="",
                variable=self.var,
                value="",
                font=("Helvetica", 14),
                bg="#34495e",
                fg="#ecf0f1",
                selectcolor="#2980b9",
                activebackground="#2980b9",
                activeforeground="white",
                pady=5,
                anchor="w"
            )
            rb.pack(fill="x", padx=20, pady=5)
            self.options.append(rb)

        # Progress and timer frame
        self.bottom_frame = tk.Frame(root, bg="#2c3e50")
        self.bottom_frame.pack(fill="x", padx=20, pady=(0,10))

        # Progress label
        self.progress_label = tk.Label(self.bottom_frame, text="", font=("Helvetica", 12), fg="#ecf0f1", bg="#2c3e50")
        self.progress_label.pack(side="left")

        # Timer label
        self.timer_label = tk.Label(self.bottom_frame, text="", font=("Helvetica", 12, "bold"), fg="#e74c3c", bg="#2c3e50")
        self.timer_label.pack(side="right")

        # Submit button with hover effect
        self.submit_button = tk.Button(root, text="Submit", font=("Helvetica", 14, "bold"), bg="#27ae60", fg="white", activebackground="#2ecc71", activeforeground="white", padx=20, pady=8, command=self.submit_answer)
        self.submit_button.pack(pady=10)

        self.submit_button.bind("<Enter>", lambda e: self.submit_button.config(bg="#2ecc71"))
        self.submit_button.bind("<Leave>", lambda e: self.submit_button.config(bg="#27ae60"))

        self.load_question()

    def load_question(self):
        if self.q_index < len(questions):
            self.fade_out_in(self.show_question)
        else:
            self.show_result()

    def show_question(self):
        q = questions[self.q_index]
        self.question_label.config(text=f"Q{self.q_index + 1}: {q['question']}")

        # Load icon image
        icon_path = q.get("icon", None)
        if icon_path and os.path.exists(icon_path):
            img = Image.open(icon_path)
            img = img.resize((80, 80), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(img)
            self.icon_label.config(image=self.photo)
        else:
            self.icon_label.config(image='')

        self.var.set(None)
        for i, option in enumerate(q["options"]):
            self.options[i].config(text=option, value=option)

        self.progress_label.config(text=f"Question {self.q_index + 1} of {len(questions)}")
        self.time_left = 15
        self.update_timer_label()
        self.timer_running = True
        self.run_timer()

    def run_timer(self):
        if self.time_left > 0 and self.timer_running:
            self.time_left -= 1
            self.update_timer_label()
            self.root.after(1000, self.run_timer)
        elif self.time_left == 0 and self.timer_running:
            self.timer_running = False
            messagebox.showinfo("Time's up!", "You ran out of time! Moving to next question.")
            self.q_index += 1
            self.load_question()

    def update_timer_label(self):
        self.timer_label.config(text=f"Time left: {self.time_left}s")

    def submit_answer(self):
        if not self.var.get():
            messagebox.showwarning("Warning", "Please select an option!")
            return

        self.timer_running = False  # stop timer

        selected = self.var.get()
        correct = questions[self.q_index]["answer"]

        # Play sounds
        self.play_sound(correct == selected)

        if correct == selected:
            self.score += 1

        self.q_index += 1
        self.load_question()

    def play_sound(self, correct):
        # Play simple beep for right or wrong answer
        try:
            if platform.system() == "Windows":
                if correct:
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                else:
                    winsound.MessageBeep(winsound.MB_ICONHAND)
            else:
                # For other OS (Linux/Mac), you can use playsound package and wav files if you add them
                pass
        except Exception as e:
            pass  # if sound fails, ignore

    def fade_out_in(self, func):
        # Simple fade effect by gradually changing background color brightness
        def fade(step=0):
            if step <= 10:
                color_val = 44 + step * 8
                hex_color = f"#{color_val:02x}{color_val+10:02x}{color_val+20:02x}"
                self.frame.config(bg=hex_color)
                self.question_label.config(bg=hex_color)
                self.qa_frame.config(bg=hex_color)
                self.icon_label.config(bg=hex_color)
                for rb in self.options:
                    rb.config(bg=hex_color)
                self.root.after(30, lambda: fade(step+1))
            else:
                func()
                fade_back(10)

        def fade_back(step):
            if step >= 0:
                color_val = 44 + step * 8
                hex_color = f"#{color_val:02x}{color_val+10:02x}{color_val+20:02x}"
                self.frame.config(bg=hex_color)
                self.question_label.config(bg=hex_color)
                self.qa_frame.config(bg=hex_color)
                self.icon_label.config(bg=hex_color)
                for rb in self.options:
                    rb.config(bg=hex_color)
                self.root.after(30, lambda: fade_back(step-1))

        fade()

    def show_result(self):
        result_msg = f"Quiz Completed!\nYour score: {self.score} / {len(questions)}"
        if self.score == len(questions):
            result_msg += "\n🏆 Excellent! Perfect Score!"
        elif self.score >= len(questions) / 2:
            result_msg += "\n👍 Good job!"
        else:
            result_msg += "\n😕 Better luck next time!"
        messagebox.showinfo("Result", result_msg)
        self.root.destroy()


if __name__ == "__main__":
    # Check if PIL is installed (required for images)
    try:
        from PIL import Image, ImageTk
    except ImportError:
        messagebox.showerror("Missing Package", "Please install pillow package:\npip install pillow")
        exit()

    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
