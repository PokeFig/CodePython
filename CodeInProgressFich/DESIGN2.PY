import tkinter as tk
from tkinter import ttk, messagebox, Label
from PIL import Image, ImageTk
import xmlrpc.client, time
from odoo import Connect
from Production1copy import ShowProductImage, Product
from Production import getManufOrderToDo, ModifOF


#EnterPassword = Username #"Ntm123456789!"                                                                    #VARIABLE JARDEL POUR LE MOT DE PASSE
#EnterEmail = Password #"logistique"    "buisson.a@ad.afpi-bretagne.com"                                                              #VARIABLE JARDEL POUR MAIL OU IDENTIFIANT
AuthentificationChek = False                                                                       #VARIABLE SI AUTHENTIFICATION CORRECTE
ConnectionCheck = True                                                                             #VARIABLE SI CONNEXION est correcte
ProfilType = None                                                                                  #VARIABLE TYPE DE PROFIL

#Gestion des identifiants serveurs
server_ip = "172.18.0.1"                                                                         #IP de connection du serveur Odoo
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
        self.image = tk.PhotoImage(file="/home/user/Documents/CodePython/CodeInProgressFich/poke.png")

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
        global login
        login = ttk.Button(content_frame, text="Login", command=self.afficher_boutons_pages)
        login.grid(row=2, column=0, columnspan=2, pady=10)


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
                login.destroy()
                ttk.Button(content_frame, text="go prod", command=self.go_prod).grid(row=2, column=0, columnspan=1, pady=10)
                ttk.Button(content_frame, text="go logic", command=self.go_logic).grid(row=2, column=1, columnspan=1, pady=10)
                
            else:
                ProfilType = 'production'
                print(f"Profil production")
                self.callback(PageProduction, self.shared_data)

        except:
            #print(f"Profil logistique")  
            #ProfilType = 'logistique'
            #self.callback(PageLogistique, self.shared_data)
             messagebox.showinfo("Erreur", "Aucun droit")



        
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
        self.prod_frames = []  # Liste pour stocker les cadres des produits
        self.image_refs = []  # Liste pour stocker les références aux images


        models_proxy = Connect(server_ip="172.18.0.1", server_port=8069, password="Ntm123456789!")
        
        # Création de la bande bleue avec le texte "PokeFig"
        header_frame = tk.Frame(self, bg="#33c4ff")
        header_frame.grid(row=0, column=0, columnspan=100, sticky="ew")


        tk.Label(header_frame, text="PokeFig", font=('Times New Roman', 32, 'bold'), foreground="#F1A226", background="#33c4ff").grid(row=0, column=0, padx=10, pady=0, sticky="w")
        

        if models_proxy:
            # Appel de la fonction pour obtenir les informations des ordres de fabrication
            order_info_text = getManufOrderToDo(models_proxy)

            # Diviser les informations en blocs individuels
            orders = order_info_text.split('----------------------------')

            # Créer un cadre pour chaque bloc d'informations et les afficher côte à côte
            for i, order in enumerate(orders):
                # Créer un cadre pour afficher les informations de l'ordre
                order_frame = tk.Frame(self, relief="solid", borderwidth=1)
                order_frame.grid(row=1, column=i, padx=10, pady=10)

                # Ajouter un libellé pour afficher les informations de l'ordre
                order_label = tk.Label(order_frame, text=order, justify="left")
                order_label.pack(padx=10, pady=10)

                # Ajouter un bouton "Modifier" pour chaque cadre d'ordre de fabrication
                modify_button = ttk.Button(order_frame, text="Modifier", command=lambda idx=i: self.modify_order(models_proxy, idx))
                modify_button.pack(padx=10, pady=5)
            # Bouton pour revenir à la page d'accueil
            tk.Button(self, text="Déconnexion", command=self.deco).grid(pady=10)


    def modify_order(self, models_proxy, order_index):
        # Fonction appelée lors du clic sur le bouton "Modifier"
        # Récupérer l'ID de l'OF à modifier
        print(order_index)
        order_id = self.get_order_id(models_proxy, order_index)
        
        # Créer une nouvelle fenêtre pour la saisie des nouvelles valeurs
        modify_window = tk.Toplevel(self.master)
        modify_window.title("Modifier l'OF")
        
        # Champ de saisie pour la nouvelle quantité
        qty_label = ttk.Label(modify_window, text="Nouvelle quantité:")
        qty_label.grid(row=0, column=0, padx=10, pady=5)
        new_qty_entry = ttk.Entry(modify_window)
        new_qty_entry.grid(row=0, column=1, padx=10, pady=5)

         # Fonction pour mettre à jour l'OF et détruire la fenêtre de modification
        def update_and_close():
            self.update_order(models_proxy, order_id, new_qty_entry.get())
            modify_window.destroy()
        
        # Bouton de confirmation pour mettre à jour l'OF
        update_button = ttk.Button(modify_window, text="Mettre à jour", command=update_and_close)
        update_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
           
        

    def get_order_id(self, models_proxy, order_index):
        # Récupérer les informations des ordres de fabrication
        order_info_text = getManufOrderToDo(models_proxy)

        # Diviser les informations en blocs individuels
        orders = order_info_text.split('----------------------------')

        # Vérifier si l'index est valide
        if 0 <= order_index < len(orders):
            # Extraire l'ID de l'ordre à partir du bloc d'informations correspondant à l'index
            order_lines = orders[order_index].strip().split('\n')
            print(len(order_lines))
            for line in order_lines:
                print(line)
                if line.startswith('- id'):
                    order_id = int(line.split(':')[1].strip())
                    
                    return order_id

        # Si l'index est invalide ou si aucun ID n'est trouvé, retourner None
        print("not done")
        return None

    def update_order(self, models_proxy, order_id, new_qty):
        # Fonction pour mettre à jour la quantité de l'OF
        ModifOF(models_proxy, order_id, new_qty)
        # Mettre à jour l'affichage des informations
        # Implémentez cette partie en fonction de votre structure d'interface utilisateur
    

    def deco(self):
        self.callback(Pageconnect, self.shared_data)


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
        self.shared_data = SharedData()
        self.page_actuelle = None

        self.geometry("800x600")  # Taille initiale de la fenêtre
        self.full_screen = False  # Indicateur du mode plein écran

        # Créer un bouton pour basculer entre le mode plein écran et le mode fenêtré
        self.fullscreen_button = tk.Button(self, text="Plein écran", command=self.toggle_fullscreen)
        self.fullscreen_button.pack(anchor=tk.NE)

        # Charger la première page
        self.changer_page(Pageconnect, self.shared_data)

    def changer_page(self, classe_page, shared_data):
        nouvelle_page = classe_page(self, self.changer_page, shared_data)

        if self.page_actuelle is not None:
            self.page_actuelle.destroy()

        nouvelle_page.pack(fill=tk.BOTH, expand=True)
        self.page_actuelle = nouvelle_page

    def toggle_fullscreen(self):
        if self.full_screen:
            self.attributes("-fullscreen", False)
            self.fullscreen_button.config(text="Plein écran")
        else:
            self.attributes("-fullscreen", True)
            self.fullscreen_button.config(text="Fenêtré")

        self.full_screen = not self.full_screen



if __name__ == "__main__":
    app = Application()
    app.mainloop()

