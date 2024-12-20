# type: ignore[import]
# pyright: ignore[import]
# pylint: disable=import-error
# ruff: noqa: F401, E402
# mypy: ignore-errors
# flake8: noqa: F401



import os
import subprocess
import sys
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

    print(f"Lien {import_name} - {package_name} créé !")


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
        original_name = module_name
        from_imports = (
            lambda imports: [imports] if (t := type(imports)) == str and t != bool
            else [i for i in imports] if t == tuple and t != bool
            else imports
        )(from_imports)
        module_name = (
            lambda name: get_package_name(name) if not (dots := "." in name) 
            else get_package_name((parts := name.split("."))[0])
        )(module_name)

        try:
            if module_name not in sys.modules:
                try:
                    __import__(module_name)
                except:
                    __import__(original_name)
                    module_name = original_name
            
            if (module := sys.modules[module_name]) and (alias_name := (
                original_name.split(".")[-1] if len(original_name.split(".")) > 1 and from_imports == True
                else from_imports if from_imports != True and from_imports != False
                else alias if alias != False else module_name
            )):
                if from_imports == True:
                    caller_globals[alias_name] = module
                elif from_imports != True and from_imports != False:
                    for name in from_imports:
                        caller_globals[name] = getattr(module, name)
                else:
                    raise ValueError("La seconde valeur doit être True ou une liste de noms d'attributs et pas False.")


            
        except ImportError:
            # Tenter l'installation si le module n'existe pas
            print(f"{module_name} non trouvé. Installation en cours...")
            try:
                print(f"Installation de {module_name}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
                print(f"{module_name} installé avec succès.")
            except:
                print(f"Erreur lors de l'installation de {module_name}.")
                print("Vérifiez le nom du module et réessayez.")

                path_lib = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib.json")
                if os.path.exists(path_lib):
                    with open(path_lib, "r") as f:
                        lib = json.load(f)
                        if module_name in (mappings := json.load(open(path_lib))):
                            try:
                                if (result := input("Un lien a été trouvé avec le nom du module, souhaitez-vous réessayer avec le nom associé ? (y/n) : ")).lower() == 'y':
                                    print(f"Installation de {mappings[module_name]}...")
                                    subprocess.check_call([sys.executable, "-m", "pip", "install", mappings[module_name]])
                                    print(f"{mappings[module_name]} installé avec succès.")
                                else:
                                    print("Annulé.")
                            except:
                                print("Erreur lors de l'installation de {mappings[module_name]}.")
                                print("Installation impossible.")
                                print("Veuillez installer manuellement le module.")
            
            # Réessayer l'import après installation
            try:
                if module_name not in sys.modules:
                    try:
                        __import__(module_name)
                    except:
                        __import__(original_name)
                        module_name = original_name
                
                if (module := sys.modules[module_name]) and (alias_name := (
                    original_name.split(".")[-1] if len(original_name.split(".")) > 1 and from_imports == True
                    else from_imports if from_imports != True and from_imports != False
                    else module_name
                )):
                    if from_imports == True:
                        caller_globals[alias_name] = module
                    elif from_imports != True and from_imports != False:
                        for name in from_imports:
                            caller_globals[name] = getattr(module, name)
                    else:
                        raise ValueError("La seconde valeur doit être True ou une liste de noms d'attributs et pas False.")
                    
            except ImportError:
                print(f"Erreur : échec de l'installation de {module_name}")
        except Exception as e:
            print(f"Erreur lors de l'importation de {module_name}: {str(e)}")


def get_package_name(import_name: str) -> str:
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib.json")
    return (lambda: mappings[import_name] 
            if import_name in (mappings := json.load(open(json_path))) 
            else import_name)() if os.path.exists(json_path) else import_name

                
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
        except:
            print(f"Erreur lors de l'installation de {module}.")
            print("Vérifiez le nom du module et réessayez.")

            path_lib = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib.json")
            if os.path.exists(path_lib):
                with open(path_lib, "r") as f:
                    lib = json.load(f)
                    if module in (mappings := json.load(open(path_lib))):
                        try:
                            if (result := input("Un lien a été trouvé avec le nom du module, souhaitez-vous réessayer avec le nom associé ? (y/n) : ")).lower() == 'y':
                                print(f"Installation de {mappings[module]}...")
                                subprocess.check_call([sys.executable, "-m", "pip", "install", mappings[module]])
                                print(f"{mappings[module]} installé avec succès.")
                            else:
                                print("Annulé.")
                        except:
                            print("Erreur lors de l'installation de {mappings[module]}.")
                            print("Installation impossible.")
                            print("Veuillez installer manuellement le module.")



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
        original_name = module_name
        from_imports = (
            lambda imports: [imports] if (t := type(imports)) == str and t != bool
            else [i for i in imports] if t == tuple and t != bool
            else imports
        )(from_imports)


        module_name = (lambda name: get_package_name(name) 
              if "." not in name 
              else get_package_name(name.split(".")[0]))(module_name)


        try:
            if module_name not in sys.modules:
                try:
                    __import__(module_name)
                except:
                    __import__(original_name)
                    module_name = original_name

            if (module := sys.modules[module_name]) and (alias_name := (
                original_name.split(".")[-1] if len(original_name.split(".")) > 1 and from_imports == True
                else from_imports if from_imports != True and from_imports != False
                else module_name
            )):
                if from_imports == True:
                    caller_globals[alias_name] = module
                elif from_imports != True and from_imports != False:
                    for name in from_imports:
                        caller_globals[name] = getattr(module, name)
                else:
                    raise ValueError("La seconde valeur doit être True ou une liste de noms d'attributs et pas False.")



        except Exception as e:
            print(f"Erreur lors de l'importation de {module_name}: {str(e)}")
            print("Vérifiez le nom du module et réessayez.")
            print("Vérifiez si le module est installé.")


def uninstall(*modules) -> None:
    """
    Désinstalle des bibliothèques Python.
    -------------------
    - modules : modules à désinstaller.
    """
    for module in modules:
        original_module_name = module
        module = get_package_name(module)
        try:
            try:
                __import__(module)
            except ImportError:
                module = original_module_name
                __import__(original_module_name)
                
            # If module exists, try to uninstall it
            print(f"Désinstallation de {module}...")
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", module])
            print(f"{module} désinstallé avec succès.")
            
        except ImportError:
            print(f"Le module {module} n'est pas installé ou le nom spécifié est incorrect.")
            
        except subprocess.CalledProcessError:
            print(f"Erreur lors de la désinstallation de {module}.")
            print("Veuillez désinstaller manuellement le module.")


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
        original_name = module_name
        from_imports = (
            lambda imports: [imports] if (t := type(imports)) == str and t != bool
            else [i for i in imports] if t == tuple and t != bool
            else imports
        )(from_imports)

    
        module_name = (lambda name: get_package_name(name) 
              if "." not in name 
              else get_package_name(name.split(".")[0]))(module_name)

    
        try:
            if module_name not in sys.modules:
                __import__(module_name)   
            
            module = sys.modules[module_name]

            if (alias_name := (
                original_name.split(".")[-1] if len(original_name.split(".")) > 1 and from_imports == True
                else from_imports if from_imports != True and from_imports != False
                else original_name
            )):
                if from_imports == True:
                    del caller_globals[alias_name]
                elif from_imports != True and from_imports != False:
                    for name in from_imports:
                        del caller_globals[name]
                else:
                    raise ValueError("La seconde valeur doit être True ou une liste de noms d'attributs et pas False.")

            print(f"{module} enlevé avec succès.")

        except Exception as e:
            print(f"Erreur : {module} n'est pas installé et ne peut pas être enlevé. \n{e}")
            if (result := input("Voulez-vous l'installer ? (y/n) : ")).lower() == 'y':
                install(module)
            else:
                print("Annulé.")




def main():
    if len(sys.argv) == 4 and sys.argv[1] == "add":
        add(sys.argv[2], sys.argv[3])
        print(f"Successfully mapped {sys.argv[2]} to {sys.argv[3]}")

if __name__ == "__main__":
    main()
