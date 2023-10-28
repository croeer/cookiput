# cookiput

Create custom cookidoo recipes via API call

## API calls to create a recipe

First do a POST to the `created-recipes` endpoint:

```
POST /created-recipes/de-DE HTTP/2

{"recipeName":"My Awesome New Recipe"}
```

This will return the `recipeId` of the newly created recipe. You can then update the content of the recipe via PATCH requests to the `created-recipes/${recipeId}` enpoint.

### Adding ingredients

To add ingredients use a PATCH request to `created-recipes/${recipeId}`:

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

Adding steps for cooking is analogous to adding ingredients, use a PATCH request to `created-recipes/${recipeId}`:

```json
{
  "instructions": [
    { "type": "STEP", "text": "Prepare to stew" },
    { "type": "STEP", "text": "Add stuff" },
    { "type": "STEP", "text": "Bakeoff." }
  ]
}
```
