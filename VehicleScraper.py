import requests
from bs4 import BeautifulSoup
import re
from scraper_methods import get_html


class VehicleScraper:
   
    def __init__(self, base_urls):
        self.base_urls = base_urls

    def scrape_vehicles(self, url, page):
        html_content = get_html(f"{url}&page={page}")
        if html_content is None:
            return []

        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            vehicles = []
            

            for article in soup.find_all('article', class_='cldt-summary-full-item'):
                price = self._extract_price(article)
                transmission = self._extract_transmission(article)
                mileage = self._extract_mileage(article)
                fuel = self._extract_fuel(article)
                power = self._extract_power(article)
                evaluation_count = self._extract_evaluation_count(article)
                version = self._extract_version_element(article)
                seller = self._extract_seller_name_element(article)
                car_name_version = self._extract_car_name_version(article)
                date=self._extract_date(article)

                vehicles.append((price, transmission, version, mileage, fuel, power, evaluation_count, seller, car_name_version,date))
                

            return vehicles
        
        except Exception as e:
            print(f"Erreur de parsing sur la page {page} de l'URL {url}: {e}")
            return []
        
    
    


    def _extract_price(self, article):
        price_element = article.find('p', class_='Price_price__APlgs')
        if price_element and "€" in price_element.get_text():
            return price_element.get_text(strip=True).split(',')[0]
        else:
            super_deal_element = article.find('span', class_='SuperDeal_highlightContainer__R8edU')
            if super_deal_element and "€" in super_deal_element.get_text():
                return super_deal_element.get_text(strip=True).split(',')[0]
            else:
                return "Prix non disponible"

    def _extract_transmission(self, article):
        detail_elements = article.find_all('span', class_='VehicleDetailTable_item__4n35N')
        for detail in detail_elements:
            if 'Boîte' in detail.get_text(strip=True):
                return detail.get_text(strip=True)
        return "Boite non disponible"

    def _extract_mileage(self, article):
        detail_elements = article.find_all('span', class_='VehicleDetailTable_item__4n35N')
        for detail in detail_elements:
            if 'km' in detail.get_text(strip=True):
                return detail.get_text(strip=True)
        return "Kilométrage non disponible"

    def _extract_fuel(self, article):
        detail_elements = article.find_all('span', class_='VehicleDetailTable_item__4n35N')
        for detail in detail_elements:
            if "svg#nozzle" in str(detail):
                return detail.get_text(strip=True)
        return "Fuel non disponible"

    def _extract_power(self, article):
        detail_elements = article.find_all('span', class_='VehicleDetailTable_item__4n35N')
        for detail in detail_elements:
            if 'kW' in detail.get_text(strip=True):
                return detail.get_text(strip=True)
        return "Puissance non disponible"
    
    def _extract_date(self, article):
        date_elements = article.find_all('span', class_='VehicleDetailTable_item__4n35N')
        for date_element in date_elements:
            if 'svg#calendar' in str(date_element):
                return date_element.get_text(strip=True)
        return "Date non disponible"


           
    def _extract_evaluation_count(self, article):
        evaluation_element = article.find('span', class_='BlackStars_wrapper__stcae')
        if evaluation_element:
            evaluation_text = evaluation_element.next_sibling
            if evaluation_text:
                match = re.search(r'\((\d+)\)', evaluation_text)
                if match:
                    return int(match.group(1))
        return "Évaluations non disponibles"

    def _extract_version_element(self, article):
        version_element = article.find('span', class_='ListItem_version__5EWfi')
        return version_element.get_text(strip=True) if version_element else "Version non disponible"

    def _extract_car_name_version(self, article):
        a_tag = article.find('a', class_='ListItem_title__ndA4s')
        return a_tag.find('h2').get_text(strip=True) if a_tag and a_tag.find('h2') else "Nom de la voiture non disponible"

    def _extract_seller_name_element(self, article):
        seller_name_element = article.find("span", class_="SellerInfo_address__leRMu")
        return seller_name_element.get_text(strip=True) if seller_name_element else "Nom du vendeur non disponible"
    

    

    

    def scrape_multiple_pages(self, url, num_pages):
        all_vehicles = []
        for page in range(1, num_pages + 1):
            vehicles = self.scrape_vehicles(url, page)
            all_vehicles.extend(vehicles)
        return all_vehicles

    def scrape_all_urls(self, num_pages_per_url):
        vehicles_by_model = {}
        for url in self.base_urls:
            model = self._extract_model_from_url(url) 
            vehicles = self.scrape_multiple_pages(url, num_pages_per_url)
            if model not in vehicles_by_model:
                vehicles_by_model[model] = []
            vehicles_by_model[model].extend(vehicles)
        return vehicles_by_model

        
    
    def _extract_model_from_url(self, url):
        
        match = re.search(r'/lst/([^/?]+)', url)
        if match:
            return match.group(1)  
        return "Unknown"


