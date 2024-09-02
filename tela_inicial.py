import tkinter as tk
from tkinter import messagebox
import subprocess
import os

class TelaInicial:
    def __init__(self, root):
        self.root = root
        self.root.title("Tela Inicial")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        self.button_main = tk.Button(self.frame, text="Abrir Tela Main", command=self.abrir_main)
        self.button_main.pack(pady=10)

        self.button_turing = tk.Button(self.frame, text="Abrir Tela Turing", command=self.abrir_turing)
        self.button_turing.pack(pady=10)

    def abrir_main(self):
        try:
            # Atualize o caminho conforme a localização do seu arquivo main.py
            subprocess.Popen(["python", "interface_automato.py"], cwd=os.path.dirname(os.path.abspath(__file__)))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o main.py: {e}")

    def abrir_turing(self):
        try:
            # Atualize o caminho conforme a localização do seu arquivo turing_main.py
            subprocess.Popen(["python", "turing_main.py"], cwd=os.path.dirname(os.path.abspath(__file__)))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o turing_main.py: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TelaInicial(root)
    root.mainloop()