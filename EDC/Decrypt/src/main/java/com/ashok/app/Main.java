package com.ashok.app;


import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;

import com.ashok.app.service.ServiceThreads;

@SpringBootApplication()
public class Main {
	
	static String BROKER_HOST, CONTAINER_BROKER;

	public static String getCONTAINER_BROKER() {
		return CONTAINER_BROKER;
	}

	public static void setCONTAINER_BROKER(String cONTAINER_BROKER) {
		CONTAINER_BROKER = cONTAINER_BROKER;
	}

	public static String getBROKER_HOST() {
		return BROKER_HOST;
	}

	public static void setBROKER_HOST(String bROKER_HOST) {
		BROKER_HOST = bROKER_HOST;
	}

	public static void main(String[] args) {

		ConfigurableApplicationContext context = SpringApplication.run(Main.class, args);
		BROKER_HOST = args[0];
		CONTAINER_BROKER=args[1];
		
		context.getBean(ServiceThreads.class).startService();	
	
	}

}
