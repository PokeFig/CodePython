#######################################################################
######                 Code Fonction Production                 #######
#######################################################################
#                                                                     #
# Version 2.0                                                         #
# Autor : L.P                                                         #
#######################################################################
#======================================================================
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image
import base64 , os, io
import xmlrpc.client
import CodeStockageJardel

#======================================================================

server_ip="172.18.0.1"
server_port=8069
password = "Ntm123456789!"
database = "PokeFigDataBase"

gUrl = f"http://{server_ip}:{server_port}/xmlrpc/2/common" 
common_proxy = xmlrpc.client.ServerProxy(gUrl)
gUid = common_proxy.authenticate("PokeFigDataBase", "paimblancleo@gmail.com", password, {})

#======================================================================

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
        print(result_text)
    else:
        return "Aucun ordre de fabrication trouvé ou une erreur est survenue."



#--------------------------------------------------------------------
        
def createManufOrder(models, quantity, product_id ):
    
    model = 'mrp.production'
   
    values = {
        'product_id': product_id,
        'product_qty': quantity,
    }

    try:
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
        
def DoneManufOrder(models, order_id,product_id,quantity):
    model = 'mrp.production'
    
    values = {
        'state': 'done'
        
    }

    try:
        models.execute_kw(database, gUid, password,
                          model, 'write', [[order_id], values])

        print(f"Ordre de fabrication #{order_id} terminé avec succès.")

        try:
            # Recherche du stock du produit
            stock_Modification_id = models.execute_kw(database, gUid, password,
                                     'stock.quant', 'search',
                                     [[('product_id', '=', product_id)]])
        
            # Modification du stock
            if stock_Modification_id:
                # Extraire l'ID du premier élément de la liste
                stock_id_to_modify = stock_Modification_id[0]
            
                # Obtenir la quantité actuelle du stock
                current_quantity = models.execute_kw(database, gUid, password,
                                                 'stock.quant', 'read',
                                                 [stock_id_to_modify], {'fields': ['quantity']})[0]['quantity']
            
                # Effectuer l'opération d'addition
                new_quantity = current_quantity + quantity
            
                # Mettre à jour la quantité du stock
                models.execute_kw(database, gUid, password,
                              'stock.quant', 'write',
                              [[stock_id_to_modify], {'quantity': new_quantity}])
            
                print(f"Stock du produit avec l'ID {product_id} modifié avec succès.")
            else:
                print(f"Aucun stock trouvé pour le produit avec l'ID {product_id}.")

        except Exception as e:
            print(f"Erreur lors de la modification du stock : {e}")

    except Exception as e:
        print(f"Erreur lors de la terminaison de l'ordre de fabrication: {e}")

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

#--------------------------------------------------------------------
        
def ModifStockage(models,product_id, quantity):                                                        #Fonction pour écriture de la base de données

    try:
        # Recherche du stock du produit
        stock_Modification_id = models.execute_kw(database, gUid, password,
                                     'stock.quant', 'search',
                                     [[('product_id', '=', product_id)]])
        
        # Modification du stock
        if stock_Modification_id:
            # Extraire l'ID du premier élément de la liste
            stock_id_to_modify = stock_Modification_id[0]
            
            # Obtenir la quantité actuelle du stock
            current_quantity = models.execute_kw(database, gUid, password,
                                                 'stock.quant', 'read',
                                                 [stock_id_to_modify], {'fields': ['quantity']})[0]['quantity']
            
            # Effectuer l'opération d'addition
            new_quantity = current_quantity + quantity
            
            # Mettre à jour la quantité du stock
            models.execute_kw(database, gUid, password,
                              'stock.quant', 'write',
                              [[stock_id_to_modify], {'quantity': new_quantity}])
            
            print(f"Stock du produit avec l'ID {product_id} modifié avec succès.")
        else:
            print(f"Aucun stock trouvé pour le produit avec l'ID {product_id}.")

    except Exception as e:
        print(f"Erreur lors de la modification du stock : {e}")

#--------------------------------------------------------------------

def ModifOF(models, order_id, product_qty):
    try:
        # Recherche de l'OF
        of_search_id = models.execute_kw(database, gUid, password,
                                        'mrp.production', 'search',
                                        [[('id', '=', order_id)]])
        
        # Modification de la quantité de l'OF
        if of_search_id:
            # Extraire l'ID du premier élément de la liste
            of_id_to_modify = of_search_id[0]
            
            # Mettre à jour la quantité de l'OF
            models.execute_kw(database, gUid, password,
                              'mrp.production', 'write',
                              [[of_id_to_modify], {'product_qty': product_qty}])
            
            print(f"Quantité de l'OF avec l'ID {order_id} modifiée avec succès.")
            messagebox.showinfo("Succès", "L'OF: {} modifié avec succès".format(order_id))
        else:
            print(f"Aucun OF trouvé avec l'ID {order_id}.")

    except Exception as e:
        print(f"Erreur lors de la modification de l'OF : {e}")