from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists
from random import randrange

from tabledef import engine, Categories, Foods, MyFoods

from filldb import *


def showStartMenu():
    """display the start menu"""
    print("\n1: Replace a food")
    print("2: Show the saved foods")
    print("0: Quit\n")


def getStartMenuChoice():
    """take the user start menu choice"""
    choice = None
    ok = False
    while(not ok):
        try:
            choice = int(input("Enter your choice :"))
        except ValueError:
            print("The number entered is wrong...")

        if (choice in (1, 2, 0)):
            ok = True
        else:
            print("The choice must be a number within 1, 2 or 0")
            ok = False
    return choice


#section show registre
def showSavedFoodsMenu():
    print("\n1: Show the simple list (foods names)")
    print("2: Show the detailled list (all foods informations)")
    print("0: Back to start")


#section replace a food
def showCategoryMenuChoice():
    print("\n1: Select a category")
    print("2: Back to start")
    print("0: Quit\n")


def getCategoryMenuChoice():
    ok = False
    choice = None
    while(not ok):
        try:
            choice = int(input("Do your choice :"))
        except ValueError:
            print("The number entered is wrong...")

        if (choice in (1, 2, 0)):
            ok = True
        else:
            print("The choice must be a number within 1, 2 or 0")
            ok = False
    return choice


#sub menu select a category
def showCategoriesList(engine):
    """display the list of all categories"""
    #connect to the db
    connection = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    #query the db about categories
    for category in session.query(Categories):
        print("{} : {}".format(category.id, category.name))

    connection.close()


def getCategoryNumberChoice(maxCategories):
    """take the user category choosen"""
    ok = False
    choice = None
    while (not ok):
        try:
            choice = int(input("Enter the category number: "))
        except ValueError:
            print("The number entered is wrong")

        if(choice in range(1, maxCategories)):
            ok = True
        else:
            print("Please, the number must be in 1 to {}\n".
                  format(maxCategories))
            ok = False
    return choice


#sub sub menu select a food

def makePage(data):
    """Function that permit to slice all the foods of categorie
    by table of 20 """
    nbPage = data.count() // 20
    if data.count() % 20 is not 0:
        nbPage += 1
    if data.count() < 20:
        nbPage = 1
    first, last, step, pageList = 0, 20, 20, list()
    for i in range(nbPage):
        if i is not (nbPage - 1):
            #intermediary page
            pageList.append(data[first: last])
        else:
            #the last page
            pageList.append(data[first:])  # append the data left
        first += step
        last += step
    return pageList


def printFoods(pageList, pageNum):
    print("=" * 50)
    for elt in pageList[pageNum - 1]:
        print("{}: {}".format(elt.id, elt.name))
    print(" " * 40, end=" ")
    print("Page {} on {}".format(pageNum, len(pageList)))
    print("=" * 50)


def showFoodsMenu():
    print("\n1: Choose a food on this page")
    print("2: Visit another page")
    print("0: Quit\n")


def showFoodsMenu2():
    print("\n1: Choose a food")
    print("0: Quit\n")


def getFoodsMenuChoice():
    ok = False
    while(not ok):
        try:
            choice = int(input("Do your choice :"))
        except ValueError:
            print("The number entered is wrong...")

        if (choice in (1, 2, 0)):
            ok = True
        else:
            print("The choice must be a number within 1, 2 or 0")
            ok = False
    return choice


def getFoodsMenuChoice2():
    ok = False
    while(not ok):
        try:
            choice = int(input("Do your choice :"))
        except ValueError:
            print("The number entered is wrong...")

        if (choice in (1, 0)):
            ok = True
        else:
            print("The choice must be a number within 1, 2 or 0")
            ok = False
    return choice


def getFoodsPage(maxPage):
    ok = False
    choice = None
    while (not ok):
        try:
            choice = int(input("Enter the page number: "))
        except ValueError:
            print("The number entered is not an integer")

        if(choice in range(1, maxPage+1)):
            ok = True
        else:
            print("This page do not exist, please try again")
            ok = False
    return choice


def getFoodsNumber(maxFoods):
    ok = False
    choice = None
    while (not ok):
        try:
            choice = int(input("Enter the food number: "))
        except ValueError:
            print("The number entered is not an integer")

        if(choice > 0 and choice <= maxFoods):
            ok = True
        else:
            print("Number must be positive; try again")
            ok = False
    return choice


