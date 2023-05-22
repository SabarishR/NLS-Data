-- MySQL dump 10.13  Distrib 8.0.32, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: staging2
-- ------------------------------------------------------
-- Server version	8.0.32-0buntu0.20.04.1

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
-- Table structure for table `cstb$addl$text`
--

DROP TABLE IF EXISTS `cstb$addl$text`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cstb$addl$text` (
  `REFERENCE_NO` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `EVNT_SEQ_NO` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `ADDL_TEXT` varchar(300) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `TIME_STAMP` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `funds$transfer`
--

DROP TABLE IF EXISTS `funds$transfer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `funds$transfer` (
  `ID` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `EVENT_SEQ_NO` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `PRODUCT_CODE` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `USER_REF_NUMBER` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `DR_VALUE_DATE` date DEFAULT NULL,
  `CR_ACCOUNT_BRANCH` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `CR_ACCOUNT` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `CR_CCY` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `CR_AMOUNT` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `CR_VALUE_DATE` date DEFAULT NULL,
  `EXCHANGE_RATE` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `TRANSFER_TYPE` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `EVENT_CODE` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `DR_ACCOUNT_BRANCH` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `DR_ACCOUNT` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `DR_CCY` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `DR_AMOUNT` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SPREAD_CODE` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `LCY_EQUIV` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `MCK_NUMBER` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `CHECK_NUMBER` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `ENTRIES_STATUS` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `CHARGE_WHOM` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `RATE_TYPE` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `AFTER_RATE_CHANGE` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SOURCE_REF_NO` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `BY_ORDER_OF1` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `BY_ORDER_OF2` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `BY_ORDER_OF3` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `BY_ORDER_OF4` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `ULT_BENEFICIARY1` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `ULT_BENEFICIARY2` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `ULT_BENEFICIARY3` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `ULT_BENEFICIARY4` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `TIME_STAMP` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `PAYMENT_DETAILS` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nostro$statement`
--

DROP TABLE IF EXISTS `nostro$statement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nostro$statement` (
  `ID` int unsigned NOT NULL DEFAULT '0',
  `FORIEGN_BANK_ACCOUNT_NUMBER` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `ACCOUNT_NUMBER` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `CURRENCY` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `VALUE_DATE` date DEFAULT NULL,
  `ENTRY_DATE` date DEFAULT NULL,
  `CRF_TYPE` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FUND_CODE` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `SWIFT_AMOUNT` double NOT NULL DEFAULT '0',
  `TRANSACTION_TYPE` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `ACC_OWNER_REF_FOR_DEBIT` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `ACC_SERVICING_INSTITUTE_REF_FOR_CREDIT` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `SUPPLEMENTARY_DETAILS` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FIELD_N0` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FILE_NAME` varchar(400) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `ACTION` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `MESSAGE_TYPE` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `STATEMENT_SEQ_NO` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `TIME_STAMP` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `INPUTTER` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `AUTHORISER` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `DRAFT_ID` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `statement$detail$history`
--

DROP TABLE IF EXISTS `statement$detail$history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `statement$detail$history` (
  `AC_ENTRY_SR_NO` varchar(50) NOT NULL,
  `PERIOD_CODE` varchar(50) DEFAULT NULL,
  `FINANCIAL_CYCLE` varchar(50) DEFAULT NULL,
  `CUST_GL` varchar(1) DEFAULT NULL,
  `AC_BRANCH` varchar(5) DEFAULT NULL,
  `ACCOUNT_NO` varchar(50) NOT NULL,
  `LCY_AMOUNT` double DEFAULT NULL,
  `FCY_AMOUNT` double DEFAULT NULL,
  `VALUE_DT` date DEFAULT NULL,
  `TXN_INIT_DATE` date DEFAULT NULL,
  `TRN_DT` date DEFAULT NULL,
  `STMT_DT` date DEFAULT NULL,
  `EXTERNAL_REF_NO` varchar(500) DEFAULT NULL,
  `PRODUCT` varchar(50) DEFAULT NULL,
  `CATEGORY` varchar(50) DEFAULT NULL,
  `BANK_CODE` varchar(50) DEFAULT NULL,
  `RELATED_CUSTOMER` varchar(50) DEFAULT NULL,
  `RELATED_ACCOUNT` varchar(50) DEFAULT NULL,
  `RELATED_REFERENCE` varchar(50) DEFAULT NULL,
  `AMOUNT_TAG` varchar(50) DEFAULT NULL,
  `TRN_CODE` varchar(50) DEFAULT NULL,
  `DRCR_IND` varchar(1) DEFAULT NULL,
  `AC_CCY` varchar(3) DEFAULT NULL,
  `MODULE` varchar(50) DEFAULT NULL,
  `TRN_REF_NO` varchar(45) DEFAULT NULL,
  `INSTRUMENT_CODE` varchar(45) DEFAULT NULL,
  `INPUTTER` varchar(45) DEFAULT NULL,
  `AUTHORISER` varchar(45) DEFAULT NULL,
  `TIME_STAMP` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ismatched` int DEFAULT NULL,
  PRIMARY KEY (`AC_ENTRY_SR_NO`,`ACCOUNT_NO`) USING BTREE,
  KEY `Index_TRN_REF_NO` (`TRN_REF_NO`) USING BTREE,
  KEY `Index_Cheque` (`INSTRUMENT_CODE`),
  KEY `Index_Reports` (`ACCOUNT_NO`,`TRN_DT`,`TRN_CODE`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbl_recon_nostro$execution$history`
--

DROP TABLE IF EXISTS `tbl_recon_nostro$execution$history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbl_recon_nostro$execution$history` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `ACCOUNT_NO` varchar(500) NOT NULL,
  `RESPONSE` varchar(8000) NOT NULL,
  `CREATED_BY` varchar(200) DEFAULT NULL,
  `CREATED_ON` datetime NOT NULL,
  `UPDATED_BY` varchar(200) DEFAULT NULL,
  `UPDATED_ON` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbl_recon_nostro$matched$entry`
--

DROP TABLE IF EXISTS `tbl_recon_nostro$matched$entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbl_recon_nostro$matched$entry` (
  `PRI_entryId` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `fld_table$name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `FLD_ITEMTYPE` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE1` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE2` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE3` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE4` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE5` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE6` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE7` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE8` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE9` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE10` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `fld_account_Number` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `fld_UniqueReference` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `fld_MatchType` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `fld_unmatchComment` text CHARACTER SET latin1 COLLATE latin1_swedish_ci,
  `REPROCESS_STATUS` tinyint unsigned DEFAULT '0',
  `process_date` date DEFAULT NULL,
  `fld_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `authoriser` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `inputter` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `INPUTTER_COMMENT` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `AUTHORISER_COMMENT` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `INPUTTER_TIMESTAMP` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `AUTHORISER_TIMESTAMP` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `fld_AMOUNT` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT '0',
  `FLD_CURRENCY` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `MATCHED_REFERENCE` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbl_recon_nostro$unmatched$entry`
--

DROP TABLE IF EXISTS `tbl_recon_nostro$unmatched$entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbl_recon_nostro$unmatched$entry` (
  `PRI_entryId` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `fld_table$name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `FLD_ITEMTYPE` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE1` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE2` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE3` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE4` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE5` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE6` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE7` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE8` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE9` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE10` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `fld_account_Number` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `fld_UniqueReference` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `fld_MatchType` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `fld_unmatchComment` text CHARACTER SET latin1 COLLATE latin1_swedish_ci,
  `REPROCESS_STATUS` tinyint unsigned DEFAULT '0',
  `process_date` date DEFAULT NULL,
  `fld_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `authoriser` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `inputter` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `INPUTTER_COMMENT` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `AUTHORISER_COMMENT` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `INPUTTER_TIMESTAMP` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `AUTHORISER_TIMESTAMP` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `fld_AMOUNT` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT '0',
  `FLD_CURRENCY` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `MATCHED_REFERENCE` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbl_recon_nostro$unmatched$entry_manual`
--

DROP TABLE IF EXISTS `tbl_recon_nostro$unmatched$entry_manual`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbl_recon_nostro$unmatched$entry_manual` (
  `PRI_entryId` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `fld_table$name` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `fld_account_Number` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `fld_UniqueReference` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `fld_MatchType` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `fld_unmatchComment` text CHARACTER SET latin1 COLLATE latin1_swedish_ci,
  `process_date` date DEFAULT NULL,
  `fld_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `INPUTTER` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `authoriser` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `fld_AMOUNT` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT '0',
  `FLD_CURRENCY` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT 'KES',
  `MATCHED_REFERENCE` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `fld_itemtype` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE1` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE2` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE3` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `fld_UniqueReference4` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `fld_UniqueReference5` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE6` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE7` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE8` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE9` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `FLD_UNIQUEREFERENCE10` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbl_recon_nostro$virtual$possible$match`
--

DROP TABLE IF EXISTS `tbl_recon_nostro$virtual$possible$match`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbl_recon_nostro$virtual$possible$match` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `ACCOUNT_NO` varchar(500) NOT NULL,
  `STATEMENT_DETAIL_ID` varchar(1000) NOT NULL,
  `MATCH_TABLE` varchar(1000) NOT NULL,
  `MATCH_ID` varchar(1000) NOT NULL,
  `MATCH_AMOUNT` double NOT NULL,
  `VARIANCE` double NOT NULL,
  `ISMATCHED` tinyint(1) DEFAULT '0',
  `CREATED_BY` varchar(200) DEFAULT NULL,
  `CREATED_ON` datetime NOT NULL,
  `UPDATED_BY` varchar(200) DEFAULT NULL,
  `UPDATED_ON` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-25 15:02:27
