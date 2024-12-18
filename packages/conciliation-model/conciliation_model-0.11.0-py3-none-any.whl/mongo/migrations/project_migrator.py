from mongo.models.project import (Project, ProjectConfigurationStatus,
                                       ProjectStatus, Trigger)
from mongo.mongo_migration_manager import Migrator

project_migrator = Migrator(Project)


@project_migrator.migration(schema_version=2)
def migrate_to_version_2(document: dict):
    if "schedule_config" in document:
        return document

    triggers: list[str] = document.get("trigger", [])
    if Trigger.SCHEDULED.value in triggers:
        document["schedule_config"] = {"day_of_month": 1}
    return document


@project_migrator.migration(schema_version=3)
def migrate_to_version_3(document: dict):
    if "project_status" not in document:
        document["project_status"] = ProjectStatus.ACTIVE.value
    return document


@project_migrator.migration(schema_version=4)
def migrate_to_version_4(document: dict):
    if "configuration_status" not in document:
        document["configuration_status"] = (
            ProjectConfigurationStatus.INITIAL_CONFIG.value
        )
    return document
