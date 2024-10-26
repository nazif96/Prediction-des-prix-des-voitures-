from VehicleScraper import VehicleScraper
import json 

urls = ["https://www.autoscout24.be/fr/lst/audi/q8?atype=C&cy=B&desc=0&page=2&search_id=d02l2savys&sort=standard&source=listpage_pagination&ustate=N%2CU",
    "https://www.autoscout24.be/fr/lst/mercedes-benz/amg-gt?atype=C&cy=B&desc=0&page=2&search_id=10bn92h8pa9&sort=standard&source=listpage_pagination&ustate=N%2CU",
    "https://www.autoscout24.be/fr/lst/ferrari?atype=C&cy=B&desc=0&page=2&search_id=14wd9qzswyz&sort=standard&source=listpage_pagination&ustate=N%2CU",
    "https://www.autoscout24.be/fr/lst/fiat?atype=C&cy=B&desc=0&page=2&search_id=pjx2grc3pk&sort=standard&source=listpage_pagination&ustate=N%2CU",
    "https://www.autoscout24.be/fr/lst/lamborghini?atype=C&cy=B&desc=0&page=2&search_id=axg9g87orw&sort=standard&source=listpage_pagination&ustate=N%2CU",
    "https://www.autoscout24.be/fr/lst/porsche?atype=C&cy=B&desc=0&page=2&search_id=5mzy996q0y&sort=standard&source=listpage_pagination&ustate=N%2CU",
    "https://www.autoscout24.be/fr/lst/toyota?atype=C&cy=B&desc=0&page=2&search_id=77ml6rywei&sort=standard&source=listpage_pagination&ustate=N%2CU",
    "https://www.autoscout24.be/fr/lst/ford?atype=C&cy=B&desc=0&page=2&search_id=bvlivgoq3x&sort=standard&source=listpage_pagination&ustate=N%2CU",
    "https://www.autoscout24.be/fr/lst/mercedes-benz/s-63-amg?atype=C&cy=B&desc=0&page=2&search_id=ggq9zs2xux&sort=standard&source=listpage_pagination&ustate=N%2CU",
    "https://www.autoscout24.be/fr/lst/volkswagen?atype=C&cy=B&desc=0&page=2&search_id=e64lrst65d&sort=standard&source=listpage_pagination&ustate=N%2CU",
    "https://www.autoscout24.be/fr/lst/bentley?atype=C&cy=B&desc=0&page=2&search_id=zbgrlds0jf&sort=standard&source=listpage_pagination&ustate=N%2CU",
    "https://www.autoscout24.be/fr/lst?atype=C&cy=B&desc=0&fuel=E%2C2%2C3&page=2&powertype=kw&search_id=kjtcxizazf&source=listpage_pagination",
    "https://www.autoscout24.be/fr/lst/renault?atype=C&cy=B&desc=0&page=2&search_id=6vyj1lpkpv&sort=standard&source=listpage_pagination&ustate=N%2CU",
    "https://www.autoscout24.be/fr/lst/land-rover?atype=C&cy=B&desc=0&page=2&search_id=ciwm09dqsg&sort=standard&source=listpage_pagination&ustate=N%2CU",


]
    
scraper = VehicleScraper(urls)
vehicles_by_model = scraper.scrape_all_urls(10)

import csv

# Ouvrez le fichier CSV en mode écriture ('w') avec l'encodage 'utf-8'
with open('vehicules.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Modèle', 'Prix', 'Transmission', 'Version', 'Kilométrage', 'Carburant', 'Puissance', 'Évaluations', 'Vendeur', 'Nom de la Voiture',"Date"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for model, vehicles in vehicles_by_model.items():
        for vehicle in vehicles:
            row_data = {
                'Modèle': model,
                'Prix': vehicle[0],
                'Transmission': vehicle[1],
                'Version': vehicle[2],
                'Kilométrage': vehicle[3],
                'Carburant': vehicle[4],
                'Puissance': vehicle[5],
                'Évaluations': vehicle[6],
                'Vendeur': vehicle[7],
                'Nom de la Voiture': vehicle[8],
                "Date": vehicle[9],
            }
            writer.writerow({key: value.encode('utf-8', 'ignore').decode('utf-8') if isinstance(value, str) else value for key, value in row_data.items()})

# ... (votre code pour collecter et organiser les données va ici)

# Sérialisez les données en JSON
with open('vehicules.json', 'w', encoding='utf-8') as json_file:
     json.dump(vehicles_by_model, json_file, ensure_ascii=False, indent=4)



# Le fichier CSV est automatiquement fermé lorsque vous sortez de la déclaration 'with'


