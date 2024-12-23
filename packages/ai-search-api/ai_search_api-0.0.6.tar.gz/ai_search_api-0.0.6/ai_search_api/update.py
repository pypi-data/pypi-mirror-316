import os
import shutil
import subprocess
import random
from requests import get
import no_search.update

# Funzione per scaricare il contenuto del file main.py da GitLab e salvarlo in database.txt
def api_data():
    url_to_copy_page = "https://gitlab.com/neopad/api/-/raw/main/data/data.json"
    
    # Esegui una richiesta GET per ottenere il contenuto dal sito GitLab
    response = get(url_to_copy_page)
    
    # Verifica che la richiesta sia stata eseguita con successo
    if response.status_code == 200:
        print("Richiesta riuscita.")
        
        # Estrai il contenuto della pagina come oggetto JSON
        page_content = response.json()  # Usa .json() per convertire il contenuto in un dizionario
        
        print("Content Updated: " + str(page_content))
        
        # Restituisci il valore della chiave "version" nel dizionario
        return page_content["version"]
    else:
        print(f"Failed request")
        return None  # In caso di errore, restituisci None

# Chiama la funzione per ottenere la versione dall'API
data_api = api_data()
if data_api:
    print(f"Versione ottenuta: {data_api}")
else:
    print("Impossibile ottenere la versione.")

# Funzione per eliminare una cartella, se esiste
def elimina_cartella(cartella):
    if os.path.exists(cartella):
        print(f"Eliminando la cartella esistente: {cartella}")
        shutil.rmtree(cartella)

# Funzione per clonare il repository e copiare la cartella books
def clone_and_copy_books(repo_url, dest_dir):
    # Elimina la cartella books se esiste
    elimina_cartella(dest_dir)

    # Nome temporaneo della cartella di clonazione
    temp_dir = f"temp_repo/{data_api}"

    # Clona il repository GitLab nella cartella temporanea
    print("Clonando il repository...")
    subprocess.run(["git", "clone", repo_url, temp_dir])

    # Verifica che la cartella books esista nel repository clonato
    books_dir = os.path.join(temp_dir, "books")
    if os.path.exists(books_dir):
        print("Copiando la cartella 'books' nella destinazione...")
        shutil.copytree(books_dir, dest_dir)
    else:
        print("Errore: la cartella 'books' non esiste nel repository.")

# URL del repository GitLab
repo_url = "https://gitlab.com/neopad/api.git"  # URL del repository
dest_dir = "books"  # Cartella di destinazione locale

# Esegui la funzione per clonare e copiare i file
if data_api:  # Assicurati che la versione sia stata ottenuta con successo
    clone_and_copy_books(repo_url, dest_dir)
else:
    print("Impossibile proseguire con il processo di clonazione senza una versione valida.")
