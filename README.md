# NoFoodWaste Recipe Finder

NoFoodWaste is a Python-based recipe finder designed to help reduce food waste by allowing you to make the most of the ingredients you already have. Simply input the ingredients in your fridge, and the program will suggest recipes that you can make using only those items.

## Features

- **Exact Ingredient Matching**: Only recipes that can be fully prepared with the given ingredients are displayed.
- **Natural Language Processing**: Uses spaCy for ingredient lemmatization, handling variations like plurals (e.g., "eggs" vs. "egg").
- **Fuzzy Matching**: Uses FuzzyWuzzy for approximate string matching, allowing for small spelling differences.
- **Flexible Input Options**: Type 'quit' or '0' at any point to exit the program.

## Technologies Used

- **Python**: Main programming language for the application logic.
- **spaCy**: Used for NLP-based ingredient processing to handle variations.
- **FuzzyWuzzy**: Implements fuzzy matching for similar ingredient names.
- **JSON**: Stores recipes in a flexible, easy-to-edit format.

## Project Files

- **`recipes.json`**: Contains a list of recipes with ingredients and instructions.
- **`nofoodwaste.py`**: Main Python script that runs the NoFoodWaste program.
