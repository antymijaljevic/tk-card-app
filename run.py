import tkinter as tk
from tkinter import messagebox
import csv
import random

class CardApp:
    def __init__(self, master):
        self.master = master
        self.setup_gui()
        self.load_dictionary()
        self.initialize_counters()
        self.shuffle_dictionary()
        self.bind_shortcuts()
        self.update_word()

    def setup_gui(self):
        self.master.title("Card App v1.0.0")
        self.master.configure(bg="#F5F5F5")
        self.center_window(0.4, 0.6)
        
        self.quit_label = tk.Label(self.master, text="<Esc> to quit program", font=("Arial", 12), bg="#F5F5F5", fg="#FF5722")
        self.quit_label.pack(fill=tk.X, pady=(25, 0))

        self.setup_current_word_frame()
        self.shuffle_label = tk.Label(self.master, text="<Space> to shuffle cards", font=("Arial", 12), bg="#F5F5F5", fg="#00008B")
        self.shuffle_label.pack(fill=tk.X, pady=(25, 0))
        
        self.setup_counters()
        self.setup_navigation_buttons()

    def center_window(self, width_ratio, height_ratio):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        app_width = int(screen_width * width_ratio)
        app_height = int(screen_height * height_ratio)
        app_x = (screen_width - app_width) // 2
        app_y = (screen_height - app_height) // 2
        self.master.geometry(f"{app_width}x{app_height}+{app_x}+{app_y}")

    def setup_current_word_frame(self):
        self.current_word_frame = tk.Frame(self.master, bg="#FFFFFF", padx=50, pady=50, bd=3, relief=tk.SOLID)
        self.current_word_frame.pack(pady=(50, 50))
        
        self.word_label = tk.Label(self.current_word_frame, text="", font=("Arial", 28, "bold"), bg="#FFFFFF", width=13, height=2)
        self.word_label.pack(pady=(0, 20))
        
        self.translation_label = tk.Label(self.current_word_frame, text="", font=("Arial", 16), bg="#FFFFFF")
        self.translation_label.pack(pady=(0, 20))
        
        self.translation_toggle_label = tk.Label(self.current_word_frame, text="Show Translation", font=("Arial", 12, "italic", "underline"), bg="#FFFFFF", fg="blue")
        self.translation_toggle_label.pack(pady=(0, 20))
        self.translation_toggle_label.bind("<Button-1>", self.toggle_translation)

    def setup_counters(self):
        self.opened_counter_label = tk.Label(self.master, text=f"Opened Cards: {self.words_opened}/{len(self.dict)}", font=("Arial", 12), bg="#F5F5F5")
        self.opened_counter_label.pack(fill=tk.X, padx=(80, 80), pady=(20, 0))
        
        self.known_counter_label = tk.Label(self.master, text=f"Known Words: {self.words_known}", font=("Arial", 12), bg="#F5F5F5", fg="#4CAF50")
        self.known_counter_label.pack(fill=tk.X, padx=(80, 80), pady=(10, 0))
        
        self.unknown_counter_label = tk.Label(self.master, text=f"Unknown Words: {self.words_unknown}", font=("Arial", 12), bg="#F5F5F5", fg="#F44336")
        self.unknown_counter_label.pack(fill=tk.X, padx=(80, 80), pady=(10, 0))

    def setup_navigation_buttons(self):
        upper_frame = tk.Frame(self.master, bg="#F5F5F5")
        upper_frame.pack(pady=(20, 20))

        self.know_button = tk.Button(upper_frame, text="Known <Up>", font=("Arial", 14), command=self.on_know, bg="#4CAF50", fg="white", width=15, height=1)
        self.know_button.pack(side=tk.TOP, padx=20, pady=10, anchor='center')

        lower_frame = tk.Frame(self.master, bg="#F5F5F5")
        lower_frame.pack(pady=(10, 20))

        self.prev_button = tk.Button(lower_frame, text="Previous <Left>", font=("Arial", 14), command=self.show_previous_word, bg="#FFA500", fg="white", width=12, height=1)
        self.prev_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.next_button = tk.Button(lower_frame, text="Next <Right>", font=("Arial", 14), command=self.show_next_word, bg="#FFA500", fg="white", width=12, height=1)
        self.next_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.dont_know_button = tk.Button(lower_frame, text="Unknown <Down>", font=("Arial", 14), command=self.on_dont_know, bg="#F44336", fg="white", width=15, height=1)
        self.dont_know_button.pack(side=tk.TOP, padx=20, pady=10, anchor='center')

    def bind_shortcuts(self):
        self.master.bind("<Shift_R>", self.toggle_translation)
        self.master.bind("<Up>", lambda event: self.know_button.invoke())
        self.master.bind("<Down>", lambda event: self.dont_know_button.invoke())
        self.master.bind("<Left>", lambda event: self.prev_button.invoke())
        self.master.bind("<Right>", lambda event: self.next_button.invoke())
        self.master.bind("<space>", self.shuffle_and_restart)

    def initialize_counters(self):
        self.words_opened = 0
        self.words_known = 0
        self.words_unknown = 0
        self.went_back_once = False

    def load_dictionary(self):
        self.dict = {}
        try:
            with open("dict.csv", newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) == 2:
                        self.dict[row[0]] = row[1]
                    else:
                        messagebox.showwarning("Error", "Invalid format in CSV file")
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found: dict.csv")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def shuffle_and_restart(self, event=None):
        self.shuffle_dictionary()
        self.restart_results()
        self.update_word()

    def shuffle_dictionary(self):
        keys = list(self.dict.keys())
        random.shuffle(keys)
        self.dict = {key: self.dict[key] for key in keys}

    def toggle_translation(self, event=None):
        if not self.translation_label.cget('text'):
            self.translation_label.config(text=self.current_translation, font=("Arial", 16))
            self.translation_toggle_label.config(text="Hide Translation <Shift>", fg="red")
        else:
            self.translation_label.config(text="")
            self.translation_toggle_label.config(text="Show Translation <Shift>", fg="blue")

    def update_word(self):
        if self.words_opened < len(self.dict):
            self.current_word = list(self.dict.keys())[self.words_opened]
            self.current_translation = self.dict[self.current_word]
            self.word_label.config(text=self.current_word)
            
            self.translation_label.config(text="")
            self.translation_toggle_label.config(text="Show Translation <Shift>", fg="blue")

            self.words_opened += 1
            self.opened_counter_label.config(text=f"Opened Cards: {self.words_opened}/{len(self.dict)}", fg="#333333")
        else:
            self.show_results()
            self.disable_buttons()

    def show_previous_word(self):
        if not self.went_back_once and self.words_opened > 1:
            self.words_opened -= 2
            self.update_word()
            self.went_back_once = True
            self.disable_buttons()

    def show_next_word(self):
        if self.went_back_once:
            self.update_word()
            self.enable_buttons()
            self.went_back_once = False

    def on_know(self):
        self.words_known += 1
        self.known_counter_label.config(text=f"Known Words: {self.words_known}", fg="#4CAF50")
        self.update_word()

    def on_dont_know(self):
        self.words_unknown += 1
        self.unknown_counter_label.config(text=f"Unknown Words: {self.words_unknown}", fg="#F44336")
        self.update_word()

    def show_results(self):
        self.result_window = tk.Toplevel(self.master)
        self.result_window.title("Results")
        self.result_window.configure(bg="#F5F5F5")
        self.center_window_for_result()

        total_cards_label = tk.Label(self.result_window, text=f"Total Cards Shown: {self.words_opened}", font=("Arial", 16), bg="#F5F5F5")
        total_cards_label.pack(pady=(50, 10))

        words_known_label = tk.Label(self.result_window, text=f"Words Known: {self.words_known} ({(self.words_known/self.words_opened)*100:.2f}%)", font=("Arial", 16), bg="#F5F5F5", fg="#4CAF50")
        words_known_label.pack(pady=10)

        words_unknown_label = tk.Label(self.result_window, text=f"Words Unknown: {self.words_unknown} ({(self.words_unknown/self.words_opened)*100:.2f}%)", font=("Arial", 16), bg="#F5F5F5", fg="#F44336")
        words_unknown_label.pack(pady=10)

        ok_button = tk.Button(self.result_window, text="OK <Return>", font=("Arial", 14), command=self.close_result_window_and_restart, bg="#2196F3", fg="white")
        ok_button.pack(pady=20)
        self.result_window.bind('<Return>', lambda event: ok_button.invoke())

    def center_window_for_result(self):
        self.master.update_idletasks()
        result_window_width = self.result_window.winfo_reqwidth()
        result_window_height = self.result_window.winfo_reqheight()

        main_window_center_x = self.master.winfo_rootx() + self.master.winfo_width() // 2
        main_window_center_y = self.master.winfo_rooty() + self.master.winfo_height() // 2

        x_offset = main_window_center_x - result_window_width // 2
        y_offset = main_window_center_y - result_window_height // 2

        self.result_window.geometry("+{}+{}".format(x_offset, y_offset))

    def restart_results(self):
        self.words_opened = 0
        self.words_known = 0
        self.words_unknown = 0
        self.known_counter_label.config(text=f"Known Words: {self.words_known}", fg="#4CAF50")
        self.unknown_counter_label.config(text=f"Unknown Words: {self.words_unknown}", fg="#F44336")

    def close_result_window_and_restart(self):
        self.result_window.destroy()
        self.restart_results()
        self.update_word()
        self.enable_buttons()

    def disable_buttons(self):
        self.know_button.config(state=tk.DISABLED)
        self.dont_know_button.config(state=tk.DISABLED)
    
    def enable_buttons(self):
        self.know_button.config(state=tk.NORMAL)
        self.dont_know_button.config(state=tk.NORMAL)

def close_app(root, result_window):
    if result_window:
        result_window.destroy()
    root.destroy()

def main():
    root = tk.Tk()
    app = CardApp(root)
    root.bind('<Escape>', lambda event: close_app(root, app.result_window))
    root.mainloop()

if __name__ == "__main__":
    main()
