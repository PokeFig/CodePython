#######################################################################
######                 Code Fonction Production                 #######
#######################################################################
#                                                                     #
# Version 1.0                                                         #
# Autor : B.A                                                         #
#######################################################################

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

#def SaveProductImage( models, db, uid, password, product_id, image_name):

#----------------------------------------------------------------------         