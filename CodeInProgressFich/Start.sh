#!/bin/bash

# Fonction pour vérifier si un package Python est installé
function is_python_package_installed() {
    python3 -c "import $1" >/dev/null 2>&1
}

# Fonction pour vérifier la version d'un package Python
function python_package_version() {
    python3 -c "import $1; print($1.__version__)" 2>/dev/null
}

# Vérifier si Python 3.9.2 est déjà installé
if ! is_python_package_installed "sys"; then
    # Télécharger et installer Python 3.9.2
    echo "Installation de Python 3.9.2..."
    # Ajoutez ici vos étapes d'installation de Python
fi

# Vérifier si Pillow version 10.2 est déjà installé
if ! is_python_package_installed "PIL" || [ "$(python_package_version PIL)" != "10.2" ]; then
    # Installer Pillow version 10.2
    echo "Installation de Pillow version 10.2..."
    python3 -m pip install pillow==10.2
fi

# Vérifier si Tkinter est déjà installé
if ! is_python_package_installed "tkinter"; then
    # Installer Tkinter
    echo "Installation de Tkinter..."
    sudo apt-get install python3-tk
fi

# Lancer le script Python
echo "Lancement du script Python..."
python3 CodePageStockage
