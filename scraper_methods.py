import requests
import json

def get_html(url):
    """Envoie une requête GET à l'URL spécifiée et renvoie le contenu HTML."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Erreur lors de la requête à {url}: {e}")
        return None

def save_to_json(data, filename):
    """Sauvegarde des données dans un fichier JSON."""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        




