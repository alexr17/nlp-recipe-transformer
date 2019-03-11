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
