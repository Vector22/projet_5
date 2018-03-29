from sqlalchemy.orm import sessionmaker
import requests

from tabledef import engine, Categories, Foods

#define the maximun number of categories to request
MAX_FOODS_CAT = 10
#define the max page per foods categories to request
#One categories can be composed of many many foods...
MAX_FOODS_PAGES = 5


def present(cle, table):
    """function that checks if elements belong to
    the keys of a dictionary"""
    resultat = True
    for i in cle:
        if i in table.keys():
            pass
        else:
            resultat = False
            break  # sort de la boucle
    return resultat


def fill_table():
    global MAX_FOODS
    connection = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    #geting categories objects from openfoodfacts
    url = "https://fr.openfoodfacts.org/categories.json"
    r = requests.get(url)
    categories = r.json()

    #index required to add a food in the db
    required_index = ("product_name_fr", "url", "nutrition_grade_fr",
                      "purchase_places", "manufacturing_places", "countries",
                      "ingredients_text")

    #insert the elts in the db
    for i in range(MAX_FOODS_CAT):
        cat = Categories()
        cat.name = categories['tags'][i]['name']
        cat.url = categories['tags'][i]['url']
        session.add(cat)
        session.commit()

        #insert foods for each category
        tab_url = list()  # the page url liste table
        tab_url = [cat.url + '/' + str(ind) + '.json' for ind in
                   range(1, MAX_FOODS_PAGES+1)]

        #add each aliment that respect the norme
        for j in range(len(tab_url)):
            foods_url = tab_url[j]
            #do the request
            r2 = requests.get(foods_url)
            foods = r2.json()

            #loop on each aliment of the page
            for k in range(20):
                #verify if the aliment keys contains the
                #required index
                if present(required_index, foods['products'][k]):
                    #add the food to the foods table
                    food = Foods()
                    food.categories_id = cat.id
                    food.name = foods['products'][k]['product_name_fr']
                    food.url = foods['products'][k]['url']
                    food.nutrition_grade = foods['products'][k]['nutrition_grade_fr']
                    food.purchase_places = foods['products'][k]['purchase_places']
                    food.manufacturing_places = foods['products'][k]['manufacturing_places']
                    food.countries = foods['products'][k]['countries']
                    #delete the eventual en: at begin of country name
                    food.countries.replace("en:", "")
                    food.ingredients = foods['products'][k]['ingredients_text']

                    session.add(food)
            session.commit()
        #commit the total foods added
        session.commit()
    #message to the user
    print("\nWarnings !!! Database initialized...\n")

    #close the connection
    connection.close()


def maxFoods():
    """Function that return the total foods numbers
    saved in the db"""
    connection = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    #take the total number of registered foods
    MAX_FOODS = session.query(Foods).count()
    #close the connection
    connection.close()
    return MAX_FOODS
