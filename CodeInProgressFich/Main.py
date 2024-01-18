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
from Production1copy import ShowProductImage
from Production1copy import Product
#from Production1 import getManufOrderToDo

models_proxy = Connect(server_ip="172.31.10.64", server_port=8069, password="Ntm123456789!",)

#======================================================================
#Déclaration de varaibles global
#----------------------------------------------------------------------

password = "Ntm123456789!"
database = "PokeFigDataBase"                                                                                                              

#======================================================================
if __name__ == "__main__":

    if models_proxy:

        products = Product(models_proxy, 20, password, database)                                                                      # Récupération de tous les produits de la BDD (ID, Nom, Prix)
        
        
        if products:

            for product in products:                                                                                                  # Boucle pour écriture la liste dans la console
                print(f"ID: {product.get('id')}")
                ShowProductImage(, models_proxy, "PokeFigDataBase", 20, password, product.get('id'))                                                   # Enregistrement de l'image demandée

        
    #getManufOrderToDo(models_proxy)

#======================================================================