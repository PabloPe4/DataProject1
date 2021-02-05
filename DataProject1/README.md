<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
>>>>>>> Stashed changes
# QUALITY LIFE - Team FIJI

The Quality Life project is running in a virtual machine in Google Cloud. 

### Architecture

- NIFI: http://34.121.108.20:8888
(template available in Fiji_DataProject1/DataProject/nifi_dataproject.xml)

- CASSANDRA 

- ZEPPELIN: http://34.121.108.20:9999

- WIX: https://penades497.editorx.io/qualitylife

### Description

The data used to predict the desired city is saved in Fiji_DataProject1/DataProject repository as .csv files. 

Nifi is used to ingest the data (read the different .csv files) and to write the choosen columns in Cassandra database.

With Zeppeling, the Cassandra database is connnected to Spark where the predict model is implemented. 

The WIX website is the direct interface for the client, where the client information is enquired and the result is shown. This website interacts with Zeppelin notebook to get the input data to run the model and to send the result back to the client interface. 

### Instructions

How to use the app:

1. Open the link: https://penades497.editorx.io/qualitylife/blank-2
2. Fill the form and click "Enviar"
3. The result will appear automatically

Feel free to navigate through the website https://penades497.editorx.io/qualitylife to discover our cities. 
<<<<<<< Updated upstream
=======
=======
# DataProject1

The Quality Life project is running in a virtual machine in Google Cloud. 

# Architecture

- NIFI: template available in Fiji_DataProject1/DataProject/nifi_dataproject.xml

- CASSANDRA

- SPARK:  http://34.121.108.20:9999

- WIX: https://penades497.editorx.io/qualitylife

>>>>>>> Stashed changes
>>>>>>> Stashed changes
