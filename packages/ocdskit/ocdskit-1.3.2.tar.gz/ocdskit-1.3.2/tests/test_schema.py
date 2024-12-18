import pytest
from ocdsextensionregistry.util import replace_refs

from ocdskit.schema import get_schema_fields
from tests import load


def test_items_array():
    schema = load("schema-items-array.json")

    assert {field.path_components for field in get_schema_fields(schema)} == {
        ("json_schema_example_fields", "additionalItems"),
        ("json_schema_example_fields", "additionalProperties"),
        ("json_schema_example_fields", "additionalProperties2"),
        ("json_schema_example_fields", "additionalProperties2", "okay"),
        ("json_schema_example_fields", "allOf"),
        ("json_schema_example_fields", "anyOf"),
        ("json_schema_example_fields", "dependencies"),
        ("json_schema_example_fields", "format"),
        ("json_schema_example_fields", "maximum"),
        ("json_schema_example_fields", "maximum2"),
        ("json_schema_example_fields", "maxItems"),
        ("json_schema_example_fields", "maxLength"),
        ("json_schema_example_fields", "maxProperties"),
        ("json_schema_example_fields", "minimum"),
        ("json_schema_example_fields", "minimum2"),
        ("json_schema_example_fields", "minItems"),
        ("json_schema_example_fields", "minLength"),
        ("json_schema_example_fields", "multipleOf"),
        ("json_schema_example_fields", "not"),
        ("json_schema_example_fields", "oneOf"),
        ("json_schema_example_fields", "oneOf2"),
        ("json_schema_example_fields",),
    }


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        (
            "release_schema_deprecated_fields.json",
            [
                "/awards",
                "/buyer",
                "/contracts",
                "/date",
                "/id",
                "/initiationType",
                "/language",
                "/ocid",
                "/planning",
                "/tag",
                "/tender",
            ],
        ),
        (
            "schema_with_list_and_oneof.json",
            [
                "/dissolutionDate",
                "/entityType",
                "/names",
                "/names/familyName",
                "/names/fullName",
                "/names/givenName",
                "/names/patronymicName",
                "/names/type",
                "/source",
                "/source/assertedBy",
                "/source/assertedBy/name",
                "/source/assertedBy/uri",
                "/source/description",
                "/source/retrievedAt",
                "/source/type",
                "/source/url",
            ],
        ),
    ],
)
def test_libcove(path, expected):
    schema = load("libcove", path)

    assert (
        sorted(
            set({f"/{'/'.join(field.path_components)}" for field in get_schema_fields(schema) if not field.definition})
        )
        == expected
    )


