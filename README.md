# cookiput

Import chefkoch recipes to cookidoo via API call

## Getting started

Log in to cookidoo and get the auth token from the `v-token` cookie (F12 in most current browsers). This token needs to either be given as `-jwt` command line parameter or exported as an environment variable called `COOKIDOO_JWT`.

```bash
export COOKIDOO_JWT=eyXXXXXXX.....
python CookidooImporter.py https://www.chefkoch.de/......html
```

## Usage

```bash
python CookidooImporter.py -h
usage: CookidooImporter.py [-h] [-jwt JWT] url

Cookidoo Importer

positional arguments:
  url         URL to import recipe from

options:
  -h, --help  show this help message and exit
  -jwt JWT    JSON Web Token for authenticated access to cookidoo
```

## Developer access

Each class can be used on its own to just download recipe data or to import the recipe to cookidoo, so other recipe homepages should be easy to scrape with a custom importer.

## API calls to create a recipe

First do a POST to the `created-recipes` endpoint:

```
POST /created-recipes/de-DE HTTP/2

{"recipeName":"My Awesome New Recipe"}
```

This will return the `recipeId` of the newly created recipe. You can then update the content of the recipe via PATCH requests to the `created-recipes/de-DE/${recipeId}` enpoint.

### Adding ingredients

To add ingredients use a PATCH request to `created-recipes/de-DE/${recipeId}`:

```json
{
  "ingredients": [
    { "type": "INGREDIENT", "text": "My ingredient 1" },
    { "type": "INGREDIENT", "text": "Another delicious ingredient" },
    { "type": "INGREDIENT", "text": "Neccessary other stuff" }
  ]
}
```

### Adding steps

Adding steps for cooking is analogous to adding ingredients, use a PATCH request to `created-recipes/de-DE/${recipeId}`:

```json
{
  "instructions": [
    { "type": "STEP", "text": "Prepare to stew" },
    { "type": "STEP", "text": "Add stuff" },
    { "type": "STEP", "text": "Bakeoff." }
  ]
}
```

### Adding tools, time etc.

To add supported tools and needed time ranges use a PATCH request to `created-recipes/de-DE/${recipeId}`:

```json
{
  "tools": ["TM6"],
  "totalTime": 4200,
  "prepTime": 3900,
  "yield": { "value": 4, "unitText": "portion" }
}
```

The times are in seconds, i.e. 3900s is one hour (3600s) and 5 minutes (300s).
