# DataProject1

The Quality Life project is running in a virtual machine in Google Cloud. 

### Architecture

- NIFI: http://34.121.108.20:8888
(template available in Fiji_DataProject1/DataProject/nifi_dataproject.xml)

- CASSANDRA 

- SPARK: http://34.121.108.20:9999

- WIX 

### Description

The data used to predict the desired city is saved in Fiji_DataProject1/DataProject repository as .csv files. 

Nifi is used to ingest the data (read the different .csv files) and to write the choosen columns in Cassandra database.

With Zeppeling, the Cassandra database is connnected to Spark where the predict model is implemented. 

The WIX website is the direct interface for the client, where the client information is enquired and the result is shown. This website interacts with Zeppelin notebook to get the input data to run the model and to send the result back to the client interface. 


