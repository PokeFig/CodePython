#######################################################################
######                 Code Login odoo + profile                #######
#######################################################################
#                                                                     #
# Version 1.0                                                         #
# Autor : B.A                                                         #
#######################################################################

#################################################
# Vérification de la bonne connection Prog/odoo #
#################################################

#==========================================================
# Fonction Block Connexion
#==========================================================

import xmlrpc.client
import design
from design import SharedData, Pageconnect

EnterPassword = Pageconnect.shared_data.pwd.get()#"Ntm123456789!"                                                                    #VARIABLE JARDEL POUR LE MOT DE PASSE
EnterEmail = Pageconnect.shared_data.user.get()#"BetaTest@gmail.com"                                                                  #VARIABLE JARDEL POUR MAIL OU IDENTIFIANT
AuthentificationChek = False                                                                       #VARIABLE SI AUTHENTIFICATION CORRECTE
ConnectionCheck = True                                                                             #VARIABLE SI CONNEXION est correcte
ProfilType = None                                                                                  #VARIABLE TYPE DE PROFIL 

#Gestion des identifiants serveurs
server_ip = "172.31.10.65"                                                                         #IP de connection du serveur Odoo
server_port = 8069                                                                                 #Port de dconnection du serveur Odoo
data_base = "PokeFigDataBase"                                                                      #Nom du conteneur dans Odoo
password = EnterPassword                                                                           #Gestion du mot de passe
Email = EnterEmail                                                                                 #Gestion de l'identifiant
url = f'http://{server_ip}:{server_port}'
uid = None


def ConnectionCheck():                                                                             #Fonction block check Connection serveur Odoo
    global AuthentificationChek
    global uid

    urlOdoo = f"http://{server_ip}:{server_port}/xmlrpc/2/common"                                 #Génération du lien pour la connection de Odoo
    try:
        common_proxy = xmlrpc.client.ServerProxy(urlOdoo)                                          #Connection au serveur avec le lien
        uid = common_proxy.authenticate(data_base, Email, password, {})                            #Connection au profile
        
        if uid is not False:
            print(f"Connecté à Odoo version {common_proxy.version()}")                             #Retour d'information de la version d'odoo 
            AuthentificationChek = True                                                            #Variable de confirmation de l'authentification
            print(f"Identifiant de l'utilisateur (uid) : {uid}")                                   #Retour d'information du profile


        else:
            AuthentificationChek = False                                                           #Mise à faux de l'authentification
            print(f"Connecté à Odoo version {common_proxy.version()}")                             #Retour d'information du serveur
    
    except Exception as e:
        print(f"Erreur de connexion à Odoo : {e}")                                                 #Retour du code erreur si pas de connexion avec le serveur
        print("Échec Connexion")
        ConnectionCheck = False
        return None

def getFields():                                                                                   #Fonction block pour avoir les autorisations

    global listing_acces
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))                           #Connection au serveur
    try:                                                                                            
        acces = models.execute_kw(data_base, uid, password, 'mrp.production', 'check_access_rights', ['write'])                                               
        print(f"Manufactoring order write acces rights :{acces}")
        if uid == 2 :
            ProfilType = 'administrateur'
            print(f"Profil administrateur")
        else:
            ProfilType = 'production'
            print(f"Profil production")

    except:
        print(f"Profil logistique")  
        ProfilType = 'logistique'

    #listing_acces = models.execute_kw(data_base, uid, password, 'mrp.production', 'fields_get', [], {'attributes': []})
    #for attr in listing_acces:
        #print(f'-{attr}')
    #else:
        #print(f'Odoo server authentification rejected : DB = {data_base} User ={uid}')

def AiguillageFields():

    if listing_acces is not None:
        for attr in listing_acces:
            if 'product_id' in str(attr):
                print(f"Nom trouvé Production")
                ProfilType = 'Production'
                return True
            
    print(f"Nom  non trouvé")
    ProfilType = 'logistique'
    return False
#==========================================================
# Main
#==========================================================


if __name__ == "__main__":
 ConnectionCheck()
 getFields()
 #AiguillageFields()