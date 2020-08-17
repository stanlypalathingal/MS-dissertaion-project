package com.ashok.app.service;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.MqttPersistenceException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.ashok.app.Main;

@Component
public class PayloadService implements MqttCallback {
	MqttClient client;
	
	final int PORT_NO = 1883;
	final String SEN_TOPIC = "sensor/payload";
	private static final Logger log = LoggerFactory.getLogger(PayloadService.class);

	@Autowired
	DecryptionService decSrv;

	public void connectNgetpayload() {
		try {
			client = new MqttClient("tcp://" + Main.getBROKER_HOST() + ":" + PORT_NO, "payload");

			MqttConnectOptions conOpt = new MqttConnectOptions();
			conOpt.setKeepAliveInterval(60);
			conOpt.setCleanSession(false);
			client.connect(conOpt);
			client.setCallback(this);
			client.subscribe(SEN_TOPIC);
		} catch (MqttException e) {
			e.printStackTrace();
			log.error(e.getMessage() + " - " + e.getReasonCode());
		}
	}

	@Override
	public void connectionLost(Throwable cause) {
		// TODO Auto-generated method stub

	}

	@Override
	public void messageArrived(String topic, MqttMessage message) throws Exception {
//		log.info("From PayloadService - " + topic + " - " + message.toString());
		if (topic.equals(SEN_TOPIC)) {
			decSrv.decNstoreData(message.toString());
		}
	}

	@Override
	public void deliveryComplete(IMqttDeliveryToken token) {
		// TODO Auto-generated method stub

	}

	public void publishML(String payload, String destiny, MqttClient client) throws MqttPersistenceException, MqttException {
		log.info(payload);
		MqttMessage message = new MqttMessage(payload.getBytes());
		message.setQos(0);
		client.publish("machine_learning", message);
	}

}
