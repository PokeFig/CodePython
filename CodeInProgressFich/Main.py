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
#from Production import SaveProductImage
#from Production import Product
#from Production import getManufOrderToDo
#from Production import createManufOrder
import Production

models_proxy = Connect(server_ip="172.31.10.64", server_port=8069, password="Ntm123456789!",)

#======================================================================
#Déclaration de varaibles global
#----------------------------------------------------------------------

password = "Ntm123456789!"
database = "PokeFigDataBase"
order_id = ''                                                                                                   

#======================================================================
if __name__ == "__main__":

    if models_proxy:

        products = Production.Product(models_proxy, 20, password, database)                                                                      # Récupération de tous les produits de la BDD (ID, Nom, Prix)
        
        
        if products:

            for product in products:                                                                                                  # Boucle pour écriture la liste dans la console
                print(f"ID: {product.get('id')}")
                #SaveProductImage(models_proxy, "PokeFigDataBase", 20, password, product.get('id'))                                                   # Enregistrement de l'image demandée

        
    Production.getManufOrderToDo(models_proxy)
    Production.createManufOrder(models_proxy, product_id=57, quantity=1)

     #Production.confirmManufOrder(models_proxy,order_id)

#======================================================================