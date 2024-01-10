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
from Production import SaveProductImage
from Production import Product
from Production import getManufOrderToDo

models_proxy = Connect(server_ip="172.31.10.65", server_port=8069, password="Ntm123456789!",)

#======================================================================
#Déclaration de varaibles global
#----------------------------------------------------------------------

gUid = None
gUrl = None
password = "Ntm123456789!"
database = "PokeFigDataBase"
image_name = ''

#======================================================================
if __name__ == "__main__":

    if models_proxy:

        products = Product(models_proxy, 20, password, database)                                                                        # Récupération de tous les produits de la BDD (ID, Nom, Prix)
        
        
        if products:

            for product in products:                                                                                                       # Boucle pour écriture la liste dans la console
                print(f"ID: {product.get('id')}")


    image_name = (f"ID: {product.get('id')}")
    SaveProductImage(models_proxy, "PokeFigDataBase", 20, password, 48, image_name)                                      # Enregistrement de l'image demandée
        
        #getManufOrderToDo(models_proxy)

#======================================================================