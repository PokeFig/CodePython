#######################################################################
######                     Programme main                       #######
#######################################################################
#                                                                     #
# Version 3.0                                                         #
# Autor : LP                                                          #
#######################################################################
#======================================================================
#!/usr/bin/env python3
#======================================================================
# Interface ODOO avec l'API XML-RPC
#======================================================================

from odoo import Connect
from Production import Product
from Production import SaveProductImage

#======================================================================
#Déclaration de varaibles global
#----------------------------------------------------------------------

gUid = None
gUrl = None
password = "Ntm123456789!"
database = "PokeFigDataBase"

#======================================================================
if __name__ == "__main__":
    
    models_proxy = Connect(server_ip="172.31.10.65", server_port=8069, password="Ntm123456789!")

    if models_proxy:
        products = Product(models_proxy, 20, password, database)                                                                      # Récupération de tous les produits de la BDD (ID, Nom, Prix)
        SaveProductImage(models_proxy, "PokeFigDataBase", 20, password, 48, "storage_box_image")                                      # Enregistrement de l'image demandée
        if products:

            for product in products:                                                                                                  # Boucle pour écriture la liste dans la console
                print(f"ID: {product.get('id')}, Nom: {product.get('name')}, Prix: {product.get('list_price')}€")

            