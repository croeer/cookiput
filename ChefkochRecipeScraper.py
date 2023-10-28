import requests
import argparse
from bs4 import BeautifulSoup
import re

class ChefkochRecipeScraper:
    def __init__(self):
        self.base_url = "https://www.chefkoch.de"
    
    def is_valid_div(self, element):
        return (
            element.name == "div" and
            element.get("class") == ["ds-box"] and
            all(tag.name == "br" and not tag.find_all() for tag in element.find_all("br")) and
            not any(tag for tag in element.find_all() if tag.name != "br")
        )

    def scrape_recipe(self, recipe_url):
        url = recipe_url
        if not recipe_url.startswith("https"):
            url = f"{self.base_url}{recipe_url}"

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            recipe = {
                'title': soup.find('h1', class_='').text.strip(),
                'ingredients': [],
                'instructions': [],
                'totaltime': "",
            }
            
            timestr = soup.find('span', class_='recipe-preptime').text.replace('\ue192', '').replace('\n', '').replace('Min.','').strip()
            recipe['totaltime'] = 60*int(timestr)

            ingredients_table = soup.find('table', class_='ingredients')
            if ingredients_table:
                rows = ingredients_table.find_all('tr')
                for row in rows:
                    columns = row.find_all('td')
                    if len(columns) == 2:
                        ingredient_quantity = re.sub("\s+", " ", columns[0].text.strip())
                        ingredient_name = columns[1].text.strip()
                        recipe['ingredients'].append(f"{ingredient_quantity} {ingredient_name}")
            
            instruction_divs = soup.find_all(self.is_valid_div)

            # Parse the instruction divs
            for div in instruction_divs:
                text = div.get_text(separator=" ").strip()
                parts = text.split("\n")
                
                for part in parts:
                    if part.strip() == "":
                        continue
                    recipe['instructions'].append(part.strip())
                                    
            return recipe
        
        else:
            raise Exception(f"Failed to fetch recipe from {url}. Status code: {response.status_code}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chefkoch.de Recipe Scraper")
    parser.add_argument("url", help="URL of the chefkoch recipe to scrape")

    # Parse the command-line arguments
    args = parser.parse_args()

    scraper = ChefkochRecipeScraper()
    
    try:
        recipe = scraper.scrape_recipe(args.url)
        print("Recipe Title:", recipe['title'])
        print("est. total time (s): ", recipe['totaltime'])
        print("Ingredients:")
        for ingredient in recipe['ingredients']:
            print("- " + ingredient)
        print("Instructions:")
        for i, step in enumerate(recipe['instructions'], 1):
            print(f"{i}. {step}")
    except Exception as e:
        print(f"Error: {str(e)}")
