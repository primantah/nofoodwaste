import json
from fuzzywuzzy import process  # type: ignore
import spacy  # type: ignore

# Load spaCy's medium language model
nlp = spacy.load("en_core_web_md")

# Load the recipes from JSON
def load_recipes():
    with open('recipes.json', 'r') as f:
        return json.load(f)

# Preprocess ingredients to handle plurals
def preprocess_ingredient(ingredient):
    doc = nlp(ingredient.lower())
    # Use lemmatization to get singular forms (e.g., eggs -> egg)
    return " ".join([token.lemma_ for token in doc])

# Use FuzzyWuzzy to match user ingredients with recipe ingredients
def find_similar_ingredients(user_ingredients, recipe_ingredients):
    preprocessed_user_ingredients = {preprocess_ingredient(ingredient) for ingredient in user_ingredients}
    similar_ingredients = set()
    
    for ingredient in recipe_ingredients:
        processed_ingredient = preprocess_ingredient(ingredient)
        # Fuzzy match for approximate string matching
        match, score = process.extractOne(processed_ingredient, preprocessed_user_ingredients)
        if score > 70:  # Use 70% as a similarity threshold
            similar_ingredients.add(ingredient)
    
    return similar_ingredients

# Find possible meals based on the ingredients available
def find_possible_meals(user_ingredients, recipes):
    preprocessed_user_ingredients = {preprocess_ingredient(ingredient) for ingredient in user_ingredients}
    possible_meals = {}
    
    for i, recipe in enumerate(recipes, start=1):
        recipe_ingredients = recipe['ingredients']
        
        # Get fuzzy matches between user ingredients and recipe ingredients
        matched_ingredients = find_similar_ingredients(preprocessed_user_ingredients, recipe_ingredients)
        match_ratio = len(matched_ingredients) / len(recipe_ingredients)

        # Include only recipes for which all ingredients are matched
        if match_ratio == 1.0:  # Full match
            possible_meals[i] = recipe

    return possible_meals

# Display recipe details for a selected meal
def get_recipe_details(selected_recipe):
    print(f"\nRecipe for {selected_recipe['name']}:")
    print("Ingredients:")
    for ingredient in selected_recipe['ingredients']:
        print(f" - {ingredient}")
    
    # Print the predefined instructions from the JSON
    print("\nInstructions:")
    print(selected_recipe['instructions'])

def nofoodwaste():
    # Load recipes from the JSON file
    recipes = load_recipes()
    
    while True:
        # Step 1: Receive ingredients input
        ingredients_input = input("Enter ingredients left in the fridge, separated by commas (or type 'quit' to exit): ")
        if ingredients_input.lower() in ["quit", "exit", "0"]:
            print("Exiting the program. Goodbye!")
            break
        ingredients = [ingredient.strip().lower() for ingredient in ingredients_input.split(',')]

        # Step 2: Find possible meals
        meal_options = find_possible_meals(ingredients, recipes)
        
        if meal_options:
            # Display available meals
            print("Here are some meals you can make with the available ingredients:")
            for i, meal in meal_options.items():
                print(f"{i}. {meal['name']}")

            while True:
                # Step 3: Let the user select a meal
                choice = input("\nSelect a meal number to see the recipe (or type '0' to return to main menu): ")
                if choice.lower() in ["quit", "exit", "0"]:
                    break
                try:
                    choice = int(choice)
                    selected_recipe = meal_options.get(choice)
                    if selected_recipe:
                        get_recipe_details(selected_recipe)
                        # Options after viewing a recipe
                        while True:
                            action = input("\nEnter 1 to return to main menu, 2 to view another recipe, or 0 to quit: ")
                            if action == "1":
                                break  # Return to the main menu
                            elif action == "2":
                                # Show available meals again without asking for ingredients
                                print("\nHere are some meals you can make with the available ingredients:")
                                for i, meal in meal_options.items():
                                    print(f"{i}. {meal['name']}")
                                break  # Re-run the meal selection loop to allow another choice
                            elif action in ["0", "quit", "exit"]:
                                print("Exiting the program. Goodbye!")
                                return  # Exit the entire program
                            else:
                                print("Invalid input. Please enter 1, 2, or 0.")
                        break  # Exit meal selection loop to main menu
                    else:
                        print("Invalid choice. Please select a valid meal number.")
                except ValueError:
                    print("Please enter a valid meal number.")
        else:
            print("No recipes found with the available ingredients. Try entering different ingredients.")

# Run the program
nofoodwaste()
