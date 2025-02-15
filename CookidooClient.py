import requests
import argparse
import os


class CookiputRecipeCreator:
    def __init__(self, jwt_token):
        self.base_url = "https://cookidoo.de"

        self.jwt_token = jwt_token  # The JWT token to include in the 'v-token' header
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "troet",
        }
        self.cookies = {"_oauth2_proxy": jwt_token}

    def create_recipe(self, recipe_name):
        create_recipe_url = f"{self.base_url}/created-recipes/de-DE"
        create_recipe_data = {"recipeName": recipe_name}

        response = requests.post(
            create_recipe_url,
            json=create_recipe_data,
            headers=self.headers,
            cookies=self.cookies,
        )

        if response.status_code == 200:
            recipe_id = response.json().get("recipeId")
            # self.cookies["session"] = response.cookies["session"]
            if recipe_id:
                print(f"Recipe '{recipe_name}' created with ID: {recipe_id}")
                return recipe_id
            else:
                print("Failed to retrieve recipe ID.")
        else:
            print(f"Failed to create the recipe. Status code: {response.status_code}")
        return None

    def rename_recipe(self, recipe_id, new_recipe_name):
        rename_recipe_url = f"{self.base_url}/created-recipes/de-DE/{recipe_id}"
        rename_recipe_data = {"name": new_recipe_name}

        response = requests.patch(
            rename_recipe_url,
            json=rename_recipe_data,
            headers=self.headers,
            cookies=self.cookies,
        )

    def add_ingredients(self, recipe_id, ingredients):
        # Step 2: Add ingredients
        add_ingredients_url = f"{self.base_url}/created-recipes/de-DE/{recipe_id}"
        data = {"ingredients": ingredients}

        response = requests.patch(
            add_ingredients_url, json=data, headers=self.headers, cookies=self.cookies
        )

    def add_hints(self, recipe_id, hints):
        add_hints_url = f"{self.base_url}/created-recipes/de-DE/{recipe_id}"
        data = {"hints": hints}

        response = requests.patch(
            add_hints_url, json=data, headers=self.headers, cookies=self.cookies
        )

    def add_steps(self, recipe_id, steps):
        # Step 3: Add cooking steps
        add_steps_url = f"{self.base_url}/created-recipes/de-DE/{recipe_id}"
        data = {"instructions": steps}

        response = requests.patch(
            add_steps_url, json=data, headers=self.headers, cookies=self.cookies
        )

    def add_tools_and_time(
        self, recipe_id, tools, total_time, prep_time, yield_value, yield_unit
    ):
        # Step 4: Add tools, time, and yield information
        add_tools_time_url = f"{self.base_url}/created-recipes/de-DE/{recipe_id}"
        data = {
            "tools": tools,
            "totalTime": total_time,
            "prepTime": prep_time,
            "yield": {"value": yield_value, "unitText": yield_unit},
        }
        headers = {"v-token": self.jwt_token}

        response = requests.patch(
            add_tools_time_url, json=data, headers=self.headers, cookies=self.cookies
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cookidoo Recipe Uploader")
    parser.add_argument(
        "-jwt", help="JSON Web Token for authenticated access to cookidoo"
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    jwt = args.jwt

    if jwt is None:
        jwt = os.environ.get("COOKIDOO_JWT", None)

    if jwt is None:
        print("No valid access token found. Quitting.")
        exit(-1)

    recipe_creator = CookiputRecipeCreator(jwt)

    # Step 1: Create a new recipe
    recipe_id = recipe_creator.create_recipe("My Awesome New Recipe")

    if recipe_id is None:
        exit(-1)

    # Step 2: Add ingredients
    ingredients = [
        {"type": "INGREDIENT", "text": "My ingredient 1"},
        {"type": "INGREDIENT", "text": "Another delicious ingredient"},
        {"type": "INGREDIENT", "text": "Necessary other stuff"},
    ]
    recipe_creator.add_ingredients(recipe_id, ingredients)

    # Step 3: Add cooking steps
    steps = [
        {"type": "STEP", "text": "Prepare to stew"},
        {"type": "STEP", "text": "Add stuff"},
        {"type": "STEP", "text": "Bakeoff."},
    ]
    recipe_creator.add_steps(recipe_id, steps)

    # Step 4: Add tools, time, and yield information
    tools = ["TM6"]
    total_time = 4200
    prep_time = 3900
    yield_value = 4
    yield_unit = "portion"
    recipe_creator.add_tools_and_time(
        recipe_id, tools, total_time, prep_time, yield_value, yield_unit
    )