def test_ofds_0_3():
    schema = load("ofds", "schema-0-3-0.json")

    actual = {field.path_components for field in get_schema_fields(schema)}

    # 133
    assert actual == {
        ("links", "next"),
        ("links", "prev"),
        ("links",),
        ("networks", "accuracy"),
        ("networks", "accuracyDetails"),
        ("networks", "collectionDate"),
        ("networks", "contracts"),
        ("networks", "contracts", "dateSigned"),
        ("networks", "contracts", "description"),
        ("networks", "contracts", "documents"),
        ("networks", "contracts", "documents", "description"),
        ("networks", "contracts", "documents", "format"),
        ("networks", "contracts", "documents", "title"),
        ("networks", "contracts", "documents", "url"),
        ("networks", "contracts", "id"),
        ("networks", "contracts", "relatedPhases"),
        ("networks", "contracts", "relatedPhases", "id"),
        ("networks", "contracts", "relatedPhases", "name"),
        ("networks", "contracts", "title"),
        ("networks", "contracts", "type"),
        ("networks", "contracts", "value"),
        ("networks", "contracts", "value", "amount"),
        ("networks", "contracts", "value", "currency"),
        ("networks", "crs"),
        ("networks", "crs", "name"),
        ("networks", "crs", "uri"),
        ("networks", "id"),
        ("networks", "language"),
        ("networks", "links"),
        ("networks", "links", "href"),
        ("networks", "links", "rel"),
        ("networks", "name"),
        ("networks", "nodes"),
        ("networks", "nodes", "accessPoint"),
        ("networks", "nodes", "address"),
        ("networks", "nodes", "address", "country"),
        ("networks", "nodes", "address", "locality"),
        ("networks", "nodes", "address", "postalCode"),
        ("networks", "nodes", "address", "region"),
        ("networks", "nodes", "address", "streetAddress"),
        ("networks", "nodes", "id"),
        ("networks", "nodes", "internationalConnections"),
        ("networks", "nodes", "internationalConnections", "country"),
        ("networks", "nodes", "internationalConnections", "locality"),
        ("networks", "nodes", "internationalConnections", "postalCode"),
        ("networks", "nodes", "internationalConnections", "region"),
        ("networks", "nodes", "internationalConnections", "streetAddress"),
        ("networks", "nodes", "location"),
        ("networks", "nodes", "location", "coordinates"),
        ("networks", "nodes", "location", "type"),
        ("networks", "nodes", "name"),
        ("networks", "nodes", "networkProviders"),
        ("networks", "nodes", "networkProviders", "id"),
        ("networks", "nodes", "networkProviders", "name"),
        ("networks", "nodes", "phase"),
        ("networks", "nodes", "phase", "id"),
        ("networks", "nodes", "phase", "name"),
        ("networks", "nodes", "physicalInfrastructureProvider"),
        ("networks", "nodes", "physicalInfrastructureProvider", "id"),
        ("networks", "nodes", "physicalInfrastructureProvider", "name"),
        ("networks", "nodes", "power"),
        ("networks", "nodes", "status"),
        ("networks", "nodes", "technologies"),
        ("networks", "nodes", "type"),
        ("networks", "organisations"),
        ("networks", "organisations", "country"),
        ("networks", "organisations", "id"),
        ("networks", "organisations", "identifier"),
        ("networks", "organisations", "identifier", "id"),
        ("networks", "organisations", "identifier", "legalName"),
        ("networks", "organisations", "identifier", "scheme"),
        ("networks", "organisations", "identifier", "uri"),
        ("networks", "organisations", "logo"),
        ("networks", "organisations", "name"),
        ("networks", "organisations", "roleDetails"),
        ("networks", "organisations", "roles"),
        ("networks", "organisations", "website"),
        ("networks", "phases"),
        ("networks", "phases", "description"),
        ("networks", "phases", "funders"),
        ("networks", "phases", "funders", "id"),
        ("networks", "phases", "funders", "name"),
        ("networks", "phases", "id"),
        ("networks", "phases", "name"),
        ("networks", "publicationDate"),
        ("networks", "publisher"),
        ("networks", "publisher", "identifier"),
        ("networks", "publisher", "identifier", "id"),
        ("networks", "publisher", "identifier", "legalName"),
        ("networks", "publisher", "identifier", "scheme"),
        ("networks", "publisher", "identifier", "uri"),
        ("networks", "publisher", "name"),
        ("networks", "spans"),
        ("networks", "spans", "capacity"),
        ("networks", "spans", "capacityDetails"),
        ("networks", "spans", "capacityDetails", "description"),
        ("networks", "spans", "countries"),
        ("networks", "spans", "darkFibre"),
        ("networks", "spans", "deployment"),
        ("networks", "spans", "deploymentDetails"),
        ("networks", "spans", "deploymentDetails", "description"),
        ("networks", "spans", "directed"),
        ("networks", "spans", "end"),
        ("networks", "spans", "fibreCount"),
        ("networks", "spans", "fibreLength"),
        ("networks", "spans", "fibreType"),
        ("networks", "spans", "fibreTypeDetails"),
        ("networks", "spans", "fibreTypeDetails", "description"),
        ("networks", "spans", "fibreTypeDetails", "fibreSubtype"),
        ("networks", "spans", "id"),
        ("networks", "spans", "name"),
        ("networks", "spans", "networkProviders"),
        ("networks", "spans", "networkProviders", "id"),
        ("networks", "spans", "networkProviders", "name"),
        ("networks", "spans", "phase"),
        ("networks", "spans", "phase", "id"),
        ("networks", "spans", "phase", "name"),
        ("networks", "spans", "physicalInfrastructureProvider"),
        ("networks", "spans", "physicalInfrastructureProvider", "id"),
        ("networks", "spans", "physicalInfrastructureProvider", "name"),
        ("networks", "spans", "readyForServiceDate"),
        ("networks", "spans", "route"),
        ("networks", "spans", "route", "coordinates"),
        ("networks", "spans", "route", "type"),
        ("networks", "spans", "start"),
        ("networks", "spans", "status"),
        ("networks", "spans", "supplier"),
        ("networks", "spans", "supplier", "id"),
        ("networks", "spans", "supplier", "name"),
        ("networks", "spans", "technologies"),
        ("networks", "spans", "transmissionMedium"),
        ("networks", "website"),
        ("networks",),
    }


