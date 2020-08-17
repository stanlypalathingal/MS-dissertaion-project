package com.ashok.app.service;

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

import com.ashok.app.Main;

@Component
public class GetkeyService implements MqttCallback {
	@Autowired
	DecryptionService decSrv;

	@Autowired
	PayloadService pldSrv;

	MqttClient client;
//	final String HOST = "localhost";
	final int PORT_NO = 1883;
	final String KEY_TOPIC = "data/sym_key";

	private static final Logger log = LoggerFactory.getLogger(GetkeyService.class);

	public void connectNgetkey() {		
		
		try {
			client = new MqttClient("tcp://" + Main.getCONTAINER_BROKER() + ":" + PORT_NO, KEY_TOPIC);

			MqttConnectOptions conOpt = new MqttConnectOptions();
			conOpt.setKeepAliveInterval(60);
			conOpt.setCleanSession(false);
			client.connect(conOpt);
			client.setCallback(this);
			client.subscribe(KEY_TOPIC);

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
//		log.info("From GetKeyService - " + topic + " - " + message.toString());
		if (topic.equals(KEY_TOPIC)) {
			// Setting up the cipher key to a variable in DecrytionService class file
			DecryptionService.setSymKey(decSrv.getKey(message.toString(), "boooom"));
			log.info("Received the symmetric key : " + message.toString());

		}
	}

	@Override
	public void deliveryComplete(IMqttDeliveryToken token) {
		// TODO Auto-generated method stub

	}

}
