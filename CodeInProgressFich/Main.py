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
import Production


models_proxy = Connect(server_ip="172.31.10.64", server_port=8069, password="Ntm123456789!",)

#======================================================================
#Déclaration de varaibles global
#----------------------------------------------------------------------

password = "Ntm123456789!"
database = "PokeFigDataBase"
order_id = 29     
quantity = 10                                                                                      
product_id = 56

#======================================================================
if __name__ == "__main__":

    if models_proxy:

        #products = Production.Product(models_proxy, 20, password, database)                                                                      # Récupération de tous les produits de la BDD (ID, Nom, Prix)
        
        
        #if products:

            #for product in products:                                                                                                  # Boucle pour écriture la liste dans la console
                #print(f"ID: {product.get('id')}")
                #ShowProductImage(, models_proxy, "PokeFigDataBase", 20, password, product.get('id'))                                                   # Enregistrement de l'image demandée

        
     #Production.getManufOrderToDo(models_proxy)                                                                      #Récupération des OF
     #Production.createManufOrder(models_proxy, quantity, product_id)                                                 #Création des OF
     #Production.confirmManufOrder(models_proxy,order_id)                                                             #confirmation de l'OF
     Production.DoneManufOrder(models_proxy, order_id)                                                                 #Ordre de fabrication terminé
     #Production.CancelManufOrder(models_proxy,order_id)

#======================================================================