def test_rdls_0_2():
    schema = load("rdls", "schema-0-2-0.json")

    actual = {field.path_components for field in get_schema_fields(replace_refs(schema, proxies=True))}

    assert actual == {
        ("attributions", "entity"),
        ("attributions", "entity", "email"),
        ("attributions", "entity", "name"),
        ("attributions", "entity", "url"),
        ("attributions", "id"),
        ("attributions", "role"),
        ("attributions",),
        ("contact_point", "email"),
        ("contact_point", "name"),
        ("contact_point", "url"),
        ("contact_point",),
        ("creator", "email"),
        ("creator", "name"),
        ("creator", "url"),
        ("creator",),
        ("description",),
        ("details",),
        ("exposure", "category"),
        ("exposure", "metrics"),
        ("exposure", "metrics", "dimension"),
        ("exposure", "metrics", "id"),
        ("exposure", "metrics", "quantity_kind"),
        ("exposure", "taxonomy"),
        ("exposure",),
        ("hazard", "event_sets"),
        ("hazard", "event_sets", "analysis_type"),
        ("hazard", "event_sets", "calculation_method"),
        ("hazard", "event_sets", "event_count"),
        ("hazard", "event_sets", "events"),
        ("hazard", "event_sets", "events", "calculation_method"),
        ("hazard", "event_sets", "events", "description"),
        ("hazard", "event_sets", "events", "disaster_identifiers"),
        ("hazard", "event_sets", "events", "disaster_identifiers", "description"),
        ("hazard", "event_sets", "events", "disaster_identifiers", "id"),
        ("hazard", "event_sets", "events", "disaster_identifiers", "scheme"),
        ("hazard", "event_sets", "events", "disaster_identifiers", "uri"),
        ("hazard", "event_sets", "events", "footprints"),
        ("hazard", "event_sets", "events", "footprints", "data_uncertainty"),
        ("hazard", "event_sets", "events", "footprints", "id"),
        ("hazard", "event_sets", "events", "footprints", "intensity_measure"),
        ("hazard", "event_sets", "events", "hazard"),
        ("hazard", "event_sets", "events", "hazard", "id"),
        ("hazard", "event_sets", "events", "hazard", "intensity_measure"),
        ("hazard", "event_sets", "events", "hazard", "processes"),
        ("hazard", "event_sets", "events", "hazard", "trigger"),
        ("hazard", "event_sets", "events", "hazard", "trigger", "processes"),
        ("hazard", "event_sets", "events", "hazard", "trigger", "type"),
        ("hazard", "event_sets", "events", "hazard", "type"),
        ("hazard", "event_sets", "events", "id"),
        ("hazard", "event_sets", "events", "occurrence"),
        ("hazard", "event_sets", "events", "occurrence", "deterministic"),
        ("hazard", "event_sets", "events", "occurrence", "deterministic", "index_criteria"),
        ("hazard", "event_sets", "events", "occurrence", "deterministic", "thresholds"),
        ("hazard", "event_sets", "events", "occurrence", "empirical"),
        ("hazard", "event_sets", "events", "occurrence", "empirical", "return_period"),
        ("hazard", "event_sets", "events", "occurrence", "empirical", "temporal"),
        ("hazard", "event_sets", "events", "occurrence", "empirical", "temporal", "duration"),
        ("hazard", "event_sets", "events", "occurrence", "empirical", "temporal", "end"),
        ("hazard", "event_sets", "events", "occurrence", "empirical", "temporal", "start"),
        ("hazard", "event_sets", "events", "occurrence", "probabilistic"),
        ("hazard", "event_sets", "events", "occurrence", "probabilistic", "event_rate"),
        ("hazard", "event_sets", "events", "occurrence", "probabilistic", "probability"),
        ("hazard", "event_sets", "events", "occurrence", "probabilistic", "probability", "span"),
        ("hazard", "event_sets", "events", "occurrence", "probabilistic", "probability", "value"),
        ("hazard", "event_sets", "events", "occurrence", "probabilistic", "return_period"),
        ("hazard", "event_sets", "frequency_distribution"),
        ("hazard", "event_sets", "hazards"),
        ("hazard", "event_sets", "hazards", "id"),
        ("hazard", "event_sets", "hazards", "intensity_measure"),
        ("hazard", "event_sets", "hazards", "processes"),
        ("hazard", "event_sets", "hazards", "trigger"),
        ("hazard", "event_sets", "hazards", "trigger", "processes"),
        ("hazard", "event_sets", "hazards", "trigger", "type"),
        ("hazard", "event_sets", "hazards", "type"),
        ("hazard", "event_sets", "id"),
        ("hazard", "event_sets", "occurrence_range"),
        ("hazard", "event_sets", "seasonality"),
        ("hazard", "event_sets", "spatial"),
        ("hazard", "event_sets", "spatial", "bbox"),
        ("hazard", "event_sets", "spatial", "centroid"),
        ("hazard", "event_sets", "spatial", "countries"),
        ("hazard", "event_sets", "spatial", "gazetteer_entries"),
        ("hazard", "event_sets", "spatial", "gazetteer_entries", "description"),
        ("hazard", "event_sets", "spatial", "gazetteer_entries", "id"),
        ("hazard", "event_sets", "spatial", "gazetteer_entries", "scheme"),
        ("hazard", "event_sets", "spatial", "gazetteer_entries", "uri"),
        ("hazard", "event_sets", "spatial", "geometry"),
        ("hazard", "event_sets", "spatial", "geometry", "coordinates"),
        ("hazard", "event_sets", "spatial", "geometry", "type"),
        ("hazard", "event_sets", "spatial", "scale"),
        ("hazard", "event_sets", "temporal"),
        ("hazard", "event_sets", "temporal", "duration"),
        ("hazard", "event_sets", "temporal", "end"),
        ("hazard", "event_sets", "temporal", "start"),
        ("hazard",),
        ("id",),
        ("license",),
        ("links", "href"),
        ("links", "rel"),
        ("links",),
        ("loss", "losses"),
        ("loss", "losses", "approach"),
        ("loss", "losses", "category"),
        ("loss", "losses", "cost"),
        ("loss", "losses", "cost", "dimension"),
        ("loss", "losses", "cost", "id"),
        ("loss", "losses", "cost", "unit"),
        ("loss", "losses", "description"),
        ("loss", "losses", "exposure_id"),
        ("loss", "losses", "hazard_analysis_type"),
        ("loss", "losses", "hazard_id"),
        ("loss", "losses", "hazard_process"),
        ("loss", "losses", "hazard_type"),
        ("loss", "losses", "id"),
        ("loss", "losses", "impact"),
        ("loss", "losses", "impact", "base_data_type"),
        ("loss", "losses", "impact", "metric"),
        ("loss", "losses", "impact", "type"),
        ("loss", "losses", "impact", "unit"),
        ("loss", "losses", "type"),
        ("loss", "losses", "vulnerability_id"),
        ("loss",),
        ("project",),
        ("publisher", "email"),
        ("publisher", "name"),
        ("publisher", "url"),
        ("publisher",),
        ("purpose",),
        ("referenced_by", "author_names"),
        ("referenced_by", "date_published"),
        ("referenced_by", "doi"),
        ("referenced_by", "id"),
        ("referenced_by", "name"),
        ("referenced_by", "url"),
        ("referenced_by",),
        ("resources", "access_url"),
        ("resources", "coordinate_system"),
        ("resources", "description"),
        ("resources", "download_url"),
        ("resources", "format"),
        ("resources", "id"),
        ("resources", "media_type"),
        ("resources", "spatial_resolution"),
        ("resources", "temporal"),
        ("resources", "temporal", "duration"),
        ("resources", "temporal", "end"),
        ("resources", "temporal", "start"),
        ("resources", "temporal_resolution"),
        ("resources", "title"),
        ("resources",),
        ("risk_data_type",),
        ("sources", "component"),
        ("sources", "id"),
        ("sources", "name"),
        ("sources", "type"),
        ("sources", "url"),
        ("sources",),
        ("spatial", "bbox"),
        ("spatial", "centroid"),
        ("spatial", "countries"),
        ("spatial", "gazetteer_entries"),
        ("spatial", "gazetteer_entries", "description"),
        ("spatial", "gazetteer_entries", "id"),
        ("spatial", "gazetteer_entries", "scheme"),
        ("spatial", "gazetteer_entries", "uri"),
        ("spatial", "geometry"),
        ("spatial", "geometry", "coordinates"),
        ("spatial", "geometry", "type"),
        ("spatial", "scale"),
        ("spatial",),
        ("temporal_resolution",),
        ("title",),
        ("version",),
        ("vulnerability", "analysis_details"),
        ("vulnerability", "category"),
        ("vulnerability", "cost"),
        ("vulnerability", "cost", "dimension"),
        ("vulnerability", "cost", "id"),
        ("vulnerability", "cost", "unit"),
        ("vulnerability", "functions"),
        ("vulnerability", "functions", "damage_to_loss"),
        ("vulnerability", "functions", "damage_to_loss", "approach"),
        ("vulnerability", "functions", "damage_to_loss", "damage_scale_name"),
        ("vulnerability", "functions", "damage_to_loss", "damage_states_names"),
        ("vulnerability", "functions", "damage_to_loss", "relationship"),
        ("vulnerability", "functions", "engineering_demand"),
        ("vulnerability", "functions", "engineering_demand", "approach"),
        ("vulnerability", "functions", "engineering_demand", "parameter"),
        ("vulnerability", "functions", "engineering_demand", "relationship"),
        ("vulnerability", "functions", "fragility"),
        ("vulnerability", "functions", "fragility", "approach"),
        ("vulnerability", "functions", "fragility", "damage_scale_name"),
        ("vulnerability", "functions", "fragility", "damage_states_names"),
        ("vulnerability", "functions", "fragility", "relationship"),
        ("vulnerability", "functions", "vulnerability"),
        ("vulnerability", "functions", "vulnerability", "approach"),
        ("vulnerability", "functions", "vulnerability", "relationship"),
        ("vulnerability", "hazard_analysis_type"),
        ("vulnerability", "hazard_primary"),
        ("vulnerability", "hazard_process_primary"),
        ("vulnerability", "hazard_process_secondary"),
        ("vulnerability", "hazard_secondary"),
        ("vulnerability", "impact"),
        ("vulnerability", "impact", "base_data_type"),
        ("vulnerability", "impact", "metric"),
        ("vulnerability", "impact", "type"),
        ("vulnerability", "impact", "unit"),
        ("vulnerability", "intensity"),
        ("vulnerability", "se_category"),
        ("vulnerability", "se_category", "description"),
        ("vulnerability", "se_category", "id"),
        ("vulnerability", "se_category", "scheme"),
        ("vulnerability", "se_category", "uri"),
        ("vulnerability", "spatial"),
        ("vulnerability", "spatial", "bbox"),
        ("vulnerability", "spatial", "centroid"),
        ("vulnerability", "spatial", "countries"),
        ("vulnerability", "spatial", "gazetteer_entries"),
        ("vulnerability", "spatial", "gazetteer_entries", "description"),
        ("vulnerability", "spatial", "gazetteer_entries", "id"),
        ("vulnerability", "spatial", "gazetteer_entries", "scheme"),
        ("vulnerability", "spatial", "gazetteer_entries", "uri"),
        ("vulnerability", "spatial", "geometry"),
        ("vulnerability", "spatial", "geometry", "coordinates"),
        ("vulnerability", "spatial", "geometry", "type"),
        ("vulnerability", "spatial", "scale"),
        ("vulnerability", "taxonomy"),
        ("vulnerability",),
    }


