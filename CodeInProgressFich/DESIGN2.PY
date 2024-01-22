import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import xmlrpc.client, time
from odoo import Connect
from Production import ShowProductImage, Product


#EnterPassword = Username #"Ntm123456789!"                                                                    #VARIABLE JARDEL POUR LE MOT DE PASSE
#EnterEmail = Password #"logistique"    "buisson.a@ad.afpi-bretagne.com"                                                              #VARIABLE JARDEL POUR MAIL OU IDENTIFIANT
AuthentificationChek = False                                                                       #VARIABLE SI AUTHENTIFICATION CORRECTE
ConnectionCheck = True                                                                             #VARIABLE SI CONNEXION est correcte
ProfilType = None                                                                                  #VARIABLE TYPE DE PROFIL

#Gestion des identifiants serveurs
server_ip = "172.31.10.64"                                                                         #IP de connection du serveur Odoo
server_port = 8069                                                                                 #Port de dconnection du serveur Odoo
data_base = "PokeFigDataBase"                                                                      #Nom du conteneur dans Odoo
#password = EnterPassword                                                                           #Gestion du mot de passe
#Email = EnterEmail                                                                                 #Gestion de l'identifiant
url = f'http://{server_ip}:{server_port}'
uid = None

class SharedData:
    def __init__(self):
        self.user = tk.StringVar()
        self.pwd = tk.StringVar()
        self.listing_acces = None  # Définir listing_acces en tant que variable globale

# Page de connexion
class Pageconnect(tk.Frame):
    
    def __init__(self, master, callback, shared_data):
        super().__init__(master, background="#33c4ff")

        self.master = master
        self.callback = callback
        self.shared_data = shared_data

        # Création du groupe d'éléments
        global content_frame
        content_frame = ttk.Frame(self)

        #image_path = "CodePython/CodeInProgressFich/poke.png"
        self.image = tk.PhotoImage(file="/home/user/Documents/clone/CodePython/CodeInProgressFich/poke.png")

        # Créer un Label pour afficher l'image
        image_label = tk.Label(self, image=self.image, background="#33c4ff")
        image_label.grid(row=1, column=0, padx=10, pady=(20,1))

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
        global Username
        global Password
        Username = self.shared_data.user.get()
        Password = self.shared_data.pwd.get()

        self.ConnectionCheck()
        if AuthentificationChek == True :
            self.getFields()

    
    def ConnectionCheck(self):                                                                             #Fonction block check Connection serveur Odoo
        global AuthentificationChek
        global uid

        urlOdoo = f"http://{server_ip}:{server_port}/xmlrpc/2/common"                                 #Génération du lien pour la connection de Odoo
        try:
            common_proxy = xmlrpc.client.ServerProxy(urlOdoo)                                          #Connection au serveur avec le lien
            uid = common_proxy.authenticate(data_base, Username, Password, {})                            #Connection au profile
            
            if uid is not False:
                print(f"Connecté à Odoo version {common_proxy.version()}")                             #Retour d'information de la version d'odoo 
                AuthentificationChek = True                                                            #Variable de confirmation de l'authentification
                print(f"Identifiant de l'utilisateur (uid) : {uid}")                                   #Retour d'information du profile


            else:
                AuthentificationChek = False                                                           #Mise à faux de l'authentification
                print(f"Erreur de connexion à Odoo {common_proxy.version()}")                             #Retour d'information du serveur
        
        except Exception as e:
            print(f"Erreur de connexion à Odoo : {e}")                                                 #Retour du code erreur si pas de connexion avec le serveur
            print("Échec Connexion")
            ConnectionCheck = False
            

    def getFields(self):                                                                                   #Fonction block pour avoir les autorisations

        global listing_acces
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))                           #Connection au serveur
        try:                                                                                            
            acces = models.execute_kw(data_base, uid, Password, 'mrp.production', 'check_access_rights', ['write'])                                               
            print(f"Manufactoring order write acces rights :{acces}")
            if uid == 2 :
                ProfilType = 'administrateur'
                print(f"Profil administrateur")
                ttk.Button(content_frame, text="go prod", command=self.go_prod).grid(row=2, column=0, columnspan=1, pady=10)
                ttk.Button(content_frame, text="go logic", command=self.go_logic).grid(row=2, column=1, columnspan=1, pady=10)
                
            else:
                ProfilType = 'production'
                print(f"Profil production")
                self.callback(PageProduction, self.shared_data)

        except:
            print(f"Profil logistique")  
            ProfilType = 'logistique'
            self.callback(PageLogistique, self.shared_data)



        
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
        self.prod_images = []  # Liste pour stocker les objets PhotoImage
        

        models_proxy = Connect(server_ip="172.31.10.64", server_port=8069, password="Ntm123456789!",)
        #self.image = tk.PhotoImage(file="CodePython/CodeInProgressFich/poke.png")

        # Création de la bande bleue avec le texte "PokeFig"
        header_frame = tk.Frame(self, bg="#33c4ff")
        header_frame.grid(row=0, column=0, columnspan=100, sticky="ew")

        tk.Label(header_frame, text="PokeFig", font=('Times New Roman', 32, 'bold'), foreground="#F1A226", background="#33c4ff").pack(pady=0)

        if models_proxy:
            products = Product(models_proxy, 56, Password, data_base)

        if products:
            x = 5
            for product in products:
                num = product.get('id')
                print(f"ID: {num}")

                # Enregistrement de l'image demandée
                Image = ShowProductImage(self, models_proxy, "PokeFigDataBase", 56, Password, product.get('id'))
                image_resize = Image.resize((160, 160))
                tk_image = ImageTk.PhotoImage(image_resize)
                self.prod_images.append(tk_image)  # Stocker l'objet PhotoImage

                # Afficher l'image dans une fenêtre Tkinter
                label = tk.Label(self, image=tk_image)
                label.grid(row=3, column=x)
                self.update_idletasks()

                tk.Label(self, text="boucle").grid(row=4, column=x)
                self.update_idletasks()  # Ajout de la mise à jour de la fenêtre
                x += 1

        # Bouton pour revenir à la page d'accueil
        tk.Button(self, text="Déconnexion", command=self.deco).grid(column=0, columnspan=100)

        # Afficher un bouton supplémentaire si l'utilisateur est "Mister-J23"
        if ProfilType == "administrateur":
            tk.Button(self, text="Page Logistique", command=self.go_logic).grid()
        


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
        if ProfilType == "administrateur":
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
        self.geometry("800x600")  # Définir la taille initiale

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

