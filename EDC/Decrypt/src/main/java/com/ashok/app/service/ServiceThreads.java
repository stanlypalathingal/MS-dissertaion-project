package com.ashok.app.service;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.ashok.app.Main;

@Component
public class ServiceThreads {

	@Autowired
	PayloadService pldSrv;

	@Autowired
	GetkeyService gtSrv;

	@Autowired
	DecryptionService decSrv;

//	String CONTAINER_HOST = "localhost";
	String PORT_NO = "1883";

	private static final Logger log = LoggerFactory.getLogger(ServiceThreads.class);

	public void startService() {
		Runnable nwThrd = () -> pldSrv.connectNgetpayload();
		new Thread(nwThrd).start();

		DecryptionService.setClient(getLocalBroker());

		gtSrv.connectNgetkey();

	}

	public MqttClient getLocalBroker() {
		MqttClient client = null;
		boolean repeat = true;
		int retry = 0;
		while (repeat) {
			try {

				client = new MqttClient("tcp://" + Main.getCONTAINER_BROKER() + ":" + PORT_NO, "MachineLearning");

				MqttConnectOptions connOpts = new MqttConnectOptions();
				connOpts.setCleanSession(false);
				client.connect(connOpts);
				repeat = false;

			} catch (Exception e) {
				log.error(e.getMessage());
				retry += 1;
				if (retry <= 4) {
					log.warn("MQTT Connection lost with local broker retry no: " + retry);
					repeat = true;
				} else {
					break;
				}
			}

		}
		return client;

	}
}
