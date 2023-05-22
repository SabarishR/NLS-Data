CREATE TABLE  `regression$model$prediction` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `MODEL_ID` int(11) NOT NULL,
  `INPUT` json NOT NULL,
  `OUTPUT` json NOT NULL,
  `CREATED_BY` varchar(200) DEFAULT NULL,
  `CREATED_ON` datetime NOT NULL,
  `UPDATED_BY` varchar(200) DEFAULT NULL,
  `UPDATED_ON` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_regression$model$prediction_1` (`MODEL_ID`),
  CONSTRAINT `FK_regression$model$prediction_1` FOREIGN KEY (`MODEL_ID`) REFERENCES `regression$model$information` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;