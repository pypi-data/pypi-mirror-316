"""
MutableMapping interface for the database.

The term _Database is used to follow the naming convention of the Python Shelve module, even though it is not mandatory.
"""
from logging import Logger
from collections.abc import MutableMapping
from concurrent.futures import ThreadPoolExecutor

from ._data_processing import DataProcessing
from .provider_interface import ProviderInterface
from ._flag import can_create, can_write, clear_db
from .exceptions import (
    CanNotCreateDBError,
    DBDoesNotExistsError,
    DBDoesNotExistsError,
)


__all__ = ["_Database"]


class _Database(MutableMapping):
    """
    Wrapper around the ProviderInterface to provide a MutableMapping interface with the Shelf business logic.
    """

    def __init__(
        self,
        logger: Logger,
        db: ProviderInterface,
        flag: str,
        data_processing: DataProcessing,
    ) -> None:
        super().__init__()
        self.data_processing = data_processing
        self.db = db
        self.flag = flag
        self.logger = logger

    def __getitem__(self, key: bytes) -> bytes:
        """
        Retrieve the value associated with the key from the database.
        """
        value = self.db.get(key)
        return self.data_processing.apply_post_processing(value)

    @can_write
    def __setitem__(self, key: bytes, value: bytes) -> None:
        """
        Set the value associated with the key in the database.
        """
        value = self.data_processing.apply_pre_processing(value)
        self.db.set(key, value)

    @can_write
    def __delitem__(self, key: bytes) -> None:
        """
        Delete the key from the database.
        """
        self.db.delete(key)

    def __iter__(self):
        """
        Iterate over the keys in the database.
        """
        yield from self.db.iter()

    def __len__(self) -> int:
        """
        Return the number of elements in the database.
        """
        return self.db.len()

    def close(self) -> None:
        """
        Close the database.
        """
        self.db.close()

    def sync(self) -> None:
        """
        Sync the database.
        """
        self.db.sync()

    def _init(self):
        """
        Initialize the database by:
        - Creating the database if it doesn't exist and the flag allows it.
        - Clearing the database if the flag allows it.
        """
        if not self.db.exists():
            self.logger.info(f"Database doesn't exists.")
            if can_create(self.flag):
                self.logger.info(f"Creating the database...")
                try:
                    self.db.create()
                except Exception as e:
                    self.logger.critical(f"Can't create the database.")
                    raise CanNotCreateDBError("Can't create database.") from e
                self.logger.info(f"Database created.")
            else:
                self.logger.critical(f"Can't create the database")
                raise DBDoesNotExistsError("Database does not exist.")
        else:
            # If the database exists, but the flag parameter indicates that it should be cleared, clear it.
            if clear_db(self.flag):
                self.logger.info(f"Purging the database...")
                # Retrieve all the keys and delete them.
                # Retrieving keys is quick, but deletion synchronously is slow, so we use threads to speed up the process.
                with ThreadPoolExecutor() as executor:
                    list(executor.map(self.db.delete, self.db.iter()))
                self.logger.info(f"Database purged.")
