package com.ashok.app;

import java.io.UnsupportedEncodingException;
import java.security.NoSuchAlgorithmException;
import java.security.spec.InvalidKeySpecException;
import java.util.List;
import java.util.stream.Collectors;

import javax.crypto.SecretKey;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.ashok.app.resources.DataService;
import com.ashok.app.resources.EncryptionService;
import com.ashok.app.resources.LinkService;

/**
 * @author AshokKumar
 * 
 * @throws MQTT exception if connection is aborted or couldn't establish with
 *              broker
 * 
 * @see while{repeat} to try for 4 retry to establish connection
 *      {@code getIpaddress(), getTopicName()} Fetch the ipaddress of MQTT
 *      broker running as main arg[] Fetch the Topic name for MQTT publish
 */

@Component
public class Publish {

	MqttClient client;
	MqttClient client2;
	final String PORT_NO = "1883";
	static final Logger log = LoggerFactory.getLogger(Publish.class);
	final String SALT = "boooom";
	@Autowired
	Subscribe sub;
	@Autowired
	ListenerDec listn;
	@Autowired
	LinkService lnk;
	@Autowired
	EncryptionService Enserv;

	public void connectNsend(String destiny) throws MqttException {
		boolean repeat = true;
		int retry = 0;
		while (repeat) {
			try {
				if (destiny.equals("decider")) {
					client = new MqttClient("tcp://" + StartMain.getIpaddress() + ":" + PORT_NO,
							StartMain.getTopicName());
				} else if (destiny.equals("datacentre")) {
					client = new MqttClient("tcp://" + StartMain.getDcIpaddress() + ":" + PORT_NO,
							StartMain.getDcTopicName());
				}

				MqttConnectOptions connOpts = new MqttConnectOptions();
				connOpts.setCleanSession(true); // true = Broker will clean all message when client disconnects. false =
												// Broker will retain message
				client.connect(connOpts);
				repeat = false;

			} catch (Exception e) {
				log.error(e.getMessage());
				retry += 1;
				if (retry <= 4) {
					log.warn("MQTT Connection lost with " + destiny + ". Retry no: " + retry);
					repeat = true;
				} else {
					break;
				}
			}
		}

		if (destiny == "decider") {

			List<String> dstPayld = (List<String>) sub.getPayloadData().stream().map(payload -> {
				String data = payload.getName() + "," + payload.getVariable() + "," + payload.getUnits();

				return data;
			}).distinct().sorted().collect(Collectors.toList());

			dstPayld.forEach(payload -> {
				try {
					publishData(payload, destiny);
				} catch (Exception e) {
					log.error("Error during Streaming API" + e.getMessage());
					e.printStackTrace();
				}
			});

			publishData("done", destiny); // Let the decider know that this is the end of dataset
			log.info("Delivered data to " + destiny + "..");
			listn.getDecision();
		}

	}

	public void EncryptNsend(String destiny, String key)
			throws MqttException, UnsupportedEncodingException, NoSuchAlgorithmException, InvalidKeySpecException {
		boolean repeat = true;
		int retry = 0;
		while (repeat) {
			try {
				client2 = new MqttClient("tcp://" + StartMain.getDcIpaddress() + ":" + PORT_NO,
						StartMain.getDcTopicName());

				MqttConnectOptions connOpts = new MqttConnectOptions();
				connOpts.setCleanSession(true); // true = Broker will clean all message when client disconnects. false =
												// Broker will retain message
				client2.connect(connOpts);
				repeat = false;

			} catch (Exception e) {
				retry += 1;
				if (retry <= 4) {
					log.error("MQTT Connection lost with " + destiny + ". Retry no: " + retry);
					log.error(e.getMessage());
					repeat = true;
				} else {
					break;
				}
			}
		}
		// Generate secret key based on python key.
		SecretKey symKey = Enserv.generateKey(key, SALT);
		for (DataService payload : sub.getPayloadData()) {
			String data = payload.getName() + "," + payload.getVariable() + "," + payload.getUnits() + ","
					+ payload.getDate() + "," + payload.getValue() + "," + payload.getFlag();

			String cipherData;
			EncryptionService encServ = new EncryptionService();
			cipherData = encServ.Encryption(data, symKey);
			publishData(cipherData, destiny);
		}
		String cipherDone;
		cipherDone = Enserv.Encryption("done", symKey);
		publishData(cipherDone, destiny); // ---> Confirm message to datacentre that all is complete
		
		log.info("Delivered to " + destiny + "..");
		sub.getPayloadData().clear();
		lnk.startProcess();
	}

	/**
	 * 
	 * To publish data through MQTTclient for decider/datacentre
	 * 
	 * @param payload {@value data}Gets the data from List object that holds the
	 *                sensor data
	 * @throws MQTTexception if publish fails to send payload <br>
	 *                       {@code #getBytes} converts the payload as bytes for
	 *                       sending through MQTTclient for Decider/Datacentre
	 */

	public void publishData(String payload, String destination) throws MqttException {
		if (destination.equals("decider")) {
			MqttMessage message = new MqttMessage(payload.getBytes());
			message.setQos(0);
			client.publish(StartMain.getTopicName(), message);
		} else {
			MqttMessage message = new MqttMessage(payload.getBytes());
			message.setQos(0);
			client2.publish(StartMain.getDcTopicName(), message);

		}
	}

}