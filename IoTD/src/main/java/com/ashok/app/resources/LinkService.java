package com.ashok.app.resources;

/**

 * @author AshokKumar

 * <li>Obtain the data from the Urban Observatory API and send data for process the data. @see getRawdata() </li>
 * <li>After processing sleep for certain period then wakeup. </li>
 * <li>And get new set of historic data.</li>
 * <li>The historic data seems to be repeatable with 1 hour refresh rate.</li>
 * <li>Need to consult with the Urban Observatory department to finalize it.</li>
 * 
 * @throws IOException <p>If file not found from resources</p>
 * @throws InterruptedException <p>If thread is interrupted by some other thread</p>
 * @throws MqttException <p>If MQTT server not connected or refused for connection</p>
 */

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.eclipse.paho.client.mqttv3.MqttException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Component;

import com.ashok.app.ListenerDec;
import com.ashok.app.ListenerNewReq;
import com.ashok.app.Publish;
import com.ashok.app.Subscribe;

@Component
public class LinkService {
	@Autowired
	Subscribe sub;

	@Autowired
	Publish pub;

	@Autowired
	ListenerDec lstn;
	
	@Autowired
	ListenerNewReq newrq;

	private String Link;
	private String destination;
	final static Logger log = LoggerFactory.getLogger(LinkService.class);

	// No-arg Constructor for Spring IoC Usage
	public LinkService() {

	}

	public LinkService(String link) {
		Link = link;
	}

	public String getLink() {
		return Link;
	}

	public void setLink(String link) {
		Link = link;
	}

	public String getDestination() {
		return destination;
	}

	public void setDestination(String destination) {
		this.destination = destination;
	}

	public void startProcess() throws MqttException {
		try {
			Resource resource = new ClassPathResource("Apiurl.txt");
			BufferedReader reader = new BufferedReader(new InputStreamReader(resource.getInputStream()));
			String reqLink;

			while ((reqLink = reader.readLine()) != null) {
				sub.getRawData(reqLink);
			}

			newrq.newRequest();

		} catch (IOException e) {
			log.error("Could not reach API link file in resources: " + e.getMessage());
		} catch (Exception e) {
			log.error(e.getMessage());
		}
	}
}