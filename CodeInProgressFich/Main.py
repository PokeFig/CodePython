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
import CodeStockageJardel

models_proxy = Connect(server_ip="169.254.178.173", server_port="8069", password="Ntm123456789!")

#======================================================================
#Déclaration de varaibles global
#----------------------------------------------------------------------

password = "Ntm123456789!"
database = "PokeFigDataBase"
order_id = 36                   #Numéro de l'of pour modif
quantity = 15                   #QUAntitée qu'on veux produire
product_id = 55                 #Numéro de produit

#======================================================================
if __name__ == "__main__":

    if models_proxy:
     
     #ShowProductImage(, models_proxy, "PokeFigDataBase", 20, password, product.get('id'))                                                       # Enregistrement de l'image demandée
        
     Production.getManufOrderToDo(models_proxy)                                                                                                 #Récupération des OF
     #Production.createManufOrder(models_proxy, quantity, product_id)                                                                            #Création des OF
     #Production.confirmManufOrder(models_proxy,order_id)                                                                                        #Confirmation de l'OF
     #Production.DoneManufOrder(models_proxy,order_id,product_id,quantity)                                                                       #Ordre de fabrication terminé
     #Production.CancelManufOrder(models_proxy,order_id)                                                                                         #Annulation de l'of
     #Production.ModifOF(models_proxy, order_id, quantity)

     

#======================================================================