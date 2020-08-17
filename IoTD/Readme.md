# Efficient IoT Gateway for Urban Observatory API

Objective to develop an efficient IoT gateway that satisfies the following.
- Stream of data.
- Increase quality of data.
- Secure data transfer.

### Working principle
- Read the data from the pre-defined Newcastle Urban Observatory API link.
- Process the data from JSON to comma seperated value.
- Perform some filteration and aggregation with Machine Learning algorithm.
- Pass the cipher text to the datacenter from publish class.
- Decryption key will be provided by the decider with asymmetric encryption to the datacenter.
- Technology used - Spring Boot, Maven build tools, Docker.

### Docker image for pc
```bash
docker pull ashokjjk/urbanapi:pc (MQTT broker IP address)
```
### Docker image for Raspberry pi
```bash
 docker pull ashokjjk/urbanapi:pi (MQTT broker IP address)
```