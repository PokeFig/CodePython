#######################################################################
######                 Code Fonction Production                 #######
#######################################################################
#                                                                     #
# Version 2.0                                                         #
# Autor : L.P                                                         #
#######################################################################
#======================================================================

import tkinter as tk
import PIL
from PIL import Image, ImageTk
import base64, time, io
import xmlrpc.client


gUid = None
gUrl = None
password = "Ntm123456789!"
database = "PokeFigDataBase"

# Fonction pour récupérer la liste des produits
def Product(models, gUid, password, database):
    try:
        product_ids = models.execute_kw(database, gUid, password,
                                        'product.template', 'search_read',
                                        [[]],
                                        {'fields': ['default_code']})
        return product_ids if product_ids else None
    except Exception as e:
        print(f"Erreur lors de la recherche des produits : {e}")
        return None

# Fonction pour afficher une image d'un produit spécifique
def ShowProductImage(self, models, db, uid, password, product_id):
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
             # Créer l'objet Image à partir des bytes
            image = Image.open(io.BytesIO(image_bytes))
            return image
        else:
            print(f"Le produit avec l'ID {product_id} n'a pas d'image.")
    except Exception as e:
        print(f"Erreur lors de l'affichage de l'image du produit : {e}")



#-------------------------------------------------------------------
def getManufOrderToDo(models):
    fields = ['name', 'date_planned_start', 'product_id', 'product_qty', 'qty_producing', 'state']
    limit = 10
    mo_list = models.execute_kw(database, gUid, password,
        'mrp.production', 'search_read',
        [[('state', '=', 'confirmed'), ('qty_produced', '!=', 'product_qty')]],
        {'fields': fields, 'limit': limit}
    )

    if mo_list:
        result_text = ""
        for mo_dico in mo_list:
            result_text += '----------------------------\n'
            for k in mo_dico.keys():
                text = f' - {k} : {mo_dico[k]}\n'
                result_text += text
        return result_text
    else:
        return "Aucun ordre de fabrication trouvé ou une erreur est survenue."



#----------------------------------------------------------------------
    


#--------------------------------------------------------------------,