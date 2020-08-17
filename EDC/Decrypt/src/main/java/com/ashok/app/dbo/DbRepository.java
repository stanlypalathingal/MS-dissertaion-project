package com.ashok.app.dbo;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import com.ashok.app.SensorModel;

@Repository
public interface DbRepository extends MongoRepository<SensorModel, Integer> {

}