def test_bods_0_4():
    schema = load("bods", "schema-0-4-0.json")

    actual = {field.path_components for field in get_schema_fields(schema) if not field.definition}

    # 139
    assert actual == {
        ("annotations", "createdBy"),
        ("annotations", "createdBy", "name"),
        ("annotations", "createdBy", "uri"),
        ("annotations", "creationDate"),
        ("annotations", "description"),
        ("annotations", "motivation"),
        ("annotations", "statementPointerTarget"),
        ("annotations", "transformedContent"),
        ("annotations", "url"),
        ("annotations",),
        ("declaration",),
        ("declarationSubject",),
        ("publicationDetails", "bodsVersion"),
        ("publicationDetails", "license"),
        ("publicationDetails", "publicationDate"),
        ("publicationDetails", "publisher"),
        ("publicationDetails", "publisher", "name"),
        ("publicationDetails", "publisher", "url"),
        ("publicationDetails",),
        ("recordDetails", "addresses"),
        ("recordDetails", "addresses", "address"),
        ("recordDetails", "addresses", "country"),
        ("recordDetails", "addresses", "country", "code"),
        ("recordDetails", "addresses", "country", "name"),
        ("recordDetails", "addresses", "postCode"),
        ("recordDetails", "addresses", "type"),
        ("recordDetails", "alternateNames"),
        ("recordDetails", "birthDate"),
        ("recordDetails", "componentRecords"),
        ("recordDetails", "deathDate"),
        ("recordDetails", "dissolutionDate"),
        ("recordDetails", "entityType"),
        ("recordDetails", "entityType", "details"),
        ("recordDetails", "entityType", "subtype"),
        ("recordDetails", "entityType", "type"),
        ("recordDetails", "formedByStatute"),
        ("recordDetails", "formedByStatute", "date"),
        ("recordDetails", "formedByStatute", "name"),
        ("recordDetails", "foundingDate"),
        ("recordDetails", "identifiers"),
        ("recordDetails", "identifiers", "id"),
        ("recordDetails", "identifiers", "scheme"),
        ("recordDetails", "identifiers", "schemeName"),
        ("recordDetails", "identifiers", "uri"),
        ("recordDetails", "interestedParty"),
        ("recordDetails", "interestedParty", "description"),
        ("recordDetails", "interestedParty", "reason"),
        ("recordDetails", "interests"),
        ("recordDetails", "interests", "beneficialOwnershipOrControl"),
        ("recordDetails", "interests", "details"),
        ("recordDetails", "interests", "directOrIndirect"),
        ("recordDetails", "interests", "endDate"),
        ("recordDetails", "interests", "share"),
        ("recordDetails", "interests", "share", "exact"),
        ("recordDetails", "interests", "share", "exclusiveMaximum"),
        ("recordDetails", "interests", "share", "exclusiveMinimum"),
        ("recordDetails", "interests", "share", "maximum"),
        ("recordDetails", "interests", "share", "minimum"),
        ("recordDetails", "interests", "startDate"),
        ("recordDetails", "interests", "type"),
        ("recordDetails", "isComponent"),
        ("recordDetails", "jurisdiction"),
        ("recordDetails", "jurisdiction", "code"),
        ("recordDetails", "jurisdiction", "name"),
        ("recordDetails", "name"),
        ("recordDetails", "names"),
        ("recordDetails", "names", "familyName"),
        ("recordDetails", "names", "fullName"),
        ("recordDetails", "names", "givenName"),
        ("recordDetails", "names", "patronymicName"),
        ("recordDetails", "names", "type"),
        ("recordDetails", "nationalities"),
        ("recordDetails", "nationalities", "code"),
        ("recordDetails", "nationalities", "name"),
        ("recordDetails", "personType"),
        ("recordDetails", "placeOfBirth"),
        ("recordDetails", "placeOfBirth", "address"),
        ("recordDetails", "placeOfBirth", "country"),
        ("recordDetails", "placeOfBirth", "country", "code"),
        ("recordDetails", "placeOfBirth", "country", "name"),
        ("recordDetails", "placeOfBirth", "postCode"),
        ("recordDetails", "placeOfBirth", "type"),
        ("recordDetails", "politicalExposure"),
        ("recordDetails", "politicalExposure", "details"),
        ("recordDetails", "politicalExposure", "details", "endDate"),
        ("recordDetails", "politicalExposure", "details", "jurisdiction"),
        ("recordDetails", "politicalExposure", "details", "jurisdiction", "code"),
        ("recordDetails", "politicalExposure", "details", "jurisdiction", "name"),
        ("recordDetails", "politicalExposure", "details", "missingInfoReason"),
        ("recordDetails", "politicalExposure", "details", "reason"),
        ("recordDetails", "politicalExposure", "details", "source"),
        ("recordDetails", "politicalExposure", "details", "source", "assertedBy"),
        ("recordDetails", "politicalExposure", "details", "source", "assertedBy", "name"),
        ("recordDetails", "politicalExposure", "details", "source", "assertedBy", "uri"),
        ("recordDetails", "politicalExposure", "details", "source", "description"),
        ("recordDetails", "politicalExposure", "details", "source", "retrievedAt"),
        ("recordDetails", "politicalExposure", "details", "source", "type"),
        ("recordDetails", "politicalExposure", "details", "source", "url"),
        ("recordDetails", "politicalExposure", "details", "startDate"),
        ("recordDetails", "politicalExposure", "status"),
        ("recordDetails", "publicListing"),
        ("recordDetails", "publicListing", "companyFilingsURLs"),
        ("recordDetails", "publicListing", "hasPublicListing"),
        ("recordDetails", "publicListing", "securitiesListings"),
        ("recordDetails", "publicListing", "securitiesListings", "marketIdentifierCode"),
        ("recordDetails", "publicListing", "securitiesListings", "operatingMarketIdentifierCode"),
        ("recordDetails", "publicListing", "securitiesListings", "security"),
        ("recordDetails", "publicListing", "securitiesListings", "security", "id"),
        ("recordDetails", "publicListing", "securitiesListings", "security", "idScheme"),
        ("recordDetails", "publicListing", "securitiesListings", "security", "ticker"),
        ("recordDetails", "publicListing", "securitiesListings", "stockExchangeJurisdiction"),
        ("recordDetails", "publicListing", "securitiesListings", "stockExchangeName"),
        ("recordDetails", "subject"),
        ("recordDetails", "subject", "description"),
        ("recordDetails", "subject", "reason"),
        ("recordDetails", "taxResidencies"),
        ("recordDetails", "taxResidencies", "code"),
        ("recordDetails", "taxResidencies", "name"),
        ("recordDetails", "unspecifiedEntityDetails"),
        ("recordDetails", "unspecifiedEntityDetails", "description"),
        ("recordDetails", "unspecifiedEntityDetails", "reason"),
        ("recordDetails", "unspecifiedPersonDetails"),
        ("recordDetails", "unspecifiedPersonDetails", "description"),
        ("recordDetails", "unspecifiedPersonDetails", "reason"),
        ("recordDetails", "uri"),
        ("recordDetails",),
        ("recordId",),
        ("recordStatus",),
        ("recordType",),
        ("source", "assertedBy"),
        ("source", "assertedBy", "name"),
        ("source", "assertedBy", "uri"),
        ("source", "description"),
        ("source", "retrievedAt"),
        ("source", "type"),
        ("source", "url"),
        ("source",),
        ("statementDate",),
        ("statementId",),
    }


