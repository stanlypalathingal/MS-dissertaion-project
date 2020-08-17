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

@Component
public class ListenerNewReq implements MqttCallback {

	@Autowired
	Publish pub;

	@Autowired
	Subscribe sub;

	private MqttClient client2;
	private final String PORT_NO = "1883";
	private String SENSOR_TOPIC = "sensor_data_req";
	final static Logger log = LoggerFactory.getLogger(ListenerNewReq.class);

	public void newRequest() {
		log.debug("Waiting for next request..");
		try {

			client2 = new MqttClient("tcp://" + StartMain.getIpaddress() + ":" + PORT_NO, SENSOR_TOPIC);

			MqttConnectOptions conOpt = new MqttConnectOptions();
			conOpt.setKeepAliveInterval(60);
			conOpt.setCleanSession(false);
			client2.connect(conOpt);
			client2.setCallback(this);
			client2.subscribe(SENSOR_TOPIC);

		} catch (MqttException e) {
			log.error(e.getMessage() + " MQTT broker in Listener on new request " + e.getReasonCode());
		}

	}

	@Override
	public void connectionLost(Throwable cause) {
		// TODO Auto-generated method stub

	}

	@Override
	public void messageArrived(String topic, MqttMessage message) throws Exception {
//		log.info("From ListnerNewReq - " + topic + " - " + message.toString());
		log.debug("New request received..");
		pub.connectNsend("decider");
	}

	@Override
	public void deliveryComplete(IMqttDeliveryToken token) {
		// TODO Auto-generated method stub

	}

}
