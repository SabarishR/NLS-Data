-- MySQL dump 10.13  Distrib 8.0.28, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: kollect_cba
-- ------------------------------------------------------
-- Server version	8.0.28-0ubuntu0.20.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `classification$model$information`
--

DROP TABLE IF EXISTS `classification$model$information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classification$model$information` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `MODEL_NAME` varchar(200) NOT NULL,
  `FILE_NAME` varchar(200) NOT NULL,
  `SCALAR_NAME` varchar(200) NOT NULL,
  `ACCURACY` float NOT NULL,
  `F1_SCORE` float DEFAULT NULL,
  `SENSITIVITY` float DEFAULT NULL,
  `SPECIFICITY` float DEFAULT NULL,
  `FALSE_POSITIVE` float DEFAULT NULL,
  `FALSE_NEGATIVE` float DEFAULT NULL,
  `DATASET_COLUMNS` varchar(5000) NOT NULL,
  `ONEHOT_LIST` varchar(5000) NOT NULL,
  `CREATED_BY` varchar(200) DEFAULT NULL,
  `CREATED_ON` datetime NOT NULL,
  `UPDATED_BY` varchar(200) DEFAULT NULL,
  `UPDATED_ON` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classification$model$information`
--

LOCK TABLES `classification$model$information` WRITE;
/*!40000 ALTER TABLE `classification$model$information` DISABLE KEYS */;
INSERT INTO `classification$model$information` VALUES (1,'xgb_callsession_classifier','Models/xgb_callsession_classifier202204201213.pkl','Models/xgb_callsession_scalar202204201213.pkl',0.995,0.995,1,0.999,0.001,0.005,'[\'CUSTOMER_RISK_STATUS\', \'INDUSTRY\', \'Late_Night\', \'Early_Morning\', \'Morning\', \'Late_Morning\', \'Afteroon\', \'Late_Afternoon\', \'Evening\', \'Late_Evening\', \'Night\', \'RESIDENCE_GB\', \'RESIDENCE_KE\', \'RESIDENCE_KG\', \'RESIDENCE_NA\', \'RESIDENCE_NG\', \'RESIDENCE_NL\', \'RESIDENCE_RW\', \'RESIDENCE_UG\', \'RESIDENCE_US\', \'RESIDENCE_ZW\', \'GENDER_MALE\', \'PROMISE_SUCCESS_YES\', \'REPAY_CURRENCY_USD\', \'CUSTOMER_STATUS_Deceased\', \'CUSTOMER_STATUS_Internal Customer\', \'CUSTOMER_STATUS_NORMAL CLIENT\', \'CUSTOMER_STATUS_Rts Mail/New Address Required\', \'CUSTOMER_STATUS_Statutory Entity\', \'CUSTOMER_STATUS_Watch List / Hotlist\', \'STAGE_COLLECTION\', \'STAGE_REPOSSESSION\']','[[\'KE\', \'US\', \'UG\', \'ZW\', \'NG\', \'KG\', \'NA\', \'RW\', \'NL\', \'AE\', \'GB\'], [\'MALE\', \'FEMALE\'], [\'YES\', \'NO\'], [\'KES\', \'USD\'], [\'NORMAL CLIENT\', \'CLOSED ACCOUNT\', \'Rts Mail/New Address Required\', \'Deceased\', \'Watch List / Hotlist\', \'Internal Customer\', \'Statutory Entity\'], [\'REPOSSESSION\', \'COLLECTION\', \'AGENT\']]','ML_USER','2022-04-20 12:13:24',NULL,NULL);
/*!40000 ALTER TABLE `classification$model$information` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-20 12:17:40
