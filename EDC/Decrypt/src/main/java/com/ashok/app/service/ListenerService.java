package com.ashok.app.service;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.ashok.app.Main;

@Component
public class ListenerService implements MqttCallback {
	MqttClient client;
	final int PORT_NO = 1883;
	final String SEN_TOPIC = "sensor/payload";
	final String KEY_TOPIC = "data/sym_key";
	@Autowired
	DecryptionService decSrv;

//	public void getConnection() {
//		try {
//			client = new MqttClient("tcp://" + Main.getBROKER_HOST() + ":" + PORT_NO, KEY_TOPIC);
//
//			MqttConnectOptions conOpt = new MqttConnectOptions();
//			conOpt.setKeepAliveInterval(60);
//			conOpt.setCleanSession(false);
//			client.connect(conOpt);
//			client.setCallback(this);
//			client.subscribe(KEY_TOPIC);
//			client.subscribe(SEN_TOPIC);
//
//		} catch (MqttException e) {
//			e.printStackTrace();
//			System.out.println(e.getMessage() + " - " + e.getReasonCode());
//		}
//	}

	@Override
	public void connectionLost(Throwable cause) {
		// TODO Auto-generated method stub

	}

	@Override
	public void messageArrived(String topic, MqttMessage message) throws Exception {

		if (topic.equals(KEY_TOPIC)) {
			// Setting up the cipher key to a variable in DecrytionService class file
			DecryptionService.setSymKey(decSrv.getKey(message.toString(), "boooom"));
			System.out.println("Received the symmetric key : " + message.toString());
			
		} 
	}

	@Override
	public void deliveryComplete(IMqttDeliveryToken token) {
		// TODO Auto-generated method stub

	}

}
