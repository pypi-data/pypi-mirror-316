import typing
from typing import Optional

if typing.TYPE_CHECKING:
    from sema4ai.actions._action_context import DataContext

    from sema4ai.data._data_server_connection import DataServerConnection
    from sema4ai.data._result_set import ResultSet


class ConnectionNotSetupError(Exception):
    """
    Exception raised when the connection to the data server is not setup.
    """


class _ConnectionHolder:
    _connection: Optional["DataServerConnection"] = None

    @classmethod
    def connection(cls) -> "DataServerConnection":
        if _ConnectionHolder._connection is None:
            raise ConnectionNotSetupError(
                "The connection to the data server is not setup."
            )
        return _ConnectionHolder._connection


class DataSource:
    """
    DataSource refers to a given source configured in the data server.

    i.e.: In the data server, it's possible to configure a postgres connection
    with a name like "my_postgres_datasource". Then, this class can be used
    to refer to that datasource (without having to explicitly add the name of
    the datasource in the written SQL afterwards).
    """

    @property
    def datasource_name(self) -> str:
        """
        The name of the datasource.
        """
        raise NotImplementedError()

    def connection(self) -> "DataServerConnection":
        """
        The connection to the data server.
        """
        return _ConnectionHolder.connection()

    @classmethod
    def setup_connection_from_input_json(cls, value: dict):
        from sema4ai.data._connection_provider import _ConnectionProviderFromDict

        connection_provider = _ConnectionProviderFromDict(value)
        connection = connection_provider.connection()
        _ConnectionHolder._connection = connection

    @classmethod
    def setup_connection_from_data_context(cls, data_context: "DataContext"):
        from sema4ai.data._connection_provider import (
            _ConnectionProviderFromDataContextOrEnvVar,
        )

        connection_provider = _ConnectionProviderFromDataContextOrEnvVar(
            data_context, "data-server"
        )
        connection = connection_provider.connection()
        _ConnectionHolder._connection = connection

    @classmethod
    def setup_connection_from_env_vars(cls):
        from sema4ai.data._connection_provider import (
            _ConnectionProviderFromDataContextOrEnvVar,
        )

        connection_provider = _ConnectionProviderFromDataContextOrEnvVar(None, "")
        connection = connection_provider.connection()
        _ConnectionHolder._connection = connection

    @classmethod
    def model_validate(cls, *, datasource_name: str) -> "DataSource":
        """
        Creates a DataSource given its name.

        Return: A DataSource instance with the given value.

        Note: the model_validate method is used for compatibility with
            the pydantic API.
        """

        return _DataSourceImpl(datasource_name)

    def query(
        self,
        query: str,
        params: Optional[list[str | int | float] | dict[str, str | int | float]] = None,
    ) -> "ResultSet":
        return self.connection().query(query, params)

    def predict(
        self,
        query: str,
        params: Optional[list[str | int | float] | dict[str, str | int | float]] = None,
    ) -> "ResultSet":
        return self.connection().predict(query, params)


class _DataSourceImpl(DataSource):
    """
    Actual implementation of DataSource (not exposed as we can tweak as needed, only the public API should be relied upon).
    """

    def __init__(self, datasource_name: str):
        self._datasource_name = datasource_name

    @property
    def datasource_name(self) -> str:
        return self._datasource_name
