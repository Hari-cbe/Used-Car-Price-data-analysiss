<p align="center">
</p>
<p align="center">
    <h1 align="center">USED-CAR-PRICE-DATA-ANALYSIS</h1>
</p>
<p align="center">
   This project aims to analyze data related to used car prices to derive insights that can aid in understanding the factors influencing car prices in the secondary market.
</p>

<h2><img src="https://cdn-icons-png.flaticon.com/128/1150/1150643.png" width="20"> Overview </h2>

This is final project for the **[DataTalks Data Engineering zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)**. 
In which I have made a end-to-end pipeline 
- Extracting data from the source and loading it into a Google Storage Bucket. 
- Creating Big Query Table from the storage data.
- Visualize using the looker studio 
<hr>

<h2><img src="https://cdn-icons-png.flaticon.com/128/3066/3066169.png" width="25"> Motivation </h2>
<p> The motivation for this project is to find trend of the second hand car market in the US. The second-hand car market offers affordability, sustainability, and community engagement, providing access to quality vehicles at lower prices while reducing waste and promoting resourcefulness in transportation choices.

This analyis will help the people to find solutions for 
<ul>
<li>what cars sells the most in the second hand market ?</li> 
<li>In which states does the second hand car market is booming ?</li>
<li>In which state can we open does the second hand car market busniess ?</li>
</ul>
These are some of the examples this analysis will answer.
</p>

---
<h2> <img src="https://cdn-icons-png.flaticon.com/128/4043/4043312.png" width="20"> Architectural diagram </h2>
<img src="https://github.com/Hari-cbe/Random-resourses/blob/main/Used-car-price-data/images/Untitled%20Diagram.drawio.png?raw=true>">

<h4> Architectural Explanition </h4>
<p>Google Cloud Provider is being used for the cloud processing and cloud storage. In GCP Google's Compute Engine is being used for the Virtual Machine. So, We can work in different envirnoment</p> 
First data is downloaded from a source file and stored in the local file system. Then from the local file system data is being moved to GCS using Aiflow. Then from the GCS data bigquery table is created, From the Big Query Table then transformed with the help of dbt( Data Build Tool ). Then Visualization is created with the help of transformed data 
<hr>
<h2> <img src="https://cdn-icons-png.flaticon.com/128/10214/10214613.png" width="20"> How to run the Project on your system</h2>
To run the project locally, on your system, you will need to install tools such as

* **Google Cloud Provider** 
* **Python**
* **Terraform**
* **Docker**
* **Airflow**
* **DBT**

<h4> Steps </h4>
<ol>
    <li>Register a GCP account and create a project </li>
    <li> Clone the project<code> $ git clone https://github.com/Hari-cbe/Used-Car-Price-data-analysiss.git </code></li>
    <li>Change the terraform <b><em>variable.tf</em></b> file to your required credentials.</li>
    <li>Use <code>terraform plan</code> to plan the project and use <code>terraform apply </code> in your terminal to create the necessary infrastructure in gcp  
    <li>Login into the VM instance. Install <a href="https://www.python.org/">Python</a>, <a href="https://docs.docker.com/get-docker/">Docker</a></li>
    <li>In your Code Editor( <a href="https://code.visualstudio.com/download">VS code</a> preferred ). Connect to the remote desktop.</li>
    <li>Use <code>docker pull haricbe/extending_airflow</code> to download the docker image</li>
    <li> Run the docker image <code>docker-compose up -d</code> to run the docker image in detach mdode </li>
    <li> forward the port in vs code <b>8080</b> and use the <b>localhost:8080</b> to run airflow in browser</li>  
    <li>Run The Script </li>
    <img src="https://github.com/Hari-cbe/Random-resourses/blob/main/Used-car-price-data/images/airflow.png?raw=true">
    <li>Data has been uploaded into gcs and Big Table has been created</li>
    <li>Install <a href="https://www.getdbt.com/">dbt Core</a> change the folder dir to used_car_price_analysis and run <code>dbt build</code> to run the transformations</li>
    <li>Once dbt is finished building it will have the output</li>
    <img src="https://github.com/Hari-cbe/Random-resourses/blob/main/Used-car-price-data/images/dbt.png?raw=true">
    <li>Used the transformed data to visualize in the <b>looker studio</b></li>
</ol>

* Once you are done, you will see a visual similar to what is show below
<img src="https://github.com/Hari-cbe/Random-resourses/blob/main/Used-car-price-data/images/US_used_car_price_Analysis_page-0001.jpg?raw=true">