def chooseFood(engine, categoryNumber, maxFoods):
    #connect to the db
    connection = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    #query the db about foods of given category
    foodsAll = session.query(Foods).filter(Foods.categories_id ==
                                           categoryNumber)
    #slice the result in multiple pages
    pageList = makePage(foodsAll)
    #print the first food page of the category
    printFoods(pageList, 1)
    #display the food menu
    showFoodsMenu()
    #take the user choice
    foodsMenuChoice = getFoodsMenuChoice()

    if(foodsMenuChoice is 1):
        #choose a food on the first page
        foodNumber = getFoodsNumber(maxFoods)
        #query the db about this food id
        if session.query(exists().where(Foods.id == foodNumber)).scalar():
            food = session.query(Foods).filter(Foods.id == foodNumber).first()
            print(food)
            #display a subtitute of the food
            print("Here is a substitute:")
            #query the db about foods on the same category
            #where nutrion grade are better than the selected food
            if bool(session.query(Foods).
                    filter(Foods.nutrition_grade <= food.nutrition_grade).
                    filter(Foods.categories_id == categoryNumber)):
                subFoods = session.query(Foods).\
                    filter(Foods.categories_id == categoryNumber).\
                    filter(Foods.nutrition_grade <= food.nutrition_grade).all()
                subFoodIndex = randrange(len(subFoods))
                subFood = subFoods[subFoodIndex]
                print(subFood)
                addInDb = input("Save the food ? (y/n)")
                if(addInDb in ("Y", "y")):
                    myFood = MyFoods()
                    myFood.food_id = food.id
                    myFood.food_substitute_id = subFood.id

                    session.add(myFood)
                    print("Food saved...")
                    session.commit()
                else:
                    print("Food not saved !")
            else:
                print("No better substitute found...")
    elif(foodsMenuChoice is 2):
        #choose a food on other page
        otherPage, choice = True, None
        while(otherPage):
            foodPage = getFoodsPage(len(pageList))
            printFoods(pageList, foodPage)
            choice = input("\nOther page ? (y/n):")
            if choice in ("Y", "y"):
                otherPage = True
            else:
                otherPage = False
        showFoodsMenu2()
        foodsMenuChoice2 = getFoodsMenuChoice2()
        if(foodsMenuChoice2 is 1):
            #choose a food on the selected page
            foodNumber = getFoodsNumber(maxFoods)
            #query the db about this food id
            if session.query(exists().where(Foods.id == foodNumber)).scalar():
                food = session.query(Foods).filter(Foods.id == foodNumber).first()
                print(food)
                #display a subtitute of the food
                print("Here is a substitute:")
                #query the db about foods on the same category
                #where nutrion grade are better than the selected food
                if bool(session.query(Foods).
                        filter(Foods.nutrition_grade <= food.nutrition_grade).
                        filter(Foods.categories_id == categoryNumber)):
                    subFoods = session.query(Foods).\
                        filter(Foods.categories_id == categoryNumber).\
                        filter(Foods.nutrition_grade <= food.nutrition_grade)
                    subFoodIndex = randrange(len(subFoods.all()))
                    subFood = subFoods.all()[subFoodIndex]
                    print(subFood)
                    addInDb = input("Save the two foods ? (y/n)")
                    if(addInDb in ("Y", "y")):
                        myFood = MyFoods()
                        myFood.food_id = food.id
                        myFood.food_substitute_id = subFood.id

                        session.add(myFood)
                        session.commit()

                        print("Food saved...")
                    else:
                        print("Food not saved !")
                else:
                    print("No better substitute found...")
        else:
            print("Returning to the start...\n")
    else:
        print("Returning to the start...\n")
    #close the connection
    connection.close()


def showFavoritesFoods(engine, detailled=False):
    connection = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    #query the db about favorites foods saved
    q = session.query(Foods).join(MyFoods.food).all() +\
        session.query(Foods).join(MyFoods.food_substitute).all()
    for food in q:
        print("-" * 50)
        if(detailled):
            print(food)
        else:
            print(food.name)
        print("-" * 50)
    connection.close()


def run():
    MAX_FOODS = maxFoods()
    print("\n\nAliments total : {}\n\n".format(MAX_FOODS))
    mainLoop = True
    while(mainLoop):
        subLoop = True
        showStartMenu()
        startMenuChoice = getStartMenuChoice()
        while(subLoop):
            if(startMenuChoice is 1):
                showCategoriesList(engine)
                showCategoryMenuChoice()
                categoryMenuChoice = getCategoryMenuChoice()
                if(categoryMenuChoice is 1):
                    categoryNumber = getCategoryNumberChoice(MAX_FOODS_CAT)
                    chooseFood(engine, categoryNumber, MAX_FOODS)
                else:
                    #go back to the start menu
                    subLoop = False
            elif(startMenuChoice is 2):
                sectionLoop = True
                while(sectionLoop):
                    showSavedFoodsMenu()
                    choice = getStartMenuChoice()
                    if choice is 1:
                        print("\n\nYour favorites foods name list : \n")
                        showFavoritesFoods(engine)
                    elif choice is 2:
                        print("\n\nYour favorites foods list detailled :\n")
                        showFavoritesFoods(engine, True)
                    else:
                        sectionLoop = False
                        subLoop = False
            else:
                print("Bye...")
                subLoop = False
                mainLoop = False
