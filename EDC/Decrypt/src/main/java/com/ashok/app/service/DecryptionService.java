package com.ashok.app.service;

import java.security.NoSuchAlgorithmException;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.KeySpec;
import java.util.Base64;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttPersistenceException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.ashok.app.SensorModel;
import com.ashok.app.dbo.DAOService;

@Component
public class DecryptionService {

	@Autowired
	DecryptionService sercObj;

	@Autowired
	SensorModel senM;

	@Autowired
	DAOService insertServ;

	@Autowired
	PayloadService pldSrv;

	private static SecretKey SymKey;
	private static MqttClient Client;
	static final Logger log = LoggerFactory.getLogger(DecryptionService.class);
	int counter = 0;
	long startTm, endTm;
	double timeTkn;

	public static SecretKey getSymKey() {
		return SymKey;
	}

	public static void setSymKey(SecretKey symKey) {
		SymKey = symKey;
	}

	public static MqttClient getClient() {
		return Client;
	}

	public static void setClient(MqttClient client) {
		Client = client;
	}

	public void decNstoreData(String cipherText)
			throws NoSuchAlgorithmException, InvalidKeySpecException, MqttPersistenceException, MqttException {
		
		SecretKey secretKey = getSymKey();
		String plainTxt = Decryption(cipherText, secretKey);
		if (counter == 0) {
			startTm = System.currentTimeMillis();
		}
		if (plainTxt.equals("done")) {
			endTm = System.currentTimeMillis();
			timeTkn = endTm - startTm;
			log.info("Time taken for decryption of " + counter + " records - " + timeTkn / 1000 + " seconds");
			counter = 0;
		}
		pldSrv.publishML(plainTxt, "datacentre", Client);
		counter = counter + 1;
//		senM.setVariables(plainTxt);
//		insertServ.add(senM);
//		log.info(senM.toString());

	}

	public SecretKey getKey(String key, String salt) throws NoSuchAlgorithmException, InvalidKeySpecException {

		SecretKey secret;
		SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
		KeySpec spec = new PBEKeySpec(key.toCharArray(), salt.getBytes(), 65536, 256);
		SecretKey tmp = factory.generateSecret(spec);
		secret = new SecretKeySpec(tmp.getEncoded(), "AES");
		return secret;
	}

	public String Decryption(String cipherText, SecretKey secretKey) {
		String plainText = "";
		try {
			Cipher cipher = Cipher.getInstance("AES");

			Base64.Decoder decoder = Base64.getDecoder();

			byte[] encryptedTextByte = decoder.decode(cipherText);
			cipher.init(Cipher.DECRYPT_MODE, secretKey);// initializing cipher
			byte[] decryptedByte = cipher.doFinal(encryptedTextByte);// decrypts based on cipher initialization

			plainText = new String(decryptedByte);// storing the decrypted array into a string

		} catch (Exception e) {
			log.error("Encryption exception : " + e.getMessage());
		}
		return plainText;
	}

}
