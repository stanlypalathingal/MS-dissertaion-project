package com.ashok.app.resources;

import java.security.NoSuchAlgorithmException;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.KeySpec;
import java.util.Base64;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
public class EncryptionService {
	final static Logger log = LoggerFactory.getLogger(EncryptionService.class);

	public EncryptionService() {

	}

	public String Encryption(String plainTxt, SecretKey secretKey) {
		String cipherText = "";
		try {
			Cipher cipher = Cipher.getInstance("AES");
			byte[] plainTextByte = plainTxt.getBytes();// converting string into an array of bytes for encryption
			cipher.init(Cipher.ENCRYPT_MODE, secretKey);// initialising the cipher
			byte[] encryptedByte = cipher.doFinal(plainTextByte);// encrypts based on initialization of cipher

			// converting the array into a string
			Base64.Encoder encoder = Base64.getEncoder();
			cipherText = encoder.encodeToString(encryptedByte);// encoding the byte array to string

		} catch (Exception e) {
			log.error(e.getMessage());
		}
		return cipherText;
	}

	public SecretKey generateKey(String key, String salt) throws NoSuchAlgorithmException, InvalidKeySpecException {
		SecretKey secret;
		SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
		KeySpec spec = new PBEKeySpec(key.toCharArray(), salt.getBytes(), 65536, 256);
		SecretKey tmp = factory.generateSecret(spec);
		secret = new SecretKeySpec(tmp.getEncoded(), "AES");
		return secret;

	}
}
