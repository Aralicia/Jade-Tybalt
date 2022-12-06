from inspect import isclass
from os import environ
from dotenv import load_dotenv
from sqlitedict import SqliteDict
import sqlite3

class DataStore:
    
    def __init__(self, store):
        self._store = store
        self.cache = {}
        pass

    def __call__(self, key):
        return self.load(key)

    def load(self, key):
        if not isinstance(key, str):
            if isinstance(key, int) or (isinstance(key, float) and key.is_integer()):
                key = str(abs(key))
            else :
                if not isclass(key):
                    key = key.__class__
                module = key.__module__
                if (module is None):
                    key = key.__name__
                else:
                    key = module + '.' + key.__name__
        if key not in self.cache:
            self.cache[key] = self._store(key)
        return self.cache[key]

    def clear(self):
        self.cache = {}


class Config:
    _env_loaded = False

    def __init__(self, group):
        self.group = group
        if group == "env":
            if Config._env_loaded == False:
                load_dotenv()
                Config._env_loaded = True
        else:
            self.dict = SqliteDict("data/config/{}.sqlite3".format(group))
            pass

    def get(self, key):
        if self.group == "env":
            return environ.get(key)
        else:
            try:
                return self.dict[key]
            except KeyError:
                return None

    def set(self, key, value):
        if self.group == "env":
            pass # cannot set env
        else:
            self.dict[key] = value
            self.dict.commit()


class Data:

    def __init__(self, group):
        self.group = group
        self.db = sqlite3.connect("data/sqlite/{}.sqlite3".format(group))
        pass

    def table(self, table_name, columns):
        query = "CREATE TABLE IF NOT EXISTS {} ({})";
        if isinstance(columns, dict):
            columns = [" ".join((k, v)) for k,v in columns.items()]
        if not isinstance(columns, list):
            raise TypeError("columns must be a list or dictionary")
        query = query.format(table_name, ', '.join(columns))
        self.db.execute(query)
        self.db.commit()