def test_bods_0_3():
    schema = load("bods", "schema-0-3-0.json")

    actual = {field.path_components for field in get_schema_fields(schema)}

    # 138
    assert actual == {
        ("addresses", "address"),
        ("addresses", "country"),
        ("addresses", "postCode"),
        ("addresses", "type"),
        ("addresses",),
        ("alternateNames",),
        ("annotations", "createdBy"),
        ("annotations", "createdBy", "name"),
        ("annotations", "createdBy", "uri"),
        ("annotations", "creationDate"),
        ("annotations", "description"),
        ("annotations", "motivation"),
        ("annotations", "statementPointerTarget"),
        ("annotations", "transformedContent"),
        ("annotations", "url"),
        ("annotations",),
        ("birthDate",),
        ("componentStatementIDs",),
        ("deathDate",),
        ("dissolutionDate",),
        ("entitySubtype", "generalCategory"),
        ("entitySubtype", "localTerm"),
        ("entitySubtype",),
        ("entityType",),
        ("formedByStatute", "date"),
        ("formedByStatute", "name"),
        ("formedByStatute",),
        ("foundingDate",),
        ("identifiers", "id"),
        ("identifiers", "scheme"),
        ("identifiers", "schemeName"),
        ("identifiers", "uri"),
        ("identifiers",),
        ("interestedParty", "describedByEntityStatement"),
        ("interestedParty", "describedByPersonStatement"),
        ("interestedParty", "unspecified"),
        ("interestedParty", "unspecified", "description"),
        ("interestedParty", "unspecified", "reason"),
        ("interestedParty",),
        ("interests", "beneficialOwnershipOrControl"),
        ("interests", "details"),
        ("interests", "directOrIndirect"),
        ("interests", "endDate"),
        ("interests", "share"),
        ("interests", "share", "exact"),
        ("interests", "share", "exclusiveMaximum"),
        ("interests", "share", "exclusiveMinimum"),
        ("interests", "share", "maximum"),
        ("interests", "share", "minimum"),
        ("interests", "startDate"),
        ("interests", "type"),
        ("interests",),
        ("isComponent",),
        ("jurisdiction", "code"),
        ("jurisdiction", "name"),
        ("jurisdiction",),
        ("name",),
        ("names", "familyName"),
        ("names", "fullName"),
        ("names", "givenName"),
        ("names", "patronymicName"),
        ("names", "type"),
        ("names",),
        ("nationalities", "code"),
        ("nationalities", "name"),
        ("nationalities",),
        ("personType",),
        ("placeOfBirth", "address"),
        ("placeOfBirth", "country"),
        ("placeOfBirth", "postCode"),
        ("placeOfBirth", "type"),
        ("placeOfBirth",),
        ("placeOfResidence", "address"),
        ("placeOfResidence", "country"),
        ("placeOfResidence", "postCode"),
        ("placeOfResidence", "type"),
        ("placeOfResidence",),
        ("politicalExposure", "details"),
        ("politicalExposure", "details", "endDate"),
        ("politicalExposure", "details", "jurisdiction"),
        ("politicalExposure", "details", "jurisdiction", "code"),
        ("politicalExposure", "details", "jurisdiction", "name"),
        ("politicalExposure", "details", "missingInfoReason"),
        ("politicalExposure", "details", "reason"),
        ("politicalExposure", "details", "source"),
        ("politicalExposure", "details", "source", "assertedBy"),
        ("politicalExposure", "details", "source", "assertedBy", "name"),
        ("politicalExposure", "details", "source", "assertedBy", "uri"),
        ("politicalExposure", "details", "source", "description"),
        ("politicalExposure", "details", "source", "retrievedAt"),
        ("politicalExposure", "details", "source", "type"),
        ("politicalExposure", "details", "source", "url"),
        ("politicalExposure", "details", "startDate"),
        ("politicalExposure", "status"),
        ("politicalExposure",),
        ("publicationDetails", "bodsVersion"),
        ("publicationDetails", "license"),
        ("publicationDetails", "publicationDate"),
        ("publicationDetails", "publisher"),
        ("publicationDetails", "publisher", "name"),
        ("publicationDetails", "publisher", "url"),
        ("publicationDetails",),
        ("publicListing", "companyFilingsURLs"),
        ("publicListing", "hasPublicListing"),
        ("publicListing", "securitiesListings"),
        ("publicListing", "securitiesListings", "marketIdentifierCode"),
        ("publicListing", "securitiesListings", "operatingMarketIdentifierCode"),
        ("publicListing", "securitiesListings", "security"),
        ("publicListing", "securitiesListings", "security", "id"),
        ("publicListing", "securitiesListings", "security", "idScheme"),
        ("publicListing", "securitiesListings", "security", "ticker"),
        ("publicListing", "securitiesListings", "stockExchangeJurisdiction"),
        ("publicListing", "securitiesListings", "stockExchangeName"),
        ("publicListing",),
        ("replacesStatements",),
        ("source", "assertedBy"),
        ("source", "assertedBy", "name"),
        ("source", "assertedBy", "uri"),
        ("source", "description"),
        ("source", "retrievedAt"),
        ("source", "type"),
        ("source", "url"),
        ("source",),
        ("statementDate",),
        ("statementID",),
        ("statementType",),
        ("subject", "describedByEntityStatement"),
        ("subject",),
        ("taxResidencies", "code"),
        ("taxResidencies", "name"),
        ("taxResidencies",),
        ("unspecifiedEntityDetails", "description"),
        ("unspecifiedEntityDetails", "reason"),
        ("unspecifiedEntityDetails",),
        ("unspecifiedPersonDetails", "description"),
        ("unspecifiedPersonDetails", "reason"),
        ("unspecifiedPersonDetails",),
        ("uri",),
    }
