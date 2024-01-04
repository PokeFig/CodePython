#######################################################################
######                     Programme main                       #######
#######################################################################
#                                                                     #
# Version 1.0                                                         #
# Autor : B.A                                                         #
#######################################################################

#======================================================================

import odoo 
import Production

odoo.Connect()

#======================================================================
#!/usr/bin/env python3
#=================================================================
# Interface ODOO avec l'API XML-RPC
#=================================================================

gUid = None
gUrl = None
password = "Ntm123456789!"
database = "PokeFigDataBase"

#=================================================================
if __name__ == "__main__":
    models_proxy = odoo.Connect(server_ip="172.31.10.65", server_port=8069, password="Ntm123456789!")
    
    if models_proxy:
        # Récupération de tous les produits de la BDD (ID, Nom, Prix)
        products = Production.Product(models_proxy, 20, password, database)
        if products:

            for product in products:
                print(f"ID: {product.get('id')}, Nom: {product.get('name')}, Prix: {product.get('list_price')}€")