import json
from typing import Any, Callable

from tinydb import TinyDB
from tinydb.table import Document


class ORM:
    """
        CRUD methods for any item type into tinyDB
    """

    def __init__(self, item_type: Any):
        """ Initializer of ORM, creates table from dict """
        self.collection: dict = {}
        db = TinyDB('db.json', indent=4)
        self.table = db.table(item_type.__name__.lower() + 's')
        # self.max_id = 0
        self.item_type = item_type
        for data in self.table:
            self.create(**data)

    def create(self, *args, save=False, **kwargs):
        """ Create item, initialize id and save in db """
        if 'id' not in kwargs:
            # kwargs['id'] = self.max_id + 1
            kwargs['id'] = self.get_next_id()
        item = self.item_type(*args, **kwargs)
        self.collection[item.id] = item
        if save:
            self.save_item(item.id)
        # self.max_id = max(item.id, self.max_id)
        return item

    def save_item(self, id: int):
        """ Save item in database """
        item = self.find_by_id(id)
        self.table.upsert(Document(json.loads(item.json()), doc_id=id))

    def find_by_id(self, id: int):
        """ Find item in database by id """
        return self.collection[id]

    def find_all(self):
        """ Returns all item from item_type in database """
        return list(self.collection.values())

    def find(self, filter_key: Callable = lambda x: True, sort_key: Callable = lambda x: x.id):
        """ Return a single item from list of items"""
        return sorted(filter(filter_key, self.find_all()), key=sort_key)

    def get_next_id(self):
        """ Initialize item id in database """
        try:
            return sorted(self.table.all(), key=lambda x: x['id'])[-1]["id"] + 1
        except IndexError:
            return 1
