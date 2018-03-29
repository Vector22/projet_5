from datetime import datetime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from dbconfig import cfg


DB_URI = 'mysql' + cfg['MYSQL_PYTHON_DRIVER'] + '://' +\
    cfg['MYSQL_USER'] + ':' + cfg['MYSQL_PWD'] + '@' +\
    cfg['MYSQL_HOST'] + ':' + str(cfg['MYSQL_PORT']) + '/' +\
    cfg['MYSQL_DB'] + '?' + 'charset=utf8'
engine = create_engine(DB_URI, encoding='utf-8', echo=False)
Base = declarative_base()

###############################################################


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    url = Column(String(100))

    def __init__(self, name="", url=""):
        self.name = name
        self.url = url

    foods = relationship('Foods', back_populates="categories")


class MyFoods(Base):
    __tablename__ = "myfoods"

    id = Column(Integer, primary_key=True)
    saved_at = Column(Date(), default=datetime.now)
    food_id = Column(Integer, ForeignKey('foods.id'))
    food_substitute_id = Column(Integer, ForeignKey('foods.id'))
    food = relationship('Foods', foreign_keys=[food_id])
    food_substitute = relationship('Foods', foreign_keys=[food_substitute_id])


class Foods(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    url = Column(String(200), nullable=False)
    nutrition_grade = Column(String(2))
    purchase_places = Column(String(200))
    manufacturing_places = Column(String(700))
    countries = Column(String(50), nullable=False)
    ingredients = Column(String(2024))

    categories_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship('Categories', back_populates="foods")

    #myfoods = relationship('MyFoods', back_populates="foods")

    def __repr__(self):
        print("\nName: {}".format(self.name))
        print("Nutrition grade: {}".format(self.nutrition_grade))
        print("Country: {}".format(self.countries))
        if self.purchase_places is not "":
            print("Purchase places: {}\n".format(self.purchase_places))
        if self.manufacturing_places is not "":
            print("Manufacturing place: {}".format(self.manufacturing_places))
        print("\nIngredients: {}\n".format(self.ingredients))
        print("More infos :{}\n\n".format(self.url))

    def __str__(self):
        return """\nName: {}
        \nNutrition grade: {}\nCountry: {}\nPurchase places: {}
        \nManufacturing places: {}\nIngredients: {}
        \nMore infos: {}\n""".format(self.name, self.nutrition_grade,
                                     self.countries, self.purchase_places,
                                     self.manufacturing_places,
                                     self.ingredients, self.url)


# create tables
def create_table():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
