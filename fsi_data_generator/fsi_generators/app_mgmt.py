from faker import Faker

from fsi_data_generator.fsi_generators.text_list import text_list

fake = Faker()


def app_mgmt(dg):
    return [
        ('app_mgmt\\..*', '^dependency_type$', text_list([
            "runtime"
            "build"
            "test"
            "development"
            "optional"
            "provided"
            "system"
            "import"
            "compile"
            "annotationProcessor"
        ])),
        ('app_mgmt\\.application_relationships', '^criticality$', text_list([
            "no_impact",
            "minimal_impact",
            "minor_impact",
            "moderate_impact",
            "significant_impact",
            "critical_impact"])),
        ('app_mgmt\\.applications', '^lifecycle_status$', text_list([
            "Development",
            "Pilot",
            "Production",
            "Deprecated",
            "DataMaintenance",
            "Decommissioned",
            "Archived"])),
        ('app_mgmt\\.applications', '^deployment_environment$', text_list([
            "OnPremises",
            "CloudPublic",
            "CloudPrivate",
            "CloudHybrid",
            "Containerized",
            "Serverless",
            "Edge"
        ])),
        ('app_mgmt\\.applications', '^application_type$', text_list([
            "Web",
            "Mobile",
            "Desktop",
            "API",
            "Batch",
            "Microservice",
            "Legacy",
            "SaaS",
            "Database",
            "Middleware",
            "Embedded"
        ]))
    ]
