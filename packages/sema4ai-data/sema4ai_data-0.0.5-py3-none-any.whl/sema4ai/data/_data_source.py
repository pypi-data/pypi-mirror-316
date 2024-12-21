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
    DataSource is a class that is injected automatically by the framework in `@query` or `@predict`
    and can be used to make queries or run SQL commands in the Data Server.

    It's expected to be annotated with a `DataSourceSpec` with information about the data source
    (this information is used so that clients can know which data source is being used so that
    they can properly configure the connection in the Data Server).

    Example:

        Definition (data_sources.py):

        ```python
        from typing import Annotated
        from sema4ai.data import DataSource, DataSourceSpec

        PostgresDataSource = Annotated[DataSource, DataSourceSpec(
            name="my_datasource",
            engine="postgres",
        )]
        ```

        Usage (data_action.py):
        ```python
        from sema4ai.data import DataSource
        from sema4ai.actions import Response, Table
        from data_sources import PostgresDataSource

        @query
        def my_query(datasource: PostgresDataSource) -> Response[Table]:
            result_set = datasource.query("SELECT * FROM `my_datasource`.my_table")
            return Response(result=result_set.to_table())
        ```
    """

    @property
    def datasource_name(self) -> str:
        """
        The name of the Data Source.

        Note: this may be an empty string if the Data Source is not annotated with a `DataSourceSpec`
        or if it's the result of a Union of multiple data sources received in a `@query` or `@predict`
        function.
        """
        raise NotImplementedError()

    def connection(self) -> "DataServerConnection":
        """
        The connection to the data server.
        """
        return _ConnectionHolder.connection()

    @classmethod
    def setup_connection_from_input_json(cls, value: dict):
        """
        Private API to setup the connection from a JSON object.

        Not expected to be called by users. May be removed in the future.
        """
        from sema4ai.data._connection_provider import _ConnectionProviderFromDict

        connection_provider = _ConnectionProviderFromDict(value)
        connection = connection_provider.connection()
        _ConnectionHolder._connection = connection

    @classmethod
    def setup_connection_from_data_context(cls, data_context: "DataContext"):
        """
        Private API to setup the connection from a DataContext.

        Not expected to be called by users. May be removed in the future.
        """
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
        """
        Private API to setup the connection from environment variables.

        Not expected to be called by users. May be removed in the future.
        """
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
        """
        API to execute a query and get the result set.

        Args:
            query: The SQL to execute.
            params: The parameters to pass to the query.

                If a list is provided, the parameters are used as positional parameters
                and `?` is used as placeholder.

                If a dict is provided, the parameters are used as named parameters
                and names such as `$key` are used as placeholders.

                Note: the parameters can only be used in the SQL for the replacement of regular variables,
                not for the datasource name (i.e.: it works when the escaping single or double quotes,
                but for datasource names must be escaped with backticks).

                Note: It's expected that the SQL is always using the full data source name (i.e.: `datasource_name.table_name`)
                and not just the table name (i.e.: `table_name`).

        Returns:
            The result set from the query.

        Example:
            result_set = datasource.query("SELECT * FROM `datasource_name`.my_table WHERE id = ?", [1])
            return Response(result=result_set.to_table())

            result_set = datasource.query("SELECT * FROM `datasource_name`.my_table WHERE id = $id", {"id": 1})
            return Response(result=result_set.to_table())
        """
        return self.connection().query(query, params)

    def predict(
        self,
        query: str,
        params: Optional[list[str | int | float] | dict[str, str | int | float]] = None,
    ) -> "ResultSet":
        """
        API to execute a prediction and get the result set.

        Args:
            query: The SQL to execute.
            params: The parameters to pass to the query.

                If a list is provided, the parameters are used as positional parameters
                and `?` is used as placeholder.

                If a dict is provided, the parameters are used as named parameters
                and names such as `$key` are used as placeholders.

                Note: the parameters can only be used in the SQL for the replacement of regular variables,
                not for the datasource name (i.e.: it works when the escaping single or double quotes,
                but for datasource names must be escaped with backticks).

                Note: It's expected that the SQL is always using the full data source name (i.e.: `datasource_name.table_name`)
                and not just the table name (i.e.: `table_name`).

        Returns:
            The result set from the prediction.

        Example:
            result_set = datasource.predict("SELECT * FROM `datasource_name`.my_table WHERE id = ?", [1])
            return Response(result=result_set.to_table())

            result_set = datasource.predict("SELECT * FROM `datasource_name`.my_table WHERE id = $id", {"id": 1})
            return Response(result=result_set.to_table())

        Note: the only difference between `query()` and `predict()` is that `predict()` is expected to be used when
        querying a model.
        """
        return self.connection().predict(query, params)

    def execute_sql(
        self,
        sql: str,
        params: Optional[list[str | int | float] | dict[str, str | int | float]] = None,
    ) -> "ResultSet | None":
        """
        API to execute some SQL. Either it can return a result set (if it was a query) or None
        (if it was some other SQL command).

        Args:
            query: The SQL to execute.
            params: The parameters to pass to the query.

                If a list is provided, the parameters are used as positional parameters
                and `?` is used as placeholder.

                If a dict is provided, the parameters are used as named parameters
                and names such as `$key` are used as placeholders.

                Note: the parameters can only be used in the SQL for the replacement of regular variables,
                not for the datasource name (i.e.: it works when the escaping single or double quotes,
                but for datasource names must be escaped with backticks).

                Note: It's expected that the SQL is always using the full data source name (i.e.: `datasource_name.table_name`)
                and not just the table name (i.e.: `table_name`).

        Returns:
            The result set if the SQL was a query or None if it was some other SQL command.

        Example:
            datasource.run_sql("UPDATE `datasource_name`.my_table SET name = 'John' WHERE id = 1")
        """
        return self.connection().execute_sql(sql, params)


class _DataSourceImpl(DataSource):
    """
    Actual implementation of DataSource (not exposed as we can tweak as needed, only the public API should be relied upon).
    """

    def __init__(self, datasource_name: str):
        self._datasource_name = datasource_name

    @property
    def datasource_name(self) -> str:
        return self._datasource_name
