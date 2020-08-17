package com.ashok.app;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import java.net.URL;
import java.net.URLConnection;
import java.text.SimpleDateFormat;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Date;
import java.util.HashSet;
import java.util.Set;

import org.json.JSONArray;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.stereotype.Component;

import com.ashok.app.resources.DataService;
import com.ashok.app.resources.LinkService;

/**
 * @author AshokKumar
 * @throws IOException If APIurl file not found at runtime
 * @param reqUrl from LinkService class given as API url {@code repeat} number
 *               of times incase API failure Data collection from UO- REST API
 *               after successful connection
 * @see https://jsoneditoronline.org for JSON data abstraction
 * @code JSONObject {data} gets the data presented in API @param arrData @throws
 *       NullPointerException If no data present for particular API then finally
 *       override next API link
 */

@Component
@ComponentScan({ "com.ashok.app.resources", "com.ashok.app" })
public class Subscribe {
	private Set<DataService> payloadData = new HashSet<>();
	final static Logger log = LoggerFactory.getLogger(Subscribe.class);
	URLConnection connectReq;
	URL urlObj;

	@Autowired
	LinkService lnk;

	public Set<DataService> getPayloadData() {
		return payloadData;
	}

	public void getRawData(String reqUrl) throws IOException {
		int repeat = 0, retry = 0;
		while (repeat == 0) {
			try {
				urlObj = new URL(reqUrl + getDate());
				connectReq = urlObj.openConnection();
				connectReq.connect();
				repeat = 1;
			} catch (Exception e) {
				retry += 1;
				log.warn("API connection lost.. Retry no: " + retry);
				log.error(e.getMessage());
				if (retry <= 4) {
					repeat = 0;
				} else {
					break;
				}
			}
		}

		BufferedReader stream = new BufferedReader(new InputStreamReader(connectReq.getInputStream()));
		String inputLine;
		StringBuffer bufferData = new StringBuffer();
		while ((inputLine = stream.readLine()) != null) {
			bufferData.append(inputLine);
		}

		JSONObject rawData = new JSONObject(bufferData.toString());
		JSONArray sensors = rawData.getJSONArray("sensors");

		for (int d = 0; d < sensors.length(); d++) {
			JSONObject arrData = sensors.getJSONObject(d);
			JSONObject data = new JSONObject(arrData.getJSONObject("data").toString());
			JSONArray sensorTy = data.names();
			try {
				for (Object eachTy : sensorTy) {
					JSONArray getData = data.getJSONArray((String) eachTy);
					for (int i = 0; i < getData.length(); i++) {
						JSONObject dataObj = getData.getJSONObject(i);

						String sensorNm = dataObj.getString("Sensor Name");
						String variable = dataObj.getString("Variable");
						String units = dataObj.getString("Units");
						long unixSeconds = dataObj.getLong("Timestamp");

						// Epochs returns too many long data which causes wrong calculation of unix time
						String sec = Long.toString(unixSeconds);
						Long Csec = Long.parseLong(sec.substring(0, 10));
						Date date = new java.util.Date(Csec * 1000L);
						SimpleDateFormat sdf = new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
						// Timezone reference for formatting
						sdf.setTimeZone(java.util.TimeZone.getTimeZone("GMT+1"));
						String formattedDate = sdf.format(date);

						Double value = dataObj.getDouble("Value");
						Boolean flag = dataObj.getBoolean("Flagged as Suspect Reading");

						DataService dataService = new DataService();
						dataService.setName(sensorNm);
						dataService.setVariable(variable);
						dataService.setUnits(units);
						dataService.setFlag(flag);
						dataService.setValue(value);
						dataService.setDate(formattedDate);
						payloadData.add(dataService);

					}
				}
			} catch (NullPointerException e) {
				log.error("No data in API : " + reqUrl + getDate());
			} finally {
				System.gc();
			}
		}
	}

	/**
	 * @return String that contains previous day date with day before previous date
	 *         Solely used this for the purpose UTC time from api is returned UTC
	 *         format is always 1 hour behind with current time
	 */

	private String getDate() {

//		For last 1 hour time period
		DateTimeFormatter dtFormat = DateTimeFormatter.ofPattern("yyyyMMddHHmm");
		String ZoneFrmDt = dtFormat.format(ZonedDateTime.now(ZoneId.of("Europe/London")).minusHours(2));
		String ZoneToDt = dtFormat.format(ZonedDateTime.now(ZoneId.of("Europe/London")).minusHours(1));

//		Custom date parameter
//		SimpleDateFormat smpFormat = new SimpleDateFormat("yyyyMMddHHmm");
//		String from = smpFormat.format(StartMain.getStartDt());
//		String to = smpFormat.format(StartMain.getEndDt());

//		For last 10 minutes time period
//		String from = dtFormat.format(LocalDateTime.now().minusMinutes(30));
//		String to = dtFormat.format(LocalDateTime.now().minusMinutes(10));

		return "starttime=" + ZoneFrmDt + "&endtime=" + ZoneToDt;
	}
}