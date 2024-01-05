import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import CodeLoginJardel


class SharedData:
    def __init__(self):
        self.user = tk.StringVar()
        self.pwd = tk.StringVar()

#page de connexion
class Pageconnect(tk.Frame):
    def __init__(self, master, callback, shared_data):
        super().__init__(master, background="#33c4ff")

        self.master = master
        self.callback = callback
        self.shared_data = shared_data

        #création du groupe d'éléments
        content_frame = ttk.Frame(self)
        
        image_path = "CodePython/CodeInProgressFich/poke.png"
        self.image = tk.PhotoImage(file=image_path)

        # Créer un Label pour afficher l'image
        image_label = tk.Label(self, image=self.image, background="#33c4ff").grid(row=1, column=0, padx=10, pady=(20,1))
        tk.Label(self, text="PokeFig", font=('Times New Roman', 32, 'bold'), foreground="#F1A226", background="#33c4ff").grid(row=2, column=0, padx=10, pady=(1,1))
        tk.Label(self, text="Bienvenue sur la page de connexion", font=('Arial', 14), background="#33c4ff").grid(row=3, column=0, padx=10, pady=(0, 200))

        ttk.Label(content_frame, text="username:").grid(row=0, column=0, padx=10, pady=5)
        ttk.Entry(content_frame, textvariable=self.shared_data.user).grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(content_frame, text="password:").grid(row=1, column=0, padx=10, pady=5)
        ttk.Entry(content_frame, textvariable=self.shared_data.pwd, show="*").grid(row=1, column=1, padx=10, pady=5)
        

        # Bouton pour passer à la page suivante
        ttk.Button(content_frame, text="Login", command=self.afficher_boutons_pages).grid(row=2, column=0, columnspan=2, pady=10)

        content_frame.grid(row=1, column=1, rowspan=4, padx=100)



    def afficher_boutons_pages(self):
        username = self.shared_data.user.get()
        password = self.shared_data.pwd.get()

        prof = CodeLoginJardel.ProfilType

        if prof == "production":
            self.callback(PageProduction, self.shared_data)
        elif prof == "logistique":
            self.callback(PageLogistique, self.shared_data)
        elif prof == "administrateur":
            ttk.Button(self, text="Production", command=self.go_prod).pack()
            ttk.Button(self, text="Logistique", command=self.go_logic).pack()
            ttk.Button(self, text="Administrateur", command=self.go_Admin).pack()
        else:
            messagebox.showinfo(
                message=f'!!!Aucun droit!!!'
            )
        subprocess.run(["python3", "/home/user/Documents/clone/CodePython/CodeInProgressFich/CodeLoginJardel.py"])

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
