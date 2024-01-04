import xmlrpc.client

#=================================================================

def Connect(server_ip="172.31.10.65", server_port=8069, password="Ntm123456789!"):                                   #Définition de l'accès a la odoo

    gUrl = f"http://{server_ip}:{server_port}/xmlrpc/2/common"                                                       #Construction de l'URL de connexion Odoo

    try:
        
        common_proxy = xmlrpc.client.ServerProxy(gUrl,allow_none=True)                                               #Connexion au serveur Odoo en utilisant XML-RPC
        gUid = common_proxy.authenticate("PokeFigDataBase", "paimblancleo@gmail.com", password, {})                           #Authentification

        if gUid:
            print(f"Connecté à Odoo version {common_proxy.version()} à l'adresse : {gUrl}")                          #Ecriture dans la console
            print(f"Identifiant de l'utilisateur (uid) : {gUid}")                                                    #Ecriture dans la console

            models = xmlrpc.client.ServerProxy(f"http://{server_ip}:{server_port}/xmlrpc/2/object")                  #Récupération des modèles Odoo
            print("Connexion OK")                                                                                    #Ecriture dans la console si connexion reussie
            return models
        else:
            print("Échec de l'authentification. Vérifiez les informations d'identification.")                        #Ecriture dans la console si echèc de l'authentification
            return None

    except Exception as e:
        print(f"Erreur de connexion à Odoo : {e}")                                                                   #Ecriture dans la console si echèc de l'authentification
        print("Échec Connexion")
        return None
    
