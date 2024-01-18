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
import base64
import io
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
            
            # Créer l'objet PhotoImage à partir des bytes
            #tk_image = tk.PhotoImage(data=image_bytes)
             # Créer l'objet Image à partir des bytes
            image = Image.open(io.BytesIO(image_bytes))
            tk_image = ImageTk.PhotoImage(image)



            # Afficher l'image dans une fenêtre Tkinter
            label = tk.Label(self, image=tk_image)
            label.pack(padx=10, pady=10)
            self.update_idletasks()
        else:
            print(f"Le produit avec l'ID {product_id} n'a pas d'image.")
    except Exception as e:
        print(f"Erreur lors de l'affichage de l'image du produit : {e}")



#-------------------------------------------------------------------



#----------------------------------------------------------------------
    


#--------------------------------------------------------------------