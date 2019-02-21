# nlp-recipe-transformer

This is the second project of EECS-337. The purpose of this project is to learn NLP techniques by scraping and parsing recipes from allrecipes.com.

### Installing
Clone this repo and install packages
```
$ git clone https://github.com/alexr17/nlp-recipe-transformer
$ cd nlp-recipe-transformer/
$ pip3 install -r requirements.txt
```
If you don't have pip you will need to install it.

## Getting Started

...

## Contributing
Look through the assignment on Canvas and accept the invite link sent to you.

Read the description below and ask questions if you don't understand something.

### Structure

This project will have two main components: parsing, and transforming. A third, smaller component will be writing the main program and linking up the main components to create a finished product.

#### Parsing

The parsing file should have a function that takes a url and returns a dict containing the following items in a format like this:
```json
{
    "ingredients": {
        "salt": {
            "quantity": 1,
            "measurement": "tbsp"
        },
        "flour": {
            "quantity": 2,
            "measurement": "cup"
        },
        "sugar": {
            "quantity": 0.5,
            "measurement": "cup"
        }
    },
    "tools": ["whisk", "bowl", "oven"],
    "cooking_methods": {
        "primary": "bake",
        "other": []
    },
    "steps": [
        {
            "description": "blah blah blah",
            "ingredients": {
                "salt": {
                    "quantity": 0.5,
                    "measurement": "tbsp"
                }
            },
            "tools": [],
            "cooking_method": "stirring"
        }
    ]
}
```

You will probably need to use tools like [beautifulsoup](https://pypi.org/project/beautifulsoup4/) to scrape the HTML.

#### Transforming

The transforming of the recipe will occur in the transform file. You should expect to receive an object with the structure above and use that to transform the receipe. The assignment on canvas goes more in depth on transformations.

If you decide to generate any lists or files containing mappings or alternate ingredients, please do so in the data/ folder. Make sure it is something that can be generated programmatically (i.e. an online text file that we can generate by calling a method in the web api file).

#### Main program

The main program should have a user interface that determines what the user wants the program to do. It should call methods in transform and parse to get the recipes/data and print out the recipe(s) in a human-friendly format (to the console).