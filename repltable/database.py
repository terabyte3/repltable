from typing import List
from replit import Database as rdb


class Database:
    def __init__(self, database: rdb):
        self._db = database

    def __setitem__(self, name: str, value: str) -> None:
        self._db[name] = value

    def __getitem__(self, key: str):
        if key not in self._db.keys():
            self._db[key] = []
        return Table(self._db[key], self, key)

    def __delattr__(self, name: str) -> None:
        if name in self._db.keys():
            del self._db[name]

    def drop(self, table: str):
        """Drops a table from the database.

        Parameters
        ----------
        table : str
            The name of the table to drop.
        """        
        if table in self._db.keys():
            del self._db[table]

class Table:
    """An object representing a table in the database.

    You should not need to create an instance of this class yourself.
    """    
    def __init__(self, docs: List[dict], db: Database, name: str):
        self._documents = docs
        self.db = db
        self.name = name

    def __update_changes(self):
        self.db[self.name] = self._documents

    def get(self, **kwargs):
        """Gets all documents matching the given query.

        Returns
        -------
        list[dict]
            Returns a list of documents matching the given query.
        """
        l = []
        for i in self._documents:
            for key, value in kwargs.items():
                if i[key] == value:
                    l.append(i)
        return l

    def get_one(self, **kwargs):
        """Gets the first document matching the given query.

        Returns
        -------
        dict
            The document found.
        """
        try:
            return self.get(**kwargs)[0]
        except IndexError:
            return None

    def insert(self, data: dict):
        """Insert a new document into the table.

        Parameters
        ----------
        data : dict
            A dictionary containing the data to insert.
        """        
        self._documents.append(data)
        self.__update_changes()

    def update(self, data: dict, **kwargs):
        """Update an existing document in the table.

        Parameters
        ----------
        data : dict
            The new data
        **filters
            Filters that the document must match.
        """        
        for index, doc in enumerate(self._documents):
            for query, ans in kwargs.items():
                if doc[query] == ans:
                    self._documents[index] = data
        self.__update_changes()

    def drop(self):
        """Delete this table.
        """        
        delattr(self.db, self.name)
