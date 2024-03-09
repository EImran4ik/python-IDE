import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import sys

class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Прокручиваем вниз, чтобы видеть новые сообщения

class IDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Python IDE")
        self.root.configure(bg='#2b2b2b')

        self.menu_bar = tk.Menu(root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_program)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.menu_bar.add_command(label="Run", command=self.run_code)
        self.menu_bar.add_command(label="Clear Console", command=self.clear_console)

        self.root.config(menu=self.menu_bar)

        self.editor = ScrolledText(root, wrap=tk.WORD, bg='#1e1e1e', fg='#ffffff', insertbackground='#ffffff', undo=True, autoseparators=True)
        self.editor.pack(expand=True, fill=tk.BOTH)

        self.console = ScrolledText(root, wrap=tk.WORD, bg='#1e1e1e', fg='#ffffff', insertbackground='#ffffff')
        self.console.pack(expand=True, fill=tk.BOTH)

        sys.stdout = StdoutRedirector(self.console)
        sys.stderr = StdoutRedirector(self.console)

    def run_code(self):
        code = self.editor.get("1.0", tk.END)
        try:
            exec(code)
        except Exception as e:
            print(e)

    def clear_console(self):
        self.console.delete("1.0", tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", file.read())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.editor.get("1.0", tk.END))

    def exit_program(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='#2b2b2b')
    ide = IDE(root)
    root.mainloop()
