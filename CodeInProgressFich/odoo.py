import xmlrpc.client

#==============================

def Connect(server_ip="localhost", server_port=8069, password="", database="PokeFigDataBase"):
    # Construction de l'URL de connexion Odoo
    url = f"http://{server_ip}:{server_port}/xmlrpc/2/common"

    try:
        # Connexion au serveur Odoo en utilisant XML-RPC
        common_proxy = xmlrpc.client.ServerProxy(url)

        # Authentification
        uid = common_proxy.authenticate(database, "buisson.a@ad.afpi-bretagne.com", password, {})

        if uid:
            print(f"Connecté à Odoo version {common_proxy.version()} à l'adresse : {url}")
            print(f"Identifiant de l'utilisateur (uid) : {uid}")
        else:
            print("Échec de l'authentification. Vérifiez les informations d'identification.")

    except Exception as e:
        print(f"Erreur de connexion à Odoo : {e}")

if __name__ == "__main__":
    # Spécifiez le mot de passe ici si nécessaire
    mot_de_passe = "Ntm123456789!"
    Connect(password=mot_de_passe)