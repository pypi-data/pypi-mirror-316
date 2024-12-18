from mongo.models.datasource_upload import DatasourceUpload
from mongo.mongo_migration_manager import Migrator
from mongo.pydantic_types.date import Date

datasource_upload_migrator = Migrator(DatasourceUpload)


@datasource_upload_migrator.migration(2)
def migrate_to_version_2(document: dict):
    if "upload_date" in document:
        return document
    month = document.get("month", Date().month)
    year = document.get("year", Date().year)
    document["upload_date"] = Date(year=year, month=month, day=1)
    return document
