"""DataBaseOperation functions.

DataBase operations.
"""
import logging

from faunadb import query as q
from faunadb.client import FaunaClient
from faunadb.objects import Ref
from faunadb.errors import BadRequest


logging.basicConfig(
    level=logging.DEBUG, format=" %(asctime)s - %(levelname)s - %(message)s"
)


class DataBaseOperationFunctions:
    """DataBase Operation Functions.

    Authentication and secrets from Hashicorp Vault.
    Vault credentials used to retrieve twilio settings.
    input: client_token - from vault data
    input_type: str
    """

    def __init__(self, client_token: str) -> None:
        """Init class - vars are called in the function as needed."""
        self.client_token = client_token

    def __repr__(self) -> str:  # pragma: no cover
        """Display function name using repr."""
        class_name = self.__class__.__name__
        return f"{class_name}"

    def get_fauna_connection(self) -> FaunaClient:
        """Get Fauna Connection.

        input: client_token from class
        input_type: str
        output: fauna database connection
        output_type: FaunaClient
        """
        try:
            client = FaunaClient(secret=self.client_token)
            return client
        except Exception as _errorinfo:  # pragma: no cover
            raise ValueError("error connecting") from _errorinfo

    def fauna_read_database(self) -> FaunaClient:
        """Read from fauna database."""
        client = self.get_fauna_connection()
        indexes = client.query(q.paginate(q.indexes()))
        return indexes

    def fauna_write_database(self) -> FaunaClient:
        """Write to fauna database.
        2020-09-16 00:01:01,436 - DEBUG -
        {'ref': Ref(id=froglegs01_new, collection=Ref(id=databases)),
        'ts': 1599661067450000, 'name': 'froglegs01_new', 'global_id': 'yxku95xzgydbg'
        """
        client = self.get_fauna_connection()
        database = "froglegs01_new"
        try:
            new = client.query(q.delete(q.database(database)))
            return new

        except (BadRequest, Exception) as _error:  # pragma: no cover
            raise ValueError(
                "Fauna error."
            ) from _error


            # try:
            #     query = client.query(q.create_database({"name": database}))
            #     return query
            # except:  # pragma: no cover
        #     #     raise ValueError(f"Can't create database {database}")
        # except:  # pragma: no cover
        #     raise ValueError(f"Can't delete database {database}")
