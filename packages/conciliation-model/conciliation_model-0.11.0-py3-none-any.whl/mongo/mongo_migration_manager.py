import warnings
from typing import Awaitable, Callable, Self, Type

from loggerk import LoggerK

from mongo.core.base_mongo_model import BaseMongoModel
from mongo.core.mongo_connection import MongoConnection
from utils.async_checker import is_async_function


class Migrator:
    """
    Class responsible for managing migrations for a specific model.

    Usage:

    ```python
    from apps.mongo.models import MyModel
    from apps.mongo.mongo_migration_manager import Migrator

    myModelMigrator = Migrator(model=MyModel)

    @myModelMigrator.migrate_to(2) # the version to migrate to
    async def migrate_to_2(document: dict):
        # update the document to the new schema
        return document

    @myModelMigrator.migrate_to(3) # the version to migrate to
    async def migrate_to_3(document: dict):
        # update the document to the new schema
        return document

    ```
    """

    model: Type[BaseMongoModel]
    model_migrations: dict[int, Callable[[dict], Awaitable[dict]]]

    def __init__(self, model: Type[BaseMongoModel]):
        """
        Initializes the Migrator instance.

        Args:
            model (Type[BaseMongoModel]): The model associated with the migrator.
        """
        self.model = model
        self.model_migrations = {}

    def migration(self, schema_version: int):
        """
        Decorator function for defining migrations.

        Args:
            schema_version (int): The version number of the schema to migrate to.

        Usage:
        ```python
        @migrator.migrate_to(2)
        async def migrate_to_2(document: dict):
            # update the document to the new schema
            return document  # make sure to return the document
        ```

        Returns:
            Callable: A decorator function that wraps the migration function.
        """

        def _migration_wrapper(
            func: Callable[[dict], dict] | Callable[[dict], Awaitable[dict]]
        ):
            async def _run_funct_and_update_schema_version(document: dict) -> dict:
                """
                Runs the migration function and updates the schema version.

                Args:
                    document (dict): The document to be migrated.

                Returns:
                    dict: The migrated document.
                """
                if is_async_function(func):
                    migrated_document = await func(document)
                else:
                    migrated_document = func(document)

                if migrated_document is None:
                    raise InvalidMigrationFunction(
                        "Migration function must return the document after migration"
                    )

                migrated_document["schema_version"] = schema_version  # type: ignore

                return migrated_document  # type: ignore

            if schema_version not in self.model_migrations:
                self.model_migrations[schema_version] = (
                    _run_funct_and_update_schema_version
                )
            else:
                warnings.warn(
                    message=f"There is already a migration function for schema_version {schema_version} of {self.model} ",
                    category=RedefinedMigrationWarning,
                    stacklevel=2,
                )

        return _migration_wrapper


class MongoMigrationManager:
    """Singleton Class to manage migrations on the Mongo Database

    Usage:

    - on the entry point of the app, import and instantiate the class
    - define the migrations using the Migrator class
    - add the migrators to the instance

    Example:

    Initializing the Singleton

    ```python
    >> main.py
    mongo_migration_manager = MongoMigrationManager()
    ```

    Defining the migrations

    ```python
    >> my_model_migrator.py

    from apps.mongo.models import MyModel
    from apps.mongo.mongo_migration_manager import Migrator

    myModelMigrator = Migrator(model=MyModel)

    # Using the decorator to define the migrations

    @myModelMigrator.migrate_to(2) # the version to migrate to
    async def migrate_to_2(document: dict):
        # update the document to the new schema
        return document

    ```

    Adding the migrators to the instance

    ```python
    >> main.py

    mongo_migration_manager.add_migrator(proyectoMigrator)
    ```

    Running the migrations

    ```python
    >> main.py # or any other file, as this is a singleton

    await mongo_migration_manager.migrate()
    ```
    """

    _instance: Self | None = None
    _logger: LoggerK
    _connection: MongoConnection
    _migrations: dict[
        Type[BaseMongoModel], dict[int, Callable[[dict], Awaitable[dict]]]
    ]

    def __new__(
        cls,
        connection: MongoConnection = MongoConnection(),
    ) -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._connection = connection

            cls._instance._migrations = {}

            cls._instance._logger = LoggerK(cls.__name__)
        return cls._instance

    async def _apply_migration(self, collection: Type[BaseMongoModel], document: dict):
        model_migrations = self._migrations.get(collection, {})
        document_version = document.get("schema_version", 1)
        lastest_version = collection.__schema_version__

        while document_version < lastest_version:

            migration_function = model_migrations.get(document_version + 1)

            if not migration_function:
                raise MissingMigrationFunction(
                    f"Migration function for {collection}@V{document_version} not found"
                )

            self._logger.info(f"Applying migration function: {migration_function}")

            document = await migration_function(document)
            document_version += 1

        return document

    async def _migrate_collection(
        self,
        collection: Type[BaseMongoModel],
    ):
        self._logger.info(f"Migrating collection {collection}")

        collection_name = collection.__collection_name__
        if not collection_name:
            raise MissingCollectionName("Collection name not defined")

        collection_bd = self._connection.db[collection_name]
        documents = collection_bd.find({})

        for document in documents:
            document = await self._apply_migration(
                collection=collection,
                document=document,
            )
            collection_bd.replace_one(
                filter={"_id": document["_id"]},
                replacement=document,
            )

        self._logger.info(f"Collection {collection} migrated successfully")

    async def perform_migrations(self):
        self._logger.info("Migrating collections")
        for collection in self._migrations.keys():
            await self._migrate_collection(collection=collection)

    def add_migrator(self, migrator: Migrator):
        if not migrator.model in self._migrations:
            self._migrations[migrator.model] = {}

        self._migrations[migrator.model] = migrator.model_migrations


class RedefinedMigrationWarning(UserWarning):
    pass


class InvalidMigrationFunction(Exception):
    pass


class MissingMigrationFunction(Exception):
    pass


class MissingCollectionName(Exception):
    pass
