CREATE TABLE  `daywise$trans_reference$details` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `TRANSACTION_CODE` varchar(45) NOT NULL,
   `INPUT_ID` int(11) DEFAULT NULL,
  `TIME_STAMP` date NOT NULL,
  `EXPECTED_CHARGES` LONGTEXT DEFAULT NULL,
  `PRECISELY_CHARGED` LONGTEXT DEFAULT NULL,
  `NOT_PRECISELY_CHARGED` LONGTEXT DEFAULT NULL,
  `MISSING_CHARGE` LONGTEXT DEFAULT NULL,
  `MISSING_TAX_BUT_CHARGE_PRESENT` LONGTEXT DEFAULT NULL,
  `WRONG_CHARGE` LONGTEXT DEFAULT NULL,
  `REVENUE_LOSS_IN_CHARGE` LONGTEXT DEFAULT NULL,
  `REVENUE_EXTRA_IN_CHARGE` LONGTEXT DEFAULT NULL,
  `REVENUE_LOSS_IN_TAX` LONGTEXT DEFAULT NULL,
  `REVENUE_EXTRA_IN_TAX` LONGTEXT DEFAULT NULL,
  `REVENUE_BELOW_ACCEPTANCE_IN_CHARGE` LONGTEXT DEFAULT NULL,
  `REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE` LONGTEXT DEFAULT NULL,
  `IS_REGENERATED` bool DEFAULT NULL,
  `CREATED_BY` varchar(200) DEFAULT NULL,
  `CREATED_ON` datetime NOT NULL,
  `UPDATED_BY` varchar(200) DEFAULT NULL,
  `UPDATED_ON` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_daywise$trans_reference$details_1` (`INPUT_ID`),
  CONSTRAINT `FK_daywise$trans_reference$details_1` FOREIGN KEY (`INPUT_ID`) REFERENCES `transaction_input$output$details` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;