#!/usr/bin/env python3
#=================================================================
# Interface ODOO avec l'API XML-RPC
#=================================================================


import xmlrpc.client

<<<<<<< HEAD
def Connect(server_ip="", server_port=8069, password="", database="PokeFigDataBase"):
=======
#=================================================================

def Connect(server_ip="192.168.201.2", server_port=8069, password="", database="PokeFigDataBase"):
>>>>>>> 089f519bc2868453647764a5a88ab0a8b962f926
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
<<<<<<< HEAD
=======
    
#======================================================================

def Product(models, db, uid, password):
    try:
        # Recherche de l'identifiant de la table product.template
        product_template_id = models.execute_kw(
            db, uid, password,
            'ir.model', 'search', 
            [[('model', '=', 'product.template')]]
        )

        if product_template_id:
            # Lecture de l'ensemble des produits dans la table product.template
            products = models.execute_kw(
                db, uid, password,
                'product.template', 'search_read', [[]],
                {'fields': ['id', 'name', 'list_price']}
            )

            if products:
                print("Produits trouvés :")
                for product in products:
                    print(f"#{product['id']} - {product['name']} = {product['list_price']}")
            else:
                print("Aucun produit trouvé dans la base de données.")
        else:
            print("La table product.template n'a pas été trouvée.")

    except Exception as e:
        print(f"Erreur lors de la récupération des produits : {e}")
>>>>>>> 089f519bc2868453647764a5a88ab0a8b962f926

#===============================================================
        
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

#============================================================================
        

if __name__ == "__main__":
<<<<<<< HEAD
=======

    models 
    # Spécifiez le mot de passe ici si nécessaire
    mot_de_passe = "Ntm123456789!"
    
    # Connexion à Odoo
    models_proxy = Connect(password=mot_de_passe)

    # Utilisation des modèles Odoo
    if models_proxy:
        # Utilisation de la fonction Product
        Product(models_proxy, "nom_de_votre_base_de_donnees", "uid_utilisateur", mot_de_passe)
