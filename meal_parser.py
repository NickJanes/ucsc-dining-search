from html.parser import HTMLParser

class MenuItem:
    name = "No Name"
    meal = "No Meal"

    def __init__(self, name, meal):
        self.name = name
        self.meal = meal

    def __str__(self):
        return self.meal + ": " + self.name

class MealParser(HTMLParser):
    dataInc = 0
    meals = []
    meal = ""

    def handle_starttag(self, tag, attrs):
        if len(attrs) == 0:
            return

        if attrs[0][0] == "class":
            c = attrs[0][1]
            if c == "shortmenurecipes":
                self.dataInc = 1
            elif c == "shortmenumeals":
                self.dataInc = 2

    def handle_data(self, data):
        data = data.strip()
        if(len(data) == 0):
            return

        if self.dataInc == 1:
            self.meals.append((self.meal, data))
        elif self.dataInc == 2:
            self.meal = data
            
        self.dataInc = 0

    def load(self):
        return self.meals

    def reset_meals(self):
        self.meals = []

    def print(self):
        for meal in self.meals:
            print(meal)