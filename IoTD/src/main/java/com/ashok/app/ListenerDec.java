package com.ashok.app;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.ashok.app.resources.LinkService;

@Component
public class ListenerDec implements MqttCallback {
	@Autowired
	Publish pub;
	@Autowired
	LinkService lnk;
	@Autowired
	Subscribe sub;

	private MqttClient client;

	private final String PORT_NO = "1883";
	private String SENSOR_TOPIC = "sensor_sym_key";
	long stm, etm, timetaken;
	final static Logger log = LoggerFactory.getLogger(ListenerDec.class);

	public void getDecision() {
		stm = System.currentTimeMillis();
		log.debug("Waiting for decision..");
		try {
			client = new MqttClient("tcp://" + StartMain.getIpaddress() + ":" + PORT_NO, SENSOR_TOPIC);

			MqttConnectOptions conOpt = new MqttConnectOptions();
			conOpt.setKeepAliveInterval(60);
			conOpt.setCleanSession(false); // False is considered as "reliable" delivery
			client.connect(conOpt);
			client.setCallback(this);
			client.subscribe(SENSOR_TOPIC);
		} catch (MqttException e) {
			e.printStackTrace();
			log.error("MQTT broker exception in getting decision : " + e.getReasonCode() + e.getMessage());
		}
	}

	@Override
	public void connectionLost(Throwable cause) {

	}

	@Override
	public void messageArrived(String topic, MqttMessage message) throws Exception {
//		log.info("From ListenerDec - "+ topic + " - " + message.toString());
		
		if (topic.equals(SENSOR_TOPIC)) {
			// If the message is not abort get the symmetric key and go for next process

			if (message.toString().equals("abort")) {
				log.info("Decision received to: " + message.toString());
				log.warn("Clearing data on abort decision..");
				sub.getPayloadData().clear();
				lnk.startProcess();
			} else {
				log.info("Decision received with key: " + message);
				log.info("Encrypting and sending to datacentre..");
				etm = System.currentTimeMillis();
				timetaken = etm - stm;
				log.info("Time taken : " + timetaken);

				pub.EncryptNsend("datacentre", message.toString());

			}
		}
	}

	@Override
	public void deliveryComplete(IMqttDeliveryToken token) {

	}
}