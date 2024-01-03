import xmlrpc.client

def Connect(server_ip="localhost", server_port=8069, password="", database="PokeFigDataBase"):
    # Construction de l'URL de connexion Odoo
    url = f"http://{server_ip}:{server_port}/xmlrpc/2/common"

    try:
        # Connexion au serveur Odoo en utilisant XML-RPC
        common_proxy = xmlrpc.client.ServerProxy(url)

        # Authentification
        uid = common_proxy.authenticate(database, "buisson.a@ad.afpi-bretagne.com", password, {})

        if uid:
            print(f"Connecté à Odoo version {common_proxy.version()}")
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
    

    
def Company(models, db, uid, password, company_name):
    try:
        # Recherche de la compagnie dans la table res.company
        company_id = models.execute_kw(
            db, uid, password,
            'res.company', 'search', 
            [[('name', '=', company_name)]]
        )

        if company_id:
            company_data = models.execute_kw(
                db, uid, password,
                'res.company', 'read', [company_id[0]], {'fields': ['name', 'id']}
            )

            print(f"Nom de la compagnie : {company_data[0]['name']}")
            print(f"Identifiant de la compagnie : {company_data[0]['id']}")
        else:
            print("Compagnie inexistante")

    except Exception as e:
        print(f"Erreur lors de la recherche de la compagnie : {e}")


if __name__ == "__main__":
    mot_de_passe = "Ntm123456789!"
    models_proxy = Connect(password=mot_de_passe)

    # Utilisation des modèles Odoo
    if models_proxy:
        

        # Fermeture de la connexion
        models_proxy.close()