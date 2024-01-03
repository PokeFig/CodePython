#!/usr/bin/env python3
#=================================================================
# Interface ODOO avec l'API XML-RPC
#=================================================================

import xmlrpc.client

#=================================================================


def Connect(server_ip="172.31.10.65", server_port=8069, password="", database="PokeFigDataBase"):
    # Construction de l'URL de connexion Odoo
    url = f"http://{server_ip}:{server_port}/xmlrpc/2/common"

    try:
        # Connexion au serveur Odoo en utilisant XML-RPC
        common_proxy = xmlrpc.client.ServerProxy(url)

        # Authentification
        uid = common_proxy.authenticate(database, "paimblancleo@gmail.com", password, {})

        if uid:
            print(f"Connecté à Odoo version {common_proxy.version()} à l'adresse : {url}")
            print(f"Identifiant de l'utilisateur (uid) : {uid}")

            # Récupération des modèles Odoo
            models = xmlrpc.client.ServerProxy(f"http://{server_ip}:{server_port}/xmlrpc/2/object")
            print("Connexion OK")
            return models
        else:
            print("Échec de l'authentification. Vérifiez les informations d'identification.")
            return None

    except Exception as e:
        print(f"Erreur de connexion à Odoo : {e}")
        print("Échec Connexion")
        return None

if __name__ == "__main__":
    
    mot_de_passe = "Ntm123456789!"
    models_proxy = Connect(password=mot_de_passe)