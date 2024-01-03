import tkinter as tk

class PageAccueil(tk.Frame):
    def __init__(self, master, callback):
        super().__init__(master)
        self.master = master
        self.callback = callback

        tk.Label(self, text="Bienvenue sur la page d'accueil").pack(pady=10)

        # Bouton pour passer à la page suivante
        tk.Button(self, text="Afficher les détails", command=self.afficher_details).pack(pady=10)

    def afficher_details(self):
        self.callback(PageDetails)

class PageDetails(tk.Frame):
    def __init__(self, master, callback):
        super().__init__(master)
        self.master = master
        self.callback = callback

        tk.Label(self, text="C'est la page des détails").pack(pady=10)

        # Bouton pour revenir à la page d'accueil
        tk.Button(self, text="Retour à l'accueil", command=self.retour_accueil).pack(pady=10)

    def retour_accueil(self):
        self.callback(PageAccueil)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Navigation de pages en Python")
        self.geometry("400x300")

        self.page_actuelle = None
        self.changer_page(PageAccueil)

    def changer_page(self, classe_page):
        nouvelle_page = classe_page(self, self.changer_page)

        if self.page_actuelle is not None:
            self.page_actuelle.destroy()

        nouvelle_page.pack()
        self.page_actuelle = nouvelle_page

if __name__ == "__main__":
    app = Application()
    app.mainloop()
