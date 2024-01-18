#######################################################################
######                 Code Fonction Production                 #######
#######################################################################
#                                                                     #
# Version 2.0                                                         #
# Autor : L.P                                                         #
#######################################################################
#======================================================================

import base64
import xmlrpc.client

#======================================================================

server_ip="172.31.10.64"
server_port=8069
password = "Ntm123456789!"
database = "PokeFigDataBase"

gUrl = f"http://{server_ip}:{server_port}/xmlrpc/2/common" 
common_proxy = xmlrpc.client.ServerProxy(gUrl)
gUid = common_proxy.authenticate("PokeFigDataBase", "paimblancleo@gmail.com", password, {})

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

#-------------------------------------------------------------------

def SaveProductImage(models, db, uid, password, product_id):
    try:
        # Récupérer le produit avec l'identifiant product_id
        product = models.execute_kw(
            db, uid, password,
            'product.template', 'read',
            [product_id],
            {'fields': ['image_1920']}
        )
        image_name = str(product_id)
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
    
def getManufOrderToDo(models):
    
    production_ids = models.execute_kw(database, gUid, password,
                                   'mrp.production', 'search',
                                   [[]])

    if production_ids:
        print("Associations ID - Référence - Date prévue - Nom de l'article - Quantité produite - Quantité à produire - État des ordres de fabrication:")

    for production_id in production_ids:
        # Lecture des informations associées à l'ID
        production_info = models.execute_kw(database, gUid, password,
                                            'mrp.production', 'read',
                                            [production_id],
                                            {'fields': ['name', 'product_id', 'state', 'date_planned_start', 'qty_produced', 'product_qty']})
        
        if production_info:
            reference = production_info[0]['name']
            date_planned = production_info[0]['date_planned_start']
            product_name = production_info[0]['product_id'][1]  # Le nom de l'article est dans la position 1
            qty_produced = production_info[0]['qty_produced']
            qty_to_produce = production_info[0]['product_qty']
            state = production_info[0]['state']
            print(f"ID {production_id} - Référence: {reference} - Date prévue: {date_planned} - Nom de l'article: {product_name} - Quantité produite: {qty_produced} - Quantité à produire: {qty_to_produce} - État: {state}")
        else:
            print(f"ID {production_id} : Informations non trouvées.")
    else:
        print("Aucun ordre de fabrication trouvé.")

#--------------------------------------------------------------------