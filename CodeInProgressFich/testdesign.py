import tkinter as tk
from tkinter import ttk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Placement avec grid()")
        self.geometry("400x300")

        # Créer un conteneur Frame
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True)

        # Ajouter des widgets à l'intérieur du Frame en utilisant grid()
        label1 = ttk.Label(frame, text="Widget 1")
        label1.grid(row=0, column=0, padx=10, pady=10)

        label2 = ttk.Label(frame, text="Widget 2")
        label2.grid(row=1, column=1, padx=10, pady=10)

        button = ttk.Button(frame, text="Cliquez-moi")
        button.grid(row=2, column=2, padx=10, pady=10)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
