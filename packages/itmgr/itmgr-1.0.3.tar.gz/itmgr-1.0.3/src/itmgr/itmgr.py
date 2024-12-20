# type: ignore[import]
# pyright: ignore[import]
# pylint: disable=import-error
# ruff: noqa: F401, E402
# mypy: ignore-errors
# flake8: noqa: F401



import os
import importlib
import subprocess
import sys
import builtins
from pkg_resources import working_set
import pkg_resources
import json

def add(import_name: str, package_name: str) -> None:
    """
    Adds a mapping between import name and package name to lib.json
    
    Args:
        import_name: The name used in imports (e.g. 'cv2')
        package_name: The actual package name for pip (e.g. 'opencv-python')
    """
    # Get the directory where itmgr.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "lib.json")
    
    # Load existing mappings or create new dict
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            mappings = json.load(f)
    else:
        mappings = {}
    
    # Add both directional mappings
    mappings[import_name] = package_name
    mappings[package_name] = import_name
    
    # Save updated mappings
    with open(json_path, "w") as f:
        json.dump(mappings, f, indent=4)


def install_and_import(*modules: list[tuple[str, bool | list[str] | str | tuple[str], bool | str]]) -> None:
    """
    Installe et importe des bibliothèques selon les instructions fournies.

    `modules`: Liste de tuples contenant les informations pour chaque bibliothèque.
    
    Chaque tuple doit être de la forme : (nom_installation, mode_importation, alias ou False)

        - nom_installation : nom pour pip install

        - mode_importation : True pour "from module import attr", str ou list[str] ou tuple[str] pour "from module import attr"

        - alias : False pour pas d'alias ou str pour alias avec "as ..."
    """
    
    caller_globals = sys._getframe(1).f_globals
    
    for module_tpl in modules:
        module_name, from_imports, alias = module_tpl
        from_imports = [from_imports] if type(from_imports) == str and type(from_imports) != bool else \
            [i for i in from_imports] if type(from_imports) == tuple and type(from_imports) != bool \
                else from_imports

        try:
            if module_name not in sys.modules:
                __import__(module_name)   
            
            module = sys.modules[module_name]

            if alias is False:
                if len(module_name.split(".")) > 1 and from_imports == True:
                    alias = module_name.split(".")[-1]
                elif from_imports != True and from_imports != False:
                    alias = from_imports  # Utilise le nom du module comme alias par défaut
                else:
                    alias = module_name

            if from_imports == True:
                # Ajouter le module lui-même à l'espace de noms global avec l'alias
                caller_globals[alias] = module

            elif from_imports != True and from_imports != False:
                # Importer des éléments spécifiques
                for name in from_imports:
                    caller_globals[name] = getattr(module, name)
            else:
                raise ValueError("La seconde valeur doit être True ou une liste de noms d'attributs et pas False.")
            
        except ImportError:
            # Tenter l'installation si le module n'existe pas
            print(f"{module_name} non trouvé. Installation en cours...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
            
            # Réessayer l'import après installation
            try:
                if module_name not in sys.modules:
                    __import__(module_name)   
                
                module = sys.modules[module_name]

                if alias is False:
                    if len(module_name.split(".")) > 1 and from_imports == True:
                        alias = module_name.split(".")[-1]
                    elif from_imports != True and from_imports != False:
                        alias = from_imports  # Utilise le nom du module comme alias par défaut
                    else:
                        alias = module_name

                if from_imports == True:
                    # Ajouter le module lui-même à l'espace de noms global avec l'alias
                    caller_globals[alias] = module

                elif from_imports != True and from_imports != False:
                    # Importer des éléments spécifiques
                    for name in from_imports:
                        caller_globals[name] = getattr(module, name)
                else:
                    raise ValueError("La seconde valeur doit être True ou une liste de noms d'attributs et pas False.")
            except ImportError:
                print(f"Erreur : échec de l'installation de {module_name}")
        except Exception as e:
            print(f"Erreur lors de l'importation de {module_name}: {str(e)}")


def get_package_name(import_name: str) -> str:
    """Returns the correct pip package name for a given import name"""
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib.json")
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            mappings = json.load(f)
            for i in mappings.key():
                if import_name == i:
                    return mappings[i]
                
def install(*modules) -> None:
    """
    Installe des bibliothèques Python en utilisant pip.
    -------------------
    - modules : modules à installer.
    """
    for module in modules:
        try:
            print(f"Installation de {module}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            print(f"{module} installé avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'installation de {module}: {str(e)}")


def importation(*modules : tuple[str, bool | list[str] | str | tuple[str], bool | str]) -> None:
    """
    Importe des bibliothèques Python.
    -------------------
    modules : modules à importer contenant :

        - module : nom du module à importer
        - mode : True pour "import module", str ou list[str] ou tuple[str] pour "from module import attr"
        - alias : False pour pas d'alias ou str pour alias avec "as ..."
    """
    caller_globals = sys._getframe(1).f_globals


    for module_tpl in modules:
        module_name, from_imports, alias = module_tpl
        from_imports = [from_imports] if type(from_imports) == str and type(from_imports) != bool else \
            [i for i in from_imports] if type(from_imports) == tuple and type(from_imports) != bool \
                else from_imports

        try:
            if module_name not in sys.modules:
                __import__(module_name)                

            module = sys.modules[module_name]
            
            if alias is False:
                if len(module_name.split(".")) > 1 and from_imports == True:
                    alias = module_name.split(".")[-1]
                elif from_imports != True and from_imports != False:
                    alias = from_imports  # Utilise le nom du module comme alias par défaut
                else:
                    alias = module_name

            if from_imports == True:
                # Ajouter le module lui-même à l'espace de noms global avec l'alias
                caller_globals[alias] = module

            elif from_imports != True and from_imports != False:
                # Importer des éléments spécifiques
                for name in from_imports:
                    caller_globals[name] = getattr(module, name)
            else:
                raise ValueError("La seconde valeur doit être True ou une liste de noms d'attributs et pas False.")

        except Exception as e:
            print(f"Erreur lors de l'importation de {module_name}: {str(e)}")


def uninstall(*modules) -> None:
    """
    Désinstalle des bibliothèques Python.
    -------------------
    - modules : modules à désinstaller.
    """
    for module in modules:
        print(f"Désinstallation de {module}...")
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", module])
        print(f"{module} désinstallé avec succès.")


def remove_module(*modules) -> None:
    """
    Enlève des bibliothèques Python dans le programme actuel.
    -------------------
    modules : tuple du module à enlever sous la forme :

        - nom_module : nom du module

        - mode_importation : True pour "from module import attr", str ou list[str] ou tuple[str] pour "from module import attr"

        - alias : False pour pas d'alias ou str pour alias avec "as ..."
    """
    
    caller_globals = sys._getframe(1).f_globals
    
    for module_tpl in modules:
        module_name, from_imports, alias = module_tpl
        from_imports = [from_imports] if type(from_imports) == str and type(from_imports) != bool else \
            [i for i in from_imports] if type(from_imports) == tuple and type(from_imports) != bool \
                else from_imports
    
    try:
            if module_name not in sys.modules:
                __import__(module_name)   
            
            module = sys.modules[module_name]

            if alias is False:
                if len(module_name.split(".")) > 1 and from_imports == True:
                    alias = module_name.split(".")[-1]
                elif from_imports != True and from_imports != False:
                    alias = from_imports  # Utilise le nom du module comme alias par défaut
                else:
                    alias = module_name

            if from_imports == True:
                # Ajouter le module lui-même à l'espace de noms global avec l'alias
                 del caller_globals[alias]

            elif from_imports != True and from_imports != False:
                # Importer des éléments spécifiques
                for name in from_imports:
                    del caller_globals[name]
            else:
                raise ValueError("La seconde valeur doit être True ou une liste de noms d'attributs et pas False.")

            print(f"{module} enlevé avec succès.")
    except Exception as e:
        print(f"Erreur : {module} n'est pas installé et ne peut pas être enlevé. \n{e}")
        result = input("Voulez-vous l'installer ? (y/n) : ")
        install(module) if result.lower() == 'y' else print("Annulé.")


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "add":
        add(sys.argv[2], sys.argv[3])
        print(f"Successfully mapped {sys.argv[2]} to {sys.argv[3]}")

if __name__ == "__main__":
    main()
