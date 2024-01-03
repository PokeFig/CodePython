#######################################################################
######                 Code Login odoo + profile                #######
#######################################################################
#                                                                     #
# Version 1.0                                                         #
# Autor : B.A                                                         #
#######################################################################

#################################################
# Vérification de la bonne connection Prog/odoo #
#################################################

#==========================================================
# Fonction Block Connexion
#==========================================================

import xmlrpc.client

EnterPassword = "Ntm123456789!"                                                                    #VARIABLE JARDEL POUR LE MOT DE PASSE
EnterEmail = "buisson.a@ad.afpi-bretagne.com"                                                      #VARIABLE JARDEL POUR MAIL OU IDENTIFIANT


#Gestion des identifiants serveurs
server_ip = "172.31.10.65"                                                                         #IP de connection du serveur Odoo
server_port = 8069                                                                                 #Port de dconnection du serveur Odoo
data_base = "PokeFigDataBase"                                                                      #Nom du conteneur dans Odoo
password = EnterPassword                                                                           #Gestion du mot de passe
Email = EnterEmail                                                                                 #Gestion de l'identifiant


def ConnectionCheck():                                                                             #Fonction block check Connection serveur Odoo
    urlOdoo = f"http://{server_ip}:{server_port}/xmlrpc/2/common"                                  #Génération du lien pour la connection de Odoo
    try:
        common_proxy = xmlrpc.client.ServerProxy(urlOdoo)                                          #Connection au serveur avec le lien
        uid = common_proxy.authenticate(data_base, "buisson.a@ad.afpi-bretagne.com", password, {}) #Connection au profile
    