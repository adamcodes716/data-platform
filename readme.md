

*** Virtual environment

python -m venv myenv

myenv\Scripts\activatepip

## Launching this repo
Extract the project into a folder and issue "docker compose up" from the root of the project folder.  Everything should load up without any further interaction.


## Note from Adam

I am ultimately trying to accomplish two main goals:

1. Upload data in such a way that data tables are stored in minio and catalog service (currently Nessie) has the apppropriate metadata
2. Apache superset needs to be be able to query the data.  To accomplish this, there is a setup file in trino-config/catalog/iceberg.properties.  This file defines the connection to nessie for Trino.

## Data Loading
I followed this guide to get data loaded using SQL commands in dremio (I had no problems here).  https://www.dremio.com/blog/intro-to-dremio-nessie-and-apache-iceberg-on-your-laptop/

## Current Difficulty - setting up the catalog service
I am struggling to correctly define the catalog service. 
   1. Trino needs to be aware of the catalog using the aforementioned properties file.  
   2. Superset needs to be able to use trino as the means to access the catalog.   The alchemy connection string should look something like this:

   http://trino://admin@trino:8080/iceberg

    More information on this:  
    https://projectnessie.org/blog/2024/05/13/nessie-integration-of-iceberg-rest/https://medium.com/@ajanthabhat/iceberg-catalogs-choosing-the-right-one-for-your-needs-77ff6dcfaec0


## Easy path to reproduce the issue
I don't think that you would need to populate the data to reproduce the issue.

1.  docker compose up to launch the containers
2.  In minio, create a bucket called "warehouse"
3.  docker exec into the 'trino' container.   docker exec -it trino trino
    a. Issue "SHOW CATALOGS".  You should see "iceberg" because there is a trino-config/catalog/iceberg.properties file.   
    b. Issue "SHOW SCHEMAS FROM iceberg;".  You will get an error:

    2025-02-17T23:58:19.894Z        ERROR   dispatcher-query-2      io.trino.execution.QueryStateMachine    Error cleaning up query: org.apache.iceberg.exceptions.RESTException: Unable to process:
2025-02-17T23:58:19.901Z        INFO    dispatcher-query-1      io.trino.event.QueryMonitor     TIMELINE: Query 20250217_235819_00000_54y4r :: FAILED (GENERIC_INTERNAL_ERROR) :: elapsed 254ms :: planning 254ms :: waiting 0ms :: scheduling 0ms :: running 0ms :: finishing 0ms :: begin 2025-02-17T23:58:19.625Z :: end 2025-02-17T23:58:19.879Z
2025-02-18T00:02:55.481Z        INFO    dispatcher-query-9      io.trino.event.QueryMonitor     TIMELINE: Query 20250218_000254_00000_54y4r :: FINISHED :: elapsed 1103ms :: planning 478ms :: waiting 53ms :: scheduling 382ms :: running 58ms :: finishing 185ms :: begin 2025-02-18T00:02:54.373Z :: end 2025-02-18T00:02:55.476Z
2025-02-18T00:03:03.583Z        WARN    Query-20250218_000303_00001_54y4r-197   org.apache.iceberg.rest.ErrorHandlers  Unable to parse error response
java.io.UncheckedIOException: com.fasterxml.jackson.databind.exc.MismatchedInputException: No content to map due to end-of-input
 at [Source: REDACTED (`StreamReadFeature.INCLUDE_SOURCE_IN_LOCATION` disabled); line: 1]

 ### It doesn't look like the nessie endpoints (api/v1, api/v2, /iceberg) are active

 ## Loading the data

 This is also an issue