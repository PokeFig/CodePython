import tkinter as tk
from tkinter import ttk, messagebox

class SharedData:
    def __init__(self):
        self.user = tk.StringVar()
        self.pwd = tk.StringVar()

class Pageconnect(tk.Frame):
    def __init__(self, master, callback, shared_data):
        super().__init__(master)

        self.master = master
        self.callback = callback
        self.shared_data = shared_data

        tk.Label(self, text="Bienvenue sur la page de connexion").pack(pady=10)

        ttk.Label(self, text="username:").pack()
        ttk.Entry(self, textvariable=self.shared_data.user).pack()
        ttk.Label(self, text="password:").pack()
        ttk.Entry(self, textvariable=self.shared_data.pwd, show="*").pack()

        # Bouton pour passer à la page suivante
        ttk.Button(self, text="Login", command=self.afficher_boutons_pages).pack()

    def afficher_boutons_pages(self):
        username = self.shared_data.user.get()
        password = self.shared_data.pwd.get()

        if username == "Prod" and password == "trust":
            self.callback(PageProduction, self.shared_data)
        elif username == "Logic" and password == "trust":
            self.callback(PageLogistique, self.shared_data)
        elif username == "Mister-J23" and password == "trust":
            ttk.Button(self, text="Production", command=self.go_prod).pack()
            ttk.Button(self, text="Logistique", command=self.go_logic).pack()
            ttk.Button(self, text="Administrateur", command=self.go_Admin).pack()
        else:
            messagebox.showinfo(
                message=f'!!!Aucun droit!!!'
            )

    def go_prod(self):
        self.callback(PageProduction, self.shared_data)

    def go_logic(self):
        self.callback(PageLogistique, self.shared_data)

    def go_Admin(self):
        self.callback(PageDetails, self.shared_data)

class PageProduction(tk.Frame):
    def __init__(self, master, callback, shared_data):
        super().__init__(master)

        self.master = master
        self.callback = callback
        self.shared_data = shared_data

        tk.Label(self, text="C'est la page de Production").pack(pady=10)

        # Bouton pour revenir à la page d'accueil
        tk.Button(self, text="Déconnexion", command=self.deco).pack(pady=10)

        # Afficher un bouton supplémentaire si l'utilisateur est "Mister-J23"
        if self.shared_data.user.get() == "Mister-J23":
            tk.Button(self, text="Page Logistique", command=self.go_logic).pack(pady=10)

    def deco(self):
        self.callback(Pageconnect, self.shared_data)

    def go_logic(self):
        self.callback(PageLogistique, self.shared_data)

class PageLogistique(tk.Frame):
    def __init__(self, master, callback, shared_data):
        super().__init__(master)

        self.master = master
        self.callback = callback
        self.shared_data = shared_data

        tk.Label(self, text="C'est la page de Logistique").pack(pady=10)

        # Bouton pour revenir à la page d'accueil
        tk.Button(self, text="Déconnexion", command=self.deco).pack(pady=10)

        # Afficher un bouton supplémentaire si l'utilisateur est "Mister-J23"
        if self.shared_data.user.get() == "Mister-J23":
            tk.Button(self, text="Page Production", command=self.go_prod).pack(pady=10)

    def deco(self):
        self.callback(Pageconnect, self.shared_data)

    def go_prod(self):
        self.callback(PageProduction, self.shared_data)

class PageDetails(tk.Frame):
    def __init__(self, master, callback, shared_data):
        super().__init__(master)
        self.master = master
        self.callback = callback
        self.shared_data = shared_data
        tk.Label(self, text="C'est la page des détails").pack(pady=10)

        # Bouton pour revenir à la page d'accueil
        tk.Button(self, text="Retour à l'accueil", command=self.retour_accueil).pack(pady=10)

    def retour_accueil(self):
        self.callback(Pageconnect, self.shared_data)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PokeFig")
        self.geometry("800x600")

        self.shared_data = SharedData()
        self.page_actuelle = None
        self.changer_page(Pageconnect, self.shared_data)

    def changer_page(self, classe_page, shared_data):
        nouvelle_page = classe_page(self, self.changer_page, shared_data)

        if self.page_actuelle is not None:
            self.page_actuelle.destroy()

        nouvelle_page.pack()
        self.page_actuelle = nouvelle_page

if __name__ == "__main__":
    app = Application()
    app.mainloop()
