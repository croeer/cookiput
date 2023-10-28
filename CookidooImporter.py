import requests
import argparse
import os

from CookidooClient import CookiputRecipeCreator
from ChefkochRecipeScraper import ChefkochRecipeScraper

parser = argparse.ArgumentParser(description="Cookidoo Importer")
parser.add_argument("-jwt", help="JSON Web Token for authenticated access to cookidoo")
parser.add_argument("url", help="URL to import recipe from")

# Parse the command-line arguments
args = parser.parse_args()

url = args.url
jwt = args.jwt

if jwt is None:
    jwt = os.environ.get("COOKIDOO_JWT", None)

if jwt is None:
    print("No valid access token found. Quitting.")
    exit(-1)

scraper = ChefkochRecipeScraper()

# Get Recipe
print(f"Downloading recipe from {url}")
try:
    recipe = scraper.scrape_recipe(url)

except Exception as e:
    print(f"Error: {str(e)}")

recipe_creator = CookiputRecipeCreator(jwt)

# Step 1: Create a new recipe
recipe_id = recipe_creator.create_recipe(recipe['title'])

if recipe_id is None:
    exit(-1)

# Step 2: Add ingredients
ingredients = []
for ingredient in recipe['ingredients']:
    ingredients.append({"type": "INGREDIENT", "text": ingredient})
recipe_creator.add_ingredients(recipe_id, ingredients)

# Step 3: Add cooking steps
steps = []
for step in recipe['instructions']:
    steps.append({"type": "STEP", "text": step})
recipe_creator.add_steps(recipe_id, steps)

# Step 4: Add tools, time, and yield information
tools = ["TM6"]
total_time = recipe['totaltime']
yield_value = 1
yield_unit = "portion"
recipe_creator.add_tools_and_time(recipe_id, tools, total_time, total_time, yield_value, yield_unit)
