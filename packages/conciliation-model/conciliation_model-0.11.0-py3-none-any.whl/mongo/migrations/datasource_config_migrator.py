from mongo.daos.excel_data_type_dao import ExcelDataTypeDAO
from mongo.models.datasource_config import (DatasourceConfig,
                                                 DatasourceConfigStatus)
from mongo.mongo_migration_manager import Migrator

datasource_config_migrator = Migrator(DatasourceConfig)


@datasource_config_migrator.migration(schema_version=2)
def migrate_to_version_2(document: dict):
    if "template_s3_path" in document:
        return document
    document["template_s3_path"] = None
    return document


@datasource_config_migrator.migration(schema_version=3)
async def migrate_to_version_3(document: dict):
    excel_data_types = ExcelDataTypeDAO()
    string_object = await excel_data_types.get(nativo="string")
    header_types = document["header_types"]

    for header in header_types:
        header_types[header] = string_object.id
    document["header_types"] = header_types
    return document


@datasource_config_migrator.migration(schema_version=4)
def migrate_to_version_4(document: dict):
    if "config_status" not in document:
        document["config_status"] = DatasourceConfigStatus.CREATED.value
    return document
