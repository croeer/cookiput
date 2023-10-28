import requests
from bs4 import BeautifulSoup
import re

class ChefkochRecipeScraper:
    def __init__(self):
        self.base_url = "https://www.chefkoch.de"
    
    def scrape_recipe(self, recipe_url):
        url = f"{self.base_url}{recipe_url}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            recipe = {
                'title': soup.find('h1', class_='').text.strip(),
                'ingredients': [],
                'instructions': [],
                # 'instructions': [step.text.strip() for step in soup.find_all('p', class_='instruction')],

            }
            
            ingredients_table = soup.find('table', class_='ingredients')
            if ingredients_table:
                rows = ingredients_table.find_all('tr')
                for row in rows:
                    columns = row.find_all('td')
                    if len(columns) == 2:
                        ingredient_quantity = re.sub("\s+", " ", columns[0].span.text.strip())
                        ingredient_name = columns[1].span.text.strip()
                        recipe['ingredients'].append(f"{ingredient_quantity} {ingredient_name}")
            
            return recipe
        else:
            raise Exception(f"Failed to fetch recipe from {url}. Status code: {response.status_code}")

# Example usage:
if __name__ == "__main__":
    scraper = ChefkochRecipeScraper()
    recipe_url = "/rezepte/1247411229689036/Pizza-Baellchen.html"  # Replace with the URL of the recipe you want to scrape
    
    try:
        recipe = scraper.scrape_recipe(recipe_url)
        print("Recipe Title:", recipe['title'])
        print("Ingredients:")
        for ingredient in recipe['ingredients']:
            print("- " + ingredient)
        print("Instructions:")
        for i, step in enumerate(recipe['instructions'], 1):
            print(f"{i}. {step}")
    except Exception as e:
        print(f"Error: {str(e)}")
