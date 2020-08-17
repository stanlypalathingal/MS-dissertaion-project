package com.ashok.app;

/**
 * @author AshokKumar
 * Organisation- Newcastle University
 * Project - MSc dissertation
 * @since 1.0
 * 
 * */

import java.io.IOException;
import java.text.ParseException;
import java.util.Date;

import org.eclipse.paho.client.mqttv3.MqttException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;

import com.ashok.app.resources.LinkService;

@SpringBootApplication
@EnableAutoConfiguration
public class StartMain {
	private static String ipAddress, topicName, dcIpaddress, dcTopicName;
	private static Date startDt, endDt;
	static final Logger log = LoggerFactory.getLogger(StartMain.class);

	public static String getIpaddress() {
		return ipAddress;
	}

	public static String getTopicName() {
		return topicName;
	}

	public static String getDcIpaddress() {
		return dcIpaddress;
	}

	public static void setDcIpaddress(String dcIpaddress) {
		StartMain.dcIpaddress = dcIpaddress;
	}

	public static String getDcTopicName() {
		return dcTopicName;
	}

	public static void setDcTopicName(String dcTopicName) {
		StartMain.dcTopicName = dcTopicName;
	}

	public static Date getStartDt() {
		return startDt;
	}

	public static void setStartDt(Date startDt) {
		StartMain.startDt = startDt;
	}

	public static Date getEndDt() {
		return endDt;
	}

	public static void setEndDt(Date endDt) {
		StartMain.endDt = endDt;
	}

	public static void main(String[] args) throws IOException, MqttException, ParseException {
		ConfigurableApplicationContext context = SpringApplication.run(StartMain.class, args);
		try {

			ipAddress = args[0];
//			ipAddress = "54.80.131.227";
			topicName = "usbdata1";
			dcIpaddress = args[1];
//			dcIpaddress = "54.80.131.227";
			dcTopicName = "sensor/payload";
//			startDt = new SimpleDateFormat("dd-MM-yyyy HH:mm").parse(args[2]);
//			endDt = new SimpleDateFormat("dd-MM-yyyy HH:mm").parse(args[3]);

			context.getBean(LinkService.class).startProcess();

		} catch (IndexOutOfBoundsException e) {
			log.error("No arguments passed at main execution");
			System.exit(0);
		}
	}

}