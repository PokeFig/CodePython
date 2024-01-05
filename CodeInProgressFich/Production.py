#######################################################################
######                 Code Fonction Production                 #######
#######################################################################
#                                                                     #
# Version 2.0                                                         #
# Autor : L.P                                                         #
#######################################################################
#======================================================================

import base64


gUid = None
gUrl = None
password = "Ntm123456789!"
database = "PokeFigDataBase"

#======================================================================

def Product(models, gUid, password, database):
    try:
        product_ids = models.execute_kw( database, gUid, password,
                                        'product.template', 'search_read',
                                        [[]],
                                        {'fields': ['default_code']})
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
            with open(image_name + '.png', 'wb') as file:
                file.write(image_bytes)

            print(f"L'image du produit avec l'ID {product_id} a été sauvegardée dans {image_name}.png")
        else:
            print(f"Aucune image trouvée pour le produit avec l'ID {product_id}")

    except Exception as e:
        print(f"Erreur lors de la sauvegarde de l'image : {e}")

#----------------------------------------------------------------------
    
def getManufOrderToDo(models,limit=10):

    fields =['name', 'date_planned_start', 'product_id', 'product_qty', 'qty_producing', 'state']
    limit = 10
    mo_list = models.execute_kw(database, gUid,
    'mrp.production', 'search_read',
    [[('state', '=', 'confirmed'), ('qty_produced', '!=', 'product_qty')]], 
    {'fields': fields, 'limit': limit})
    for mo_dico in mo_list:
     print(f'----------------------------')
    for k in mo_dico.keys():
     print(f' - {k} : {mo_dico[k]}')

#----------------------------------------------------------------------