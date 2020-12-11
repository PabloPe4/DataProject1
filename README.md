# DataProject1

The Quality Life project is running in a virtual machine in Google Cloud. 

### Architecture

- NIFI: http://34.121.108.20:8888
(template available in Fiji_DataProject1/DataProject/nifi_dataproject.xml)

- CASSANDRA 

- SPARK: http://34.121.108.20:9999

- WIX 

### Description

The data used to predict the desired city is saved in Fiji_DataProject1/DataProject repository as .csv files. Nifi is used to ingest the data (read the different .csv files) and to writte the choosen columns in Cassandra database.

........

The WIX website is the direct interface for the client, where the client information is enquired and where the result is shown.

.............
