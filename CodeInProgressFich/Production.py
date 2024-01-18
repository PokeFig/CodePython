#######################################################################
######                 Code Fonction Production                 #######
#######################################################################
#                                                                     #
# Version 2.0                                                         #
# Autor : L.P                                                         #
#######################################################################
#======================================================================

import base64, os


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

#-------------------------------------------------------------------

def SaveProductImage(models, db, uid, password, product_id, save_path="/home/user/Documents/clone/CodePython/CodeInProgressFich/"):
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

            # Construire le chemin complet pour enregistrer l'image dans le dossier spécifié
            file_path = os.path.join(save_path, image_name + '.png')

            # Sauvegarder l'image au format '.png' sur le disque
            with open(file_path, 'wb') as file:
                file.write(image_bytes)

            print(f"L'image du produit avec l'ID {product_id} a été sauvegardée dans {image_name}.png")
        else:
            print(f"Aucune image trouvée pour le produit avec l'ID {product_id}")

    except Exception as e:
        print(f"Erreur lors de la sauvegarde de l'image : {e}")

#----------------------------------------------------------------------
    
def getManufOrderToDo(models):
    fields = ['name', 'date_planned_start', 'product_id', 'product_qty', 'qty_producing', 'state']
    limit = 10
    mo_list = models.execute_kw(
        database, gUid,
        'mrp.production', 'search_read',
        [[('state', '=', 'confirmed'), ('qty_produced', '!=', 'product_qty')]],
        {'fields': fields, 'limit': limit}
    )

    if mo_list:
        for mo_dico in mo_list:
            print(f'----------------------------')
            for k in mo_dico.keys():
                print(f' - {k} : {mo_dico[k]}')
    else:
        print("Aucun ordre de fabrication trouvé ou une erreur est survenue.")

#--------------------------------------------------------------------
        
def createManufOrder(models, quantity, product_id ):
    
    model = 'mrp.production'
    
    
   
    values = {
        'product_id': product_id,
        'product_qty': quantity,
    }

    try:
        # Créez l'ordre de fabrication
        order_id = models.execute_kw(database, gUid, password,
                                     model, 'create', [values])

        print(f"Ordre de fabrication créé avec succès. ID: {order_id}  et {quantity} produits à fabriqué")

    except Exception as e:
        print(f"Erreur lors de la création de l'ordre de fabrication: {e}")

#--------------------------------------------------------------------
        
def confirmManufOrder(models, order_id):
    model = 'mrp.production'

    values = {
        'state': 'confirmed',
    }

    try:
        models.execute_kw(database, gUid, password,
                          model, 'write', [[order_id], values])

        print(f"Ordre de fabrication #{order_id} confirmé avec succès.")

    except Exception as e:
        print(f"Erreur lors de la confirmation de l'ordre de fabrication: {e}")

#--------------------------------------------------------------------
        
def DoneManufOrder(models, order_id,qty_produced):
    model = 'mrp.production'

    values = {
        'qty_produced': qty_produced,
        'state': 'done',
    }

    try:
        models.execute_kw(database, gUid, password,
                          model, 'write', [[order_id], values])

        print(f"Ordre de fabrication #{order_id} terminé avec succès.")

    except Exception as e:
        print(f"Erreur lors de la finalisation de l'ordre de fabrication: {e}")

#--------------------------------------------------------------------
        
def CancelManufOrder(models, order_id):
    model = 'mrp.production'

    values = {
        'state': 'cancel',
    }

    try:
        models.execute_kw(database, gUid, password,
                          model, 'write', [[order_id], values])

        print(f"Ordre de fabrication #{order_id} annulé avec succès.")

    except Exception as e:
        print(f"Erreur lors de l'annualtion de l'ordre de fabrication: {e}")

  