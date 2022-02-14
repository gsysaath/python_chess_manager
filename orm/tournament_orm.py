from orm.orm import ORM
from models.tournament import Tournament


tournaments = ORM(item_type=Tournament)
