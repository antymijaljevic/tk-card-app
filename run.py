import tkinter as tk
from tkinter import messagebox
import csv
import random

class CardApp:
    def __init__(self, master):
        # Initialize the application window and set its title and background color
        self.master = master
        self.master.title("Card App v1.0.0")
        self.master.configure(bg="#F5F5F5")

        # Calculate and set the dimensions and position of the application window
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        app_width = int(screen_width * 0.4)
        app_height = int(screen_height * 0.6)
        app_x = (screen_width - app_width) // 2
        app_y = (screen_height - app_height) // 2
        self.master.geometry(f"{app_width}x{app_height}+{app_x}+{app_y}")

        # Initialize dictionary data and load dictionary from CSV file
        self.words_opened = 0
        self.words_known = 0
        self.words_unknown = 0
        self.dict = self.load_dictionary_from_csv("dict.csv")

        # Label for quitting message
        self.quit_label = tk.Label(master, text="<Esc> to quit program", font=("Arial", 12), bg="#F5F5F5", fg="#FF5722")
        self.quit_label.pack(fill=tk.X, pady=(25, 0))

        # Create current word display frame and labels for word and translation
        self.current_word_frame = tk.Frame(master, bg="#FFFFFF", padx=50, pady=50, bd=3, relief=tk.SOLID)
        self.current_word_frame.pack(pady=(0.05 * app_height, 0.05 * app_height))
        
        self.word_label = tk.Label(self.current_word_frame, text="", font=("Arial", 28, "bold"), bg="#FFFFFF", width=13, height=2)
        self.word_label.pack(pady=(0, 0.01 * app_height))
        
        self.translation_label = tk.Label(self.current_word_frame, text="", font=("Arial", 16), bg="#FFFFFF")
        self.translation_label.pack(pady=(0, 0.01 * app_height))
        self.translation_toggle_label = tk.Label(self.current_word_frame, text="Show Translation", font=("Arial", 12, "italic", "underline"), bg="#FFFFFF", fg="blue")
        self.translation_toggle_label.pack(pady=(0, 0.02 * app_height))
        self.translation_toggle_label.bind("<Button-1>", self.toggle_translation)
        
        # Label for shuffle message
        self.shuffle_label = tk.Label(master, text="<Space> to shuffle cards", font=("Arial", 12), bg="#F5F5F5", fg="#00008B")
        self.shuffle_label.pack(fill=tk.X, pady=(25, 0))
        # Create labels for word counters
        self.opened_counter_label = tk.Label(master, text=f"Opened Cards: {self.words_opened}/{len(self.dict)}", font=("Arial", 12), bg="#F5F5F5")
        self.opened_counter_label.pack(fill=tk.X, padx=(0.1 * app_width, 0.1 * app_width), pady=(0.02 * app_height, 0))
        self.known_counter_label = tk.Label(master, text=f"Known Words: {self.words_known}", font=("Arial", 12), bg="#F5F5F5", fg="#4CAF50")
        self.known_counter_label.pack(fill=tk.X, padx=(0.1 * app_width, 0.1 * app_width), pady=(0.01 * app_height, 0))
        self.unknown_counter_label = tk.Label(master, text=f"Unknown Words: {self.words_unknown}", font=("Arial", 12), bg="#F5F5F5", fg="#F44336")
        self.unknown_counter_label.pack(fill=tk.X, padx=(0.1 * app_width, 0.1 * app_width), pady=(0.01 * app_height, 0))

        # Navigation buttons
        upper_frame = tk.Frame(master, bg="#F5F5F5")
        upper_frame.pack(pady=(20, 0.01 * app_height))

        self.know_button = tk.Button(upper_frame, text="Known <Up>", font=("Arial", 14), command=self.on_know, bg="#4CAF50", fg="white", width=15, height=1)
        self.know_button.pack(side=tk.TOP, padx=(0.01 * app_width, 0.01 * app_width), pady=(0.01 * app_height, 0), anchor='center')

        lower_frame = tk.Frame(master, bg="#F5F5F5")
        lower_frame.pack(pady=(0, 0.01 * app_height))

        self.prev_button = tk.Button(lower_frame, text="Previous <Left>", font=("Arial", 14), command=self.show_previous_word, bg="#FFA500", fg="white", width=12, height=1)
        self.prev_button.pack(side=tk.LEFT, padx=(0.01 * app_width, 0.01 * app_width), pady=(0, 0.01 * app_height))

        self.next_button = tk.Button(lower_frame, text="Next <Right>", font=("Arial", 14), command=self.show_next_word, bg="#FFA500", fg="white", width=12, height=1)
        self.next_button.pack(side=tk.RIGHT, padx=(0.001 * app_width, 0.01 * app_width), pady=(0, 0.01 * app_height))

        self.dont_know_button = tk.Button(lower_frame, text="Unknown <Down>", font=("Arial", 14), command=self.on_dont_know, bg="#F44336", fg="white", width=15, height=1)
        self.dont_know_button.pack(side=tk.TOP, padx=(0.001 * app_width, 0.01 * app_width), pady=(0, 0.01 * app_height), anchor='center')

        # Bind keyboard shortcuts to actions
        self.result_window = None
        self.master.bind("<Shift_R>", self.toggle_translation)
        master.bind("<Up>", lambda event: self.know_button.invoke())
        master.bind("<Down>", lambda event: self.dont_know_button.invoke())
        master.bind("<Left>", lambda event: self.prev_button.invoke())
        master.bind("<Right>", lambda event: self.next_button.invoke())
        master.bind("<space>", self.shuffle_and_restart)

        # Add a flag to track if the user has gone back once
        self.went_back_once = False

        # Start the application by displaying the first word
        self.update_word()

    def shuffle_and_restart(self, event):
        # Shuffle cards and restart the game
        self.shuffle_dictionary()
        self.restart_results()
        self.update_word()

    def load_dictionary_from_csv(self, filename):
        # Load dictionary data from a CSV file
        csv_to_dict = {}
        try:
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) == 2:
                        csv_to_dict[row[0]] = row[1]
                    else:
                        messagebox.showwarning("Error", f"Invalid format in CSV file: {filename}")
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        return csv_to_dict
    
    def shuffle_dictionary(self):
        shuffled_keys = list(self.dict.keys())
        random.shuffle(shuffled_keys)
        self.dict = {key: self.dict[key] for key in shuffled_keys}

    def disable_buttons(self):
        self.know_button.config(state=tk.DISABLED)
        self.dont_know_button.config(state=tk.DISABLED)
    
    def enable_buttons(self):
        self.know_button.config(state=tk.NORMAL)
        self.dont_know_button.config(state=tk.NORMAL)

    def toggle_translation(self, event):
        # Toggle display of word translation
        if not self.translation_label.cget('text'):
            self.translation_label.config(text=self.current_translation, font=("Arial", 16))
            self.translation_toggle_label.config(text="Hide Translation <Shift>", fg="red")
        else:
            self.translation_label.config(text="")
            self.translation_toggle_label.config(text="Show Translation <Shift>", fg="blue")

    def update_word(self):
        # Update the display with the next word
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
        # Display the previous word if the user hasn't gone back once yet
        if not self.went_back_once:
            if self.words_opened > 1:
                self.words_opened -= 2
                self.update_word()
                self.went_back_once = True
                self.disable_buttons()

    def show_next_word(self):
        # Display the next word if the user has gone back once
        if self.went_back_once:
            self.update_word()
            self.enable_buttons()
            self.went_back_once = False

    def on_know(self):
        # Handler for when the user knows the word
        self.words_known += 1
        self.known_counter_label.config(text=f"Known Words: {self.words_known}", fg="#4CAF50")
        self.update_word()

    def on_dont_know(self):
        # Handler for when the user doesn't know the word
        self.words_unknown += 1
        self.unknown_counter_label.config(text=f"Unknown Words: {self.words_unknown}", fg="#F44336")
        self.update_word()

    def show_results(self):
        # Display results window with statistics
        self.result_window = tk.Toplevel(self.master)
        self.result_window.title("Results")
        self.result_window.configure(bg="#F5F5F5")

        self.master.update_idletasks()
        result_window_width = self.result_window.winfo_reqwidth()
        result_window_height = self.result_window.winfo_reqheight()

        main_window_center_x = self.master.winfo_rootx() + self.master.winfo_width() // 2
        main_window_center_y = self.master.winfo_rooty() + self.master.winfo_height() // 2

        x_offset = main_window_center_x - result_window_width // 2
        y_offset = main_window_center_y - result_window_height // 2

        self.result_window.geometry("+{}+{}".format(x_offset, y_offset))

        total_cards_label = tk.Label(self.result_window, text=f"Total Cards Shown: {self.words_opened}", font=("Arial", 16), bg="#F5F5F5")
        total_cards_label.pack(pady=(50, 10))

        words_known_label = tk.Label(self.result_window, text=f"Words Known: {self.words_known} ({(self.words_known/self.words_opened)*100:.2f}%)", font=("Arial", 16), bg="#F5F5F5", fg="#4CAF50")
        words_known_label.pack(pady=10)

        words_unknown_label = tk.Label(self.result_window, text=f"Words Unknown: {self.words_unknown} ({(self.words_unknown/self.words_opened)*100:.2f}%)", font=("Arial", 16), bg="#F5F5F5", fg="#F44336")
        words_unknown_label.pack(pady=10)

        ok_button = tk.Button(self.result_window, text="OK <Return>", font=("Arial", 14), command=self.close_result_window_and_restart, bg="#2196F3", fg="white")
        ok_button.pack(pady=20)
        self.result_window.bind('<Return>', lambda event: ok_button.invoke())

    def restart_results(self):
        self.words_opened = 0
        self.words_known = 0
        self.words_unknown = 0
        self.known_counter_label.config(text=f"Known Words: {self.words_known}", fg="#4CAF50")
        self.unknown_counter_label.config(text=f"Unknown Words: {self.words_unknown}", fg="#F44336")

    def close_result_window_and_restart(self):
        # Close the results window and restart the application
        self.result_window.destroy()
        self.restart_results()
        self.update_word()
        self.enable_buttons()

def close_app(root, result_window):
    # Close the application window and destroy the results window if open
    if result_window:
        result_window.destroy()
    root.destroy()

def main():
    # Main function to initialize the Tkinter application
    root = tk.Tk()
    app = CardApp(root)
    root.bind('<Escape>', lambda event: close_app(root, app.result_window))
    root.mainloop()

if __name__ == "__main__":
    main()
