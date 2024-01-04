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
            # Convertir la chaîne d'image base64 en bytes
            image_bytes = base64.b64decode(product[0]['image_1920'])

            # Sauvegarder l'image au format '.png' sur le disque
            with open(image_name, 'wb') as f:
                f.write(image_bytes)

            print(f"L'image du produit avec l'ID {product_id} a été sauvegardée dans {image_name}")
        else:
            print(f"Aucune image trouvée pour le produit avec l'ID {product_id}")

    except Exception as e:
        print(f"Erreur lors de la sauvegarde de l'image : {e}")


#----------------------------------------------------------------------         