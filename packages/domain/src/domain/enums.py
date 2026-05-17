from enum import Enum


class EntityType(str, Enum):
    PROGRAM = "program"
    SUBSYSTEM = "subsystem"
    REQUIREMENT = "requirement"
    SOFTWARE_BUILD = "software_build"
    TEST_CASE = "test_case"
    TEST_RESULT = "test_result"
    HAZARD = "hazard"
    MITIGATION = "mitigation"
    SAFETY_ANALYSIS = "safety_analysis"
    CERTIFICATION_OBJECTIVE = "certification_objective"
    APPROVAL = "approval"
    SUPPLIER = "supplier"
    DOCUMENT = "document"
    REGULATORY_OBLIGATION = "regulatory_obligation"


class RelationshipType(str, Enum):
    TRACES_TO = "TRACES_TO"
    IMPLEMENTS = "IMPLEMENTS"
    VERIFIES = "VERIFIES"
    SATISFIES = "SATISFIES"
    MITIGATES = "MITIGATES"
    AFFECTS = "AFFECTS"
    DERIVES_FROM = "DERIVES_FROM"
    APPROVES = "APPROVES"
    REFERENCES = "REFERENCES"


class SourceSystem(str, Enum):
    POLARION = "polarion"
    DOORS = "doors"
    JAMA = "jama"
    TEAMCENTER = "teamcenter"
    WINDCHILL = "windchill"
    SHAREPOINT = "sharepoint"
    GIT = "git"
    TESTRAIL = "testrail"
    SAP = "sap"
    EMAIL = "email"
    FILE_UPLOAD = "file_upload"
    MANUAL = "manual"
    REGULATORY_FEED = "regulatory_feed"


class DalLevel(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


class ExportControl(str, Enum):
    ITAR = "ITAR"
    EAR = "EAR"
    EAR99 = "EAR99"
    PUBLIC = "PUBLIC"
    UNKNOWN = "UNKNOWN"


class StandardFramework(str, Enum):
    DO_178C = "DO-178C"
    DO_254 = "DO-254"
    ARP4754A = "ARP4754A"
    AS9100 = "AS9100"
    DO_326A = "DO-326A"
    FAA_AC = "FAA-AC"
    EASA_CS = "EASA-CS"
    MIL_STD = "MIL-STD"


class ConfidenceTier(str, Enum):
    AUTHORITATIVE = "authoritative"
    INFERRED = "inferred"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
