#######################################################################
######                 Code Login odoo + profile                #######
#######################################################################
#                                                                     #
# Version 1.0                                                         #
# Autor : B.A                                                         #
#######################################################################


if __name__ == "__main__":
    models_proxy = odoo.Connect()
    
    if models_proxy:
        # Récupération de tous les produits de la BDD (ID, Nom, Prix)
        products = Production.Product(models_proxy, 20, password, "PokeFigDataBase")
        if products:

            for product in products:
                print(f"ID: {product.get('id')}, Nom: {product.get('name')}, Prix: {product.get('list_price')}€")