FROM balenalib/raspberry-pi-openjdk:8
#FROM openjdk:8
ADD target/Edge-decrypt.jar Edge-decrypt.jar
ENTRYPOINT ["java","-jar","Edge-decrypt.jar"]