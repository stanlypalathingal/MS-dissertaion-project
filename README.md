The findings of this work are published in "Decision tree based user-centric security solution for critical IoT infrastructure"

The work simulates a reallife scenario and uses Machine learning methods to identify threats.

It was part of MS Data Science Dissertation.

# Introduction
This repository contains the files of the research project titled 

**DECISION TREE EMPOWERED DATA CLASSIFICATION IN EDGE AND CLOUD DATACENTRE**. 

The scripts used in the three components (SC, IoTD and EDC) are available in the folders with the respective names. The folder named ‘Graph’ contains the graphs and plots used in the document.

<img src="architecture.png" height="182" width="550" style="vertical-align:middle">

The folders named after the components contain the **Dockerfile** used to create the docker image. The docker images available here for the **armv32** architecture (Raspberry Pi) and may not run in ordinary systems. 
# Reproducibility 
In order to reproduce the system, the required system and software requirements are
* Three SSH enable Raspberry Pi with Docker installed. 
* A static IP (Broker)

The three components must run parallelly to reproduce the model. Docker images for the components are uploaded in the **www.dockerhub.com** and one must pull it to the system to execute it.
For the details of execution see the video named **Execution_Details.mp4** in the root directory

## 1. SC

Pull the image from the docker using the command
```bash 
docker pull stanlysac/sc:controller_pi_ip 
```

After pulling the image run it as follow 
```bash
docker run -it -v <Location_in_the_system>:/logs stanlysac/sc:controller_pi_ip <Mqtt ip>
```
Eg. 
```bash 
docker run -it -v /home/pi/Documents:/logs stanlysac/sc:controller_pi_ip 54.196.9.248 
```
	
Location_in_the_system is given to save the error details for further analysis

## 2. EDC

It requires a couple of docker images

```bash
docker pull ivanmarban/armhf-mongodb
docker pull eclipse-mosquitto
docker pull ashokjjk/benchmark:decrypt
docker pull stanlysac/edc:publish
docker pull stanlysac/edc:ml_pi
```

Once all the images are in the EDC system, the folder (EDC) contains a file named  **_run.sh_**  which has the scripts to run all the images together. Copy the file to the system and enable it executable. 
Run the files as  
```bash
./run.sh <Mqtt ip>  <delay>
```
The delay here means the time gap between the requests, and it is in seconds.
Eg: 
```bash
./run.sh  54.196.9.248  30
```

## 3. IoTD

Pull the image from the docker using the command
```bash
docker pull ashokjjk/urbanapi:pi
```
Execute the image as 	
```bash
docker run -d ashokjjk/urbanapi:pi <Mqtt ip>  <Mqtt ip>
```

Eg:  	
```bash
docker run -d ashokjjk/urbanapi:pi 54.196.9.248 54.196.9.248
```
