#######################################################################
######                 Code Fonction Production                 #######
#######################################################################
#                                                                     #
# Version 2.0                                                         #
# Autor : B.A                                                         #
#######################################################################
#======================================================================

import base64

#======================================================================

def Product(models, gUid, password, database):
    try:
        product_ids = models.execute_kw( database, gUid, password,
                                        'product.template', 'search_read',
                                        [[]],
                                        {'fields': ['id', 'name', 'list_price']})
        return product_ids if product_ids else None
    except Exception as e:
        print(f"Erreur lors de la recherche des produits : {e}")
        return None

#----------------------------------------------------------------------

def SaveProductImage(models, db, uid, password, product_id, image_name):
    try:
        # Récupérer le produit avec l'identifiant product_id
        product = models.execute_kw(
            db, uid, password,
            'product.template', 'read',
            [product_id],
            {'fields': ['image_1920']}
        )

        if product and product[0].get('image_1920'):
            image_data = base64.b64decode(product[0]['image_1920'])
            with open(image_name + '.png', 'wb') as file:
                file.write(image_data)
            print(f"L'image du produit avec l'ID {product_id} a été sauvegardée sous {image_name}.png")
            return True
        else:
            print(f"Le produit avec l'ID {product_id} n'a pas d'image.")
            return False

    except Exception as e:
        print(f"Erreur lors de la sauvegarde de l'image du produit : {e}")
        return False


#----------------------------------------------------------------------         