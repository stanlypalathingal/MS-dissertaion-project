package com.ashok.app;

import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.stereotype.Component;

@Component
@Document
public class SensorModel {

	private String variables;

	public SensorModel() {

	}

	public SensorModel(String variables) {
		super();

		this.variables = variables;
	}

	public String getVariables() {
		return variables;
	}

	public void setVariables(String variables) {
		this.variables = variables;
	}

	@Override
	public String toString() {
		return variables;
	}
}
