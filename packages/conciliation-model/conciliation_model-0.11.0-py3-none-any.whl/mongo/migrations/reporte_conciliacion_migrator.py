from mongo.models.conciliation_report import ConciliationReport, StatusConciliationReport
from mongo.mongo_migration_manager import Migrator

reporte_conciliacion_migrator = Migrator(ConciliationReport)

@reporte_conciliacion_migrator.migration(schema_version=2)
def migrate_to_version_2(document: dict):
    if "status" not in document:
        document["status"] = StatusConciliationReport.CONCILIADO.value
    if "detail" not in document:
        document["detail"] = "Proceso de conciliación de ingresos completado"
    return document
