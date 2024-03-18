# Projet POKEFig
Bienvenue dans le fichier d'installation
=================================================================================
Contenu du disque :
=================================================================================
- Procédure d'installation des applications
- Sauvegarde de la base de données accessible via l'application Odoo "backup.zip"
- 2 VM Linux et 1 VM Windows
- 1 dossier Linux contenant : 1 exécutable pour l'installation de la version Python 3.9.2 "Start.sh" et un exécutable pour le lancement de l'application
- 1 dossier Windows contenant : 1 exécutable pour l'installation de la version Python 3.9.2 et un exécutable pour le lancement de l'application
- 1 dossier Odoo qui contient un fichier Start pour le démarrage du Docker et un fichier txt pour la configuration du Docker
================================================================================

Liste des librairies :
- xmlrpc.client
- base64
- PIL : pillow 10.2.0
- math : matplotlib 3.3.4
- io
===================================================================================
 Installation de Python et des bibliothèques : 
===================================================================================
- sudo apt update
- sudo apt install python3.9
- sudo apt-get install python3-pip
- pip install Pillow==10.2.0
- pip install matplotlib==3.3.4
===================================================================================
 Procédure d'installation
===================================================================================
Démarrer les PCs et vérifiez que vous êtes bien connectés au réseau wifi "afpicfai_wifi_guests" récupérez l'adresse IP de chaque ordinateur via l'invite de commande : "ipconfig". Cherchez l'adresse IPV4 de la carte réseau sans fil wifi. Faites ensuite des ping entre les PCs pour tester la communication.

1. Lancement de la VM Odoo 
- Lancer la VM Linux sur le PC Rob21
- Vérifiez si les ports 8069 sont ouverts : Rendez-vous dans l'onglet "périphériques" de la VM -> Réseau -> Réglage réseau -> Advanced -> Redirection des ports. Si aucune règle n'est configurée, veillez en créer une avec le symbole + à droite avec les configurations suivantes : protocole : TCP, port hôte : 8069, port invité : 8069 et validez.
- Lancer le fichier "Start container.sh", il démarrera l'installation de l'image Docker.
- Allez sur le navigateur Firefox et entrez l'URL suivant : http://localhost:9000/
- Connectez-vous avec l'ID : admin; mdp : admin
- Cliquez sur le docker et accédez au tableau de bord (Dashboard). Sur le menu de gauche, rendez-vous dans la section "container list" et lancez les conteneurs en stop.
- Allez ensuite dans un nouvel onglet et entrez l'adresse : 172.31.11.60:8069. Si la base de données "PokeFigDatabase" ne vous est pas proposée, cliquez sur "manage database" puis "Restore Database", là vous pouvez parcourir les dossiers et choisir dans votre disque le fichier "backup.zip". Faites Continuer et c'est bon. Vous pouvez maintenant vous connecter à la base de données avec l'adresse mail "buisson.a@ad.afpi-bretagne.com" et voir que le chargement de Odoo a bien fonctionné.

2. Lancement de l'application sur Linux 
- Lancer la VM Linux sur un des autres PCs.
- Vérifiez si les ports 8069 sont ouverts : Rendez-vous dans l'onglet "périphériques" de la VM -> Réseau -> Réglage réseau -> Advanced -> Redirection des ports. Si aucune règle n'est configurée, veillez en créer une avec le symbole + à droite avec les configurations suivantes : protocole : TCP, port hôte : 8069, port invité : 8069 et validez.
- Allez sur le navigateur Firefox et entrez l'URL : http://172.31.11.60:8069/ pour vous connecter à la base de données. Utilisez l'identifiant : "buisson.a@ad.afpi-bretagne.com" et le mot de passe "Ntm123456789!". Il s'agit d'un test plus formel que le ping pour vérifier si l'on a accès à la base de données en réseau.
- Lancez l'exécutable "Start.sh". Celui-ci lancera automatiquement l'installation de Python 3.9.2 et des bibliothèques nécessaires au fonctionnement du code et lancera ensuite l'application. Si l'application n'est pas lancée automatiquement après les installations, lancez le fichier "CodePageStockage".
- Vous pouvez maintenant dérouler la procédure de test

3. Lancement de l'application sur Windows 
- Lancer la VM Linux sur un des autres PCs.
- Vérifiez si les ports 8069 sont ouverts : Rendez-vous dans l'onglet "périphériques" de la VM -> Réseau -> Réglage réseau -> Advanced -> Redirection des ports. Si aucune règle n'est configurée, veillez en créer une avec le symbole + à droite avec les configurations suivantes : protocole : TCP, port hôte : 8069, port invité : 8069 et validez.
- Allez sur le navigateur Firefox et entrez l'URL : http://172.31.11.60:8069/ pour vous connecter à la base de données. Utilisez l'identifiant : "buisson.a@ad.afpi-bretagne.com" et le mot de passe "Ntm123456789!". Il s'agit d'un test plus formel que le ping pour vérifier si l'on a accès à la base de données en réseau.
- Lancez l'exécutable "Installe.bat". Celui-ci lancera automatiquement l'installation de Python 3.9.2 et des bibliothèques nécessaires au fonctionnement du code et lancera ensuite l'application. Si l'application n'est pas lancée automatiquement après les installations, lancez le fichier "CodePageStockage.exe".
- Vous pouvez maintenant dérouler la procédure de test

=====================================================================================================================
Fonctionnement de l'application 
=====================================================================================================================
Lorsque vous lancez l'application, vous arrivez sur la page de connexion. Là vous devez saisir un ID : "production" sur le PC de production, "logistique" sur le PC de logistique. Vous pouvez saisir un identifiant administrateur "buisson.a@ad.afpi-bretagne.com" pour choisir d'accéder à l'une ou l'autre des applications, le mot de passe : "Ntm123456789!". Il est impératif de saisir l'adresse IP de la VM du PC sur lequel est hébergée l'application Odoo, ce paramètre a été ajouté pour ne pas être handicapé dans le cas où l'adresse IP de l'ordinateur changeait.

1. Application de production 
	L'application de production affiche toutes les informations exigées par le cahier des charges pour chacun des OF confirmé et en cours. Un bouton "modifier" fait apparaître une zone de saisie qui permet de modifier la quantité produite. Dès lors les informations sont immédiatement mises à jour dans la base de données, mais il faut faire une déconnexion et reconnexion pour les voir sur la page.

2. Application logistique 
	L'application logistique affiche les produits en stock avec leurs quantités et leurs prix. En cliquant sur la zone du prix, il est possible de le modifier. Des filtres sont appliqués sur cette page pour permettre de rechercher les produits par nom ou selon un certain ordre.
