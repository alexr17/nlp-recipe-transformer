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

Our program uses a CLI designed by Alex. It is more comprehensive than the CLI shown in class. It has 4 commands: print, help, transform, and load. The actual commands for the CLI are displayed when the program is run. However to expedite the grading process I've provided examples below (because the CLI is a bit complex).

All that is needed to run the program is ```python3 main.py```.

### CLI Examples
These are the examples for the CLI. Each of the keywords (load, veg, print, cuisine, etc.) has its own shortened macro that is seen when running the CLI or pressing h.
```
load --random (loads and parses a random recipe)
load --number 12345 (loads and parses the recipe with url https://www.allrecipes.com/recipe/12345)
load --url https://www.allrecipes.com/recipe/66666 (loads and parses the recipe with url https://www.allrecipes.com/recipe/66666)

print --parsed --json (prints the loaded recipe in json format)
print --parsed --readable (prints the loaded recipe in readable format)

transform --veg (transforms the loaded recipe to vegetarian)
transform --meat (transforms the loaded recipe to non vegetarian)
transform --healthy (transforms the loaded recipe to healthy)
transform --unhealthy (transforms the loaded recipe to unhealthy)
transform --cuisine --japanese (transforms the loaded recipe to japanese)
transform --cuisine --mediterranean (transforms the loaded recipe to mediterranean)
]transform --cuisine --mexican (transforms the loaded recipe to mexican)
transform --cooking-methods [--fry | --steam | --bake | --grill] (transform the cooking method from one method to another by using any two methods)
transform --kosher (transforms the loaded recipe to kosher)
transform --halal (transforms the loaded recipe to halal)
transform --non-halal (transforms the loaded recipe to non-halal)

print --transformed --json (prints the transformed recipe in json format)
print --transformed --readable (prints the transformed recipe in readable format)

help (prints out the initial message)

quit (quits the cli)
```

## Contributing
Look through the assignment on Canvas and accept the invite link sent to you.

Read the description below and ask questions if you don't understand something.

### Structure

This project will have two main components: parsing, and transforming. A third, smaller component will be writing the main program and linking up the main components to create a finished product.

#### Parsing

The parsing file should have a function that takes a url and returns a dict containing the following items in a format like this:
```json
{
  "title": "pineapple enchiladas",
  "ingredients": {
    "fruit": [
      {
        "quantity": 1,
        "measurement": "20 ounce can",
        "ingredient": "pineapple",
        "descriptors": [
          "crushed"
        ]
      }
    ],
    "herb": [],
    "vegetable": [],
    "condiment": [
      {
        "quantity": 1,
        "measurement": "10 ounce can",
        "ingredient": "enchilada sauce",
        "descriptors": [
          "divided"
        ]
      }
    ],
    "carb": [
      {
        "quantity": 6,
        "measurement": "8 inch",
        "ingredient": "flour tortillas",
        "descriptors": []
      }
    ],
    "binder": [
      {
        "quantity": 0.25,
        "measurement": "cup",
        "ingredient": "sour cream",
        "descriptors": []
      }
    ],
    "primary_protein": [],
    "secondary_protein": [
      {
        "quantity": 2,
        "measurement": "cups",
        "ingredient": "cheddar cheese",
        "descriptors": [
          "shredded",
          "divided"
        ]
      }
    ],
    "tertiary_protein": []
  },
  "steps": [
    {
      "ingredients": [],
      "tools": [
        "oven"
      ],
      "methods": [
        "preheat"
      ],
      "times": [],
      "temperature": [
        "375 degrees F",
        "190 degrees F"
      ],
      "raw_step": "preheat oven to 375  degrees f (190 degrees c)."
    },
    {
      "ingredients": [
        "pineapple",
        "cream",
        "cheese"
      ],
      "tools": [
        "bowl"
      ],
      "methods": [
        "combine"
      ],
      "times": [],
      "temperature": [],
      "raw_step": "in a medium bowl combine pineapple, sour cream and 1 cup cheese."
    },
    {
      "ingredients": [],
      "tools": [],
      "methods": [
        "pour"
      ],
      "times": [],
      "temperature": [],
      "raw_step": "pour 1/4 cup enchilada sauce in the bottom of a 9 x 13 inch baking dish."
    },
    {
      "ingredients": [
        "pineapple",
        "cheese"
      ],
      "tools": [],
      "methods": [
        "pour",
        "sprinkle"
      ],
      "times": [],
      "temperature": [],
      "raw_step": "fill tortillas with pineapple mixture, roll and place in baking dish.  pour on remaining enchilada sauce and sprinkle with remaining cheese."
    },
    {
      "ingredients": [],
      "tools": [
        "oven"
      ],
      "methods": [
        "bake"
      ],
      "times": [
        "30 minutes"
      ],
      "temperature": [],
      "raw_step": "bake, covered, in preheated oven for 30 minutes."
    }
  ],
  "tools": [
    "bowl",
    "oven"
  ],
  "methods": {
    "primary_methods": [
      "bake",
      "preheat"
    ],
    "secondary_methods": [
      "combine",
      "sprinkle",
      "pour"
    ]
  }
}
```

You will probably need to use tools like [beautifulsoup](https://pypi.org/project/beautifulsoup4/) to scrape the HTML.

#### Transforming

The transforming of the recipe will occur in the transform file. You should expect to receive an object with the structure above and use that to transform the receipe. The assignment on canvas goes more in depth on transformations.

If you decide to generate any lists or files containing mappings or alternate ingredients, please do so in the data/ folder. Make sure it is something that can be generated programmatically (i.e. an online text file that we can generate by calling a method in the web api file).

#### Main program

The main program should have a user interface that determines what the user wants the program to do. It should call methods in transform and parse to get the recipes/data and print out the recipe(s) in a human-friendly format (to the console).
