package com.ashok.app.dbo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.ashok.app.SensorModel;

@Component
public class DAOService {
	@Autowired
	DbRepository repo;
	
	public void add(SensorModel data) {
		repo.save(data);
	}

}
