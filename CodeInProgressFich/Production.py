#!/usr/bin/env python3
#=================================================================
# Interface ODOO avec l'API XML-RPC
#=================================================================

import xmlrpc.client

gUid = None
gUrl = None
password = "Ntm123456789!"
database = "PokeFigDataBase"
IdProduct = ""


#=================================================================

def Connect(server_ip="172.31.10.65", server_port=8069, password="Ntm123456789!"):                                   #Définition de l'accès a la odoo

    gUrl = f"http://{server_ip}:{server_port}/xmlrpc/2/common"                                                       #Construction de l'URL de connexion Odoo

    try:
        
        common_proxy = xmlrpc.client.ServerProxy(gUrl,allow_none=True)                                               #Connexion au serveur Odoo en utilisant XML-RPC
        gUid = common_proxy.authenticate(database, "paimblancleo@gmail.com", password, {})                           #Authentification

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

#=================================================================

def Product(models, gUid, password, database):
    try:
        product_ids = models.execute_kw("PokeFigDataBase", gUid, password,
                                        'product.template', 'search_read',
                                        [[]],
                                        {'fields': ['id', 'name', 'list_price']})
        return product_ids if product_ids else None
    except Exception as e:
        print(f"Erreur lors de la recherche des produits : {e}")
        return None

    
#=================================================================

if __name__ == "__main__":
    models_proxy = Connect()
    
    if models_proxy:
        # Récupération de tous les produits de la BDD (ID, Nom, Prix)
        products = Product(models_proxy, 20, password, "PokeFigDataBase")
        if products:

            for product in products:
                print(f"ID: {product.get('id')}, Nom: {product.get('name')}, Prix: {product.get('list_price')}€")
           