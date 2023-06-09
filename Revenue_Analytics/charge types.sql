-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	8.0.21


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


--
-- Create schema nlscore_sidian
--

CREATE DATABASE IF NOT EXISTS nlscore_sidian;
USE nlscore_sidian;

--
-- Definition of table `bnk_charge$types`
--

DROP TABLE IF EXISTS `bnk_charge$types`;
CREATE TABLE `bnk_charge$types` (
  `id` varchar(255) NOT NULL,
  `CALCULATION_BASIS` varchar(255) DEFAULT NULL,
  `CURRENCY` varchar(255) DEFAULT NULL,
  `FLAT_AMOUNT` varchar(255) DEFAULT NULL,
  `CALC_TYPE` text,
  `PERCENTAGE` text,
  `UPTO_AMOUNT` text,
  `MINIMUM_AMOUNT` text,
  `MAXIMUM_AMOUNT` text,
  `CATEGORY_ACCOUNT` varchar(255) DEFAULT NULL,
  `DEBIT_TXN_CODE` varchar(255) DEFAULT NULL,
  `CREDIT_TXN_CODE` varchar(255) DEFAULT NULL,
  `DESCRIPTION` varchar(255) DEFAULT NULL,
  `DEFAULT_CURRENCY` varchar(255) DEFAULT NULL,
  `TAX_CODE` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bnk_charge$types`
--

/*!40000 ALTER TABLE `bnk_charge$types` DISABLE KEYS */;
INSERT INTO `bnk_charge$types` (`id`,`CALCULATION_BASIS`,`CURRENCY`,`FLAT_AMOUNT`,`CALC_TYPE`,`PERCENTAGE`,`UPTO_AMOUNT`,`MINIMUM_AMOUNT`,`MAXIMUM_AMOUNT`,`CATEGORY_ACCOUNT`,`DEBIT_TXN_CODE`,`CREDIT_TXN_CODE`,`DESCRIPTION`,`DEFAULT_CURRENCY`,`TAX_CODE`) VALUES 
 ('ACCEPT',NULL,'KES','2000.00',NULL,NULL,NULL,NULL,NULL,'52330','525','525','LC ACCEPTANCE CHARGES',NULL,'3'),
 ('ACCTCLOSE',NULL,'KES','0.00','FLAT',NULL,NULL,NULL,NULL,'52321','522','522','Account Closure Charges',NULL,'3'),
 ('ACTOMP',NULL,'KES','75.00',NULL,NULL,NULL,NULL,NULL,'52326','260','260','Account to Mpesa',NULL,'3'),
 ('ACTOMP1','PERCENTAGE','KES',NULL,'LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL','0^0^0^0^0^0','20000.00^30000.00^40000.00^50000.00^60000.00','75.00^145.00^170.00^215.00^245.00^265.00',NULL,'52326','260','260','ACCOUNT TO M-PESA COMMISSION',NULL,'3'),
 ('ACTRNCOMM',NULL,'KES','50.00',NULL,NULL,NULL,NULL,NULL,'52319','780','780','Transfer Commission',NULL,'3'),
 ('ACTTRAN',NULL,'KES','50.00',NULL,NULL,NULL,NULL,NULL,'52263','260','260','K-Rep Account to Account Transfer',NULL,'3'),
 ('ADV',NULL,'KES','1000.00','FLAT',NULL,NULL,NULL,NULL,'52230','522','522','LC ADVISING COMM',NULL,'3'),
 ('AFDAF',NULL,'KES','100.00',NULL,NULL,NULL,NULL,NULL,'52324','172','173','Affidavit Fees',NULL,'3'),
 ('AGEDEPBNK','PERCENTAGE','KES',NULL,'LEVEL','0.000000001',NULL,NULL,'0','52265','933','933','Agent Deposit Commission',NULL,'3'),
 ('AGEDEPCM','PERCENTAGE','KES',NULL,'LEVEL^LEVEL^LEVEL^LEVEL^LEVEL','0.000000001^0.000000001^0.000000001^0.000000001^0.000000001','10000.00^20000.00^50000.00^100000.00','10.00^15.00^20.00^30.00^50.00',NULL,'52265','933','933','Agent Deposit Commission',NULL,'3'),
 ('AGEWITHBNK','PERCENTAGE','KES',NULL,'LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL','0.00001^0.0001^0.00001^0.00001^0.00001^0.000001^0.000001^0.000001','2500.00^5000.00^10000.00^20000.00^35000.00^50000.00^100000.00','15.00^25.00^40.00^65.00^80.00^90.00^120.00^130.00',NULL,'52265','934','934','Agent Withdrawl Commission',NULL,'3'),
 ('AGEWITHCM','PERCENTAGE','KES',NULL,'LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL','0.00001^0.0001^0.00001^0.00001^0.00001^0.0000001^0.000001^0.000001','2500.00^5000.00^10000.00^20000.00^35000.00^50000.00^100000.00','10.00^20.00^35.00^60.00^75.00^90.00^100.00^120.00',NULL,'52265','934','934','Agent Withdrawl Commission',NULL,'3'),
 ('ATMCHG',NULL,'KES','30.00','FLAT',NULL,NULL,NULL,NULL,'52260','269','269','ATM CHARGE',NULL,'3'),
 ('ATMCHGSTF',NULL,'KES','0.00','FLAT',NULL,NULL,NULL,NULL,'52260','269','269','ATM CHARGE',NULL,NULL),
 ('ATMVISA',NULL,'KES','150.00','FLAT',NULL,NULL,NULL,NULL,'52260','269','269','VISA CHARGE',NULL,'3'),
 ('ATMVISASTF',NULL,'KES','35.00','FLAT',NULL,NULL,NULL,NULL,'52260','269','269','VISA CHARGE',NULL,'3'),
 ('BCQ',NULL,'KES','100.00',NULL,NULL,NULL,NULL,NULL,'52310','244','244','Bankers Chq Comm - Client',NULL,'3'),
 ('BCQB',NULL,'KES','70.00',NULL,NULL,NULL,NULL,NULL,'52310','244','244','Bankers Chq Comm - Client',NULL,'3'),
 ('BILLS',NULL,'KES','2.50',NULL,NULL,NULL,NULL,NULL,'KES1100700010000','192','193','STAMP DUTY ON CHEQUES',NULL,'3'),
 ('BONDA','PERCENTAGE','KES',NULL,'LEVEL','1.50',NULL,'1000.00',NULL,'52330','242','242','Commitment Fees',NULL,'3'),
 ('BONDAM',NULL,'KES','3500.00','FLAT',NULL,NULL,NULL,NULL,'52330','242','242','General Amendment Guarantees',NULL,'3'),
 ('BONDC','PERCENTAGE','KES',NULL,'LEVEL','0.50',NULL,'500.00',NULL,'52306','659','660','Commission on Guranttee',NULL,'3'),
 ('BONDCANCEL',NULL,'KES','2500.00','FLAT',NULL,NULL,NULL,NULL,'52330','242','242','Cancellation of Uncollected Guarant',NULL,'3'),
 ('BONDCL',NULL,'KES','5000.00','FLAT',NULL,NULL,NULL,NULL,'52330','242','242','Guarantee Claim Handling Commission',NULL,'3'),
 ('BONDF','PERCENTAGE','KES',NULL,'LEVEL','1.50',NULL,'1000.00',NULL,'52330','241','241','Appraisal Fees',NULL,'3'),
 ('BONDSW',NULL,'KES','2500.00','FLAT',NULL,NULL,NULL,NULL,'52330','242','242','Guarantees swift commission',NULL,'3'),
 ('CASHAND','PERCENTAGE','KES',NULL,'LEVEL^LEVEL','0^0.1','100000.00','1000.00','10000.00','52000','361','351','CASH HANDLING CHARGES',NULL,'3'),
 ('CASHDEP','PERCENTAGE','KES',NULL,'LEVEL','0',NULL,NULL,NULL,'52052','961','962','Cash Deposit Charges',NULL,'3'),
 ('CASHWDWL','PERCENTAGE','KES',NULL,'LEVEL','0',NULL,NULL,NULL,'52052','961','962','Cash Withdrawal Charges',NULL,'3'),
 ('CHIKCHAT',NULL,'KES','2000.00',NULL,NULL,NULL,NULL,NULL,'52324','172','173','Chikola Loan Chattel Fees',NULL,'3'),
 ('CHQCLEAR','PERCENTAGE','KES',NULL,'LEVEL','75',NULL,NULL,NULL,'52312','915','914','UPCOUNTRY',NULL,'3'),
 ('CHQIPO',NULL,'KES','200.00','FLAT',NULL,NULL,NULL,NULL,'52310','244','244','Banker\'s Cheque Chgs-IPO',NULL,'3'),
 ('CHQKREP','PERCENTAGE','KES',NULL,'LEVEL','0.25',NULL,'100.00','10000.00','52312','915','914','CHEQUE COMMISSION',NULL,'3'),
 ('CHQREC',NULL,'USD','15.00',NULL,NULL,NULL,NULL,NULL,'52006','246','246','FX Commision','USD','3'),
 ('CHQSENT',NULL,'USD','15.00',NULL,NULL,NULL,NULL,NULL,'52006','246','246','FX Commision','USD','3'),
 ('CHQUNPAID',NULL,'KES','1500.00',NULL,NULL,NULL,NULL,NULL,'52004','172','173','UNPAID CHEQUE CHARGE',NULL,'3'),
 ('CHQUNPAIDIN',NULL,'KES','350.00','FLAT',NULL,NULL,NULL,NULL,'52312','961','962','UNPAID CHEQUE INWARD',NULL,'3'),
 ('CHQUNPAIDOP',NULL,'KES','0.00','FLAT',NULL,NULL,NULL,NULL,'52312','961','962','UNPAID CHEQUE CHARGE',NULL,'3'),
 ('CHQUNPAIDOU',NULL,'KES','500.00','FLAT',NULL,NULL,NULL,NULL,'52312','961','962','UNPAID CHEQUE CHARGE',NULL,'3'),
 ('CHQUNPAIDPA',NULL,'KES','850.00','FLAT',NULL,NULL,NULL,NULL,'52312','961','962','UNPAID CHEQUE INWARD',NULL,'3'),
 ('CHQUNPAIDPO',NULL,'KES','2500.00','FLAT',NULL,NULL,NULL,NULL,'52312','961','962','UNPAID CHEQUE CHARGE',NULL,'3'),
 ('CHQUNPAIDQU',NULL,'KES','850.00','FLAT',NULL,NULL,NULL,NULL,'52312','961','962','UNPAID CHEQUE INWARD',NULL,'3'),
 ('CHQUNPAIDRE',NULL,'KES','300.00','FLAT',NULL,NULL,NULL,NULL,'52312','961','962','UNPAID CHEQUE RETURN',NULL,'3'),
 ('CHQUNPAIDRN',NULL,'KES','500.00','FLAT',NULL,NULL,NULL,NULL,'52312','961','962','UNPAID CHEQUE RETURN',NULL,'3'),
 ('CHQUNPAIDT',NULL,'KES','850.00','FLAT',NULL,NULL,NULL,NULL,'52000','961','962','UNPAID CHEQUE CHARGE',NULL,'3'),
 ('CHQUNPAIDTA',NULL,'KES','100.00','FLAT',NULL,NULL,NULL,NULL,'52312','961','962','UNPAID CHEQUE CHARGE',NULL,'3'),
 ('CHQUNPAIDTU',NULL,'KES','300.00','FLAT',NULL,NULL,NULL,NULL,'52312','961','962','UNPAID CHEQUE RETURN',NULL,'3'),
 ('CHQUNPAIDUE',NULL,'KES','300.00','FLAT',NULL,NULL,NULL,NULL,'52312','961','962','UNPAID CHEQUE RETURN',NULL,'3'),
 ('CLDCHG','PERCENTAGE','KES',NULL,'LEVEL','23',NULL,NULL,NULL,'52001','213','213','EXIT TAX',NULL,'3'),
 ('CLO',NULL,'KES','500.00',NULL,NULL,NULL,NULL,NULL,'52321','106','106','ACCOUNT CLOSURE',NULL,'3'),
 ('CMTFEES','PERCENTAGE','KES',NULL,'LEVEL','1.5',NULL,NULL,NULL,'52211','242','242','Committement fees',NULL,'3'),
 ('CMTFEESCCS','PERCENTAGE','KES',NULL,'LEVEL','1.5',NULL,NULL,NULL,'52211','242','242','Committement fees',NULL,'3'),
 ('COMRET','PERCENTAGE','KES',NULL,'LEVEL','1.5',NULL,NULL,NULL,'52211','242','242','Committement fees',NULL,'3'),
 ('CONFIRM',NULL,'KES','2000.00',NULL,NULL,NULL,NULL,NULL,'52330','645','517','LC CONFIRMATION CHARGES',NULL,'3'),
 ('CORP',NULL,'KES','2.50',NULL,NULL,NULL,NULL,NULL,'KES1100700010000','192','193','STAMP DUTY ON CHEQUES',NULL,NULL),
 ('CORRBKCHG',NULL,'KES','0.00',NULL,NULL,NULL,NULL,NULL,'52110','209','209','CORR BANK CHGS',NULL,'3'),
 ('CRBCHARGE',NULL,'KES','0.00',NULL,NULL,NULL,NULL,NULL,'KES1610400010999','422','422','CRB charges',NULL,NULL),
 ('CRDSTOP',NULL,'KES','250.00','FLAT',NULL,NULL,NULL,NULL,'52000','961','962','CARD STOP CHARGE',NULL,'3'),
 ('CUST',NULL,'KES','2.50',NULL,NULL,NULL,NULL,NULL,'KES1100700010000','192','193','STAMP DUTY ON CHEQUES',NULL,'3'),
 ('DCU',NULL,'KES','100.00',NULL,NULL,NULL,NULL,NULL,'52310','244','244','Bankers Chq Comm - Client',NULL,'3'),
 ('DCU.NC',NULL,'KES','300.00',NULL,NULL,NULL,NULL,NULL,'52310','244','244','Bankers Chq Comm - Non Client',NULL,'3'),
 ('DCU.NEW',NULL,'KES','100.00',NULL,NULL,NULL,NULL,NULL,'52310','244','244','Bankers Chq Comm - Client',NULL,'3'),
 ('DDCOMM','PERCENTAGE','KES',NULL,'BAND','0',NULL,NULL,NULL,'52101','203','202','DD Issue Commission',NULL,'3'),
 ('DESCRIP',NULL,'KES','1500.00',NULL,NULL,NULL,NULL,NULL,'52330','528','528','LC DESCRIPANCES CHARGES',NULL,'3'),
 ('DFOR',NULL,'KES^EUR^USD^GBP','0.00^10.00^12.00^7.00',NULL,NULL,NULL,NULL,NULL,'52310','244','244','Bankers Chq Comm - Foreign',NULL,'3'),
 ('DISCOUNTED','PERCENTAGE','KES',NULL,'BAND','10',NULL,NULL,NULL,'51000','390','391','Discounted Cheque',NULL,'3'),
 ('DNCU',NULL,'KES','300.00',NULL,NULL,NULL,NULL,NULL,'52310','244','244','Bankers Chq Comm - Non Client',NULL,'3'),
 ('DSF',NULL,'KES','100.00',NULL,NULL,NULL,NULL,NULL,'52302','244','244','Bankers Chq Comm - Schl Fees',NULL,'3'),
 ('DSTAF',NULL,'KES','50.00',NULL,NULL,NULL,NULL,NULL,'52310','244','244','Bankers Chq Comm - Staff',NULL,'3'),
 ('EEC','PERCENTAGE','KES',NULL,'LEVEL','3',NULL,NULL,'10000.00','52000','682','682','EXCESS & ENC COMMISSIONS',NULL,'3'),
 ('EECL','PERCENTAGE','KES',NULL,'LEVEL','3',NULL,'500.00',NULL,'52314','682','682','EXCESS & ENC COMMISSIONS',NULL,'3'),
 ('EFT',NULL,'KES','400.00',NULL,NULL,NULL,NULL,NULL,'52226','245','245','Commission on EFT',NULL,'3'),
 ('EFTNOCHARGE',NULL,'KES','0.00',NULL,NULL,NULL,NULL,NULL,'52000','961','962','EFT Salary Charge',NULL,'3'),
 ('EFTOUT',NULL,'KES','100.00',NULL,NULL,NULL,NULL,NULL,'52312','245','245','Commission on EFT',NULL,'3'),
 ('EFTSAL',NULL,'KES','100.00','FLAT',NULL,NULL,NULL,NULL,'52000','961','962','EFT Salary Charge',NULL,'3'),
 ('EFTSALO',NULL,'KES','100.00',NULL,NULL,NULL,NULL,NULL,'52510','961','962','EFT Salary Charge',NULL,'3'),
 ('EFTSTF',NULL,'KES','100.00',NULL,NULL,NULL,NULL,NULL,'52226','245','245','Commission on EFT',NULL,'3'),
 ('EFTSTFIB',NULL,'KES','100.00',NULL,NULL,NULL,NULL,NULL,'52333','245','245','Commission on EFT IB',NULL,'3'),
 ('EFTUNPDCHG',NULL,'KES','500.00','FLAT',NULL,NULL,NULL,NULL,'52312','961','962','UNPAID CHEQUE CHARGE',NULL,'3'),
 ('EXCISE2',NULL,'KES^USD','0.00^2.00','FLAT^FLAT',NULL,NULL,NULL,NULL,'KES1725700010000','464','465','EXCISE DUTY',NULL,NULL),
 ('EXCISE200',NULL,'KES','200.00','FLAT',NULL,NULL,NULL,NULL,'KES1725700010000','464','465','EXCISE DUTY',NULL,NULL),
 ('EXCISE50',NULL,'KES','50.00','FLAT',NULL,NULL,NULL,NULL,'KES1725700010000','464','465','EXCISE DUTY',NULL,NULL),
 ('EXCISEDUTY','PERCENTAGE','KES',NULL,'LEVEL','20.00',NULL,NULL,NULL,'KES1725700010000','464','465','EXCISE DUTY DIRECT COLLECTION',NULL,NULL),
 ('EXCISEDUTY1',NULL,'KES','50.00','FLAT',NULL,NULL,NULL,NULL,'KES1725700010000','464','465','EXCISE DUTY',NULL,NULL),
 ('FCYCOM','PERCENTAGE','USD',NULL,'LEVEL','1.5',NULL,NULL,NULL,'52301','49','49','Fcy Lodgements',NULL,'3'),
 ('FCYCOM1','PERCENTAGE','USD',NULL,'LEVEL','1',NULL,NULL,NULL,'52301','49','49','Fcy Withdrawals',NULL,'3'),
 ('FCYD','PERCENTAGE','KES^USD^EUR^GBP',NULL,'LEVEL^LEVEL^LEVEL^LEVEL','0^0.5^0.5^0.5',NULL,'10.00^8.00^6.00','200.00^160.00^120.00','52003','195','196','FCY DEPOSITS',NULL,'3'),
 ('FCYSALE','PERCENTAGE','KES',NULL,'LEVEL','0',NULL,NULL,NULL,'52003','195','196','Chgs on Sales of Foreign Currency',NULL,'3'),
 ('FCYW','PERCENTAGE','KES^USD',NULL,'LEVEL^LEVEL','0^0.00000001',NULL,'5.00',NULL,'52001','195','196','FCY WITHDRAWALS',NULL,'3'),
 ('FLEXXY',NULL,'KES','750.00','FLAT',NULL,NULL,NULL,NULL,'52250','347','346','FLexxy Current Account',NULL,'3'),
 ('FTKCHG',NULL,'KES','50.00','FLAT',NULL,NULL,NULL,NULL,'52265','994','994','VBS FT to Own K-Rep Acc Charge',NULL,'3'),
 ('FTOCHG',NULL,'KES','50.00','FLAT',NULL,NULL,NULL,NULL,'52265','995','995','VBS FT to Own Account Charge',NULL,'3'),
 ('FTVBS',NULL,'KES','50.00','FLAT',NULL,NULL,NULL,NULL,'52329','995','995','VBS FT to Own Account Charge',NULL,'3'),
 ('FXCOM','PERCENTAGE','KES',NULL,'LEVEL','1',NULL,NULL,NULL,'52301','49','49','Forex Commission',NULL,'3'),
 ('FXCOMM',NULL,'USD','20.00',NULL,NULL,NULL,NULL,NULL,'52006','246','246','FX Commision','USD','3'),
 ('FXCOMMCHQ',NULL,'USD','5.00',NULL,NULL,NULL,NULL,NULL,'52006','246','246','FX Commision on Cheques','USD','3'),
 ('FXCOMMEUR',NULL,'USD','20.00',NULL,NULL,NULL,NULL,NULL,'52006','246','246','Foreign Exchange Commision','USD','3'),
 ('FXCOMMGBP',NULL,'USD','20.00',NULL,NULL,NULL,NULL,NULL,'52006','246','246','Foreign Exchange Commision','USD','3'),
 ('HANDLIN',NULL,'KES','1000.00',NULL,NULL,NULL,NULL,NULL,'52330','524','524','LC HANDLING CHARGES',NULL,'3'),
 ('IMCHAT',NULL,'KES','2000.00',NULL,NULL,NULL,NULL,NULL,'52324','172','173','Individual Micrifinance Chattel Fee',NULL,'3'),
 ('INDEMN',NULL,'KES','1000.00',NULL,NULL,NULL,NULL,NULL,'52330','540','540','LC INDEMNITY CHARGES',NULL,'3'),
 ('INREMITCHG',NULL,'KES^USD','0.00^20.00','FLAT^FLAT',NULL,NULL,NULL,NULL,'52110','209','209','Inward REMIT Charges',NULL,'3'),
 ('INSWIFTCHG',NULL,'KES^USD','0.00^20.00','FLAT^FLAT',NULL,NULL,NULL,NULL,'52006','224','224','Inward SWIFT Charges',NULL,'3'),
 ('INTELEXCHG','PERCENTAGE','KES',NULL,'BAND','0',NULL,NULL,NULL,'52109','208','208','Inward TELEX Charges',NULL,'3'),
 ('JHCHAT',NULL,'KES','2000.00',NULL,NULL,NULL,NULL,NULL,'52324','172','173','Juhudi Loan Chattel Fees',NULL,'3'),
 ('JSLCASHHAND','PERCENTAGE','KES^USD^EUR',NULL,'LEVEL^LEVEL^LEVEL^LEVEL','0^0.1^0.5^0.5','50000.00',NULL,'10000.00^200.00','52000','361','351','JSL CASH HANDLING CHARGES',NULL,'3'),
 ('KCBCHG',NULL,'KES','60.00','FLAT',NULL,NULL,NULL,NULL,'52260','269','269','ATM CHARGE',NULL,'3'),
 ('KCBCHGSTF',NULL,'KES','50.00','FLAT',NULL,NULL,NULL,NULL,'52260','269','269','ATM CHARGE',NULL,'3'),
 ('KITSCOMM','PERCENTAGE','KES',NULL,'LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL','0.00001^0.00001^0.00001^0.00001^0.00001^0.00001^0.00001^0.00001^0.00001','501.00^5001.00^10001.00^20001.00^50001.00^100001.00^200001.00^500001.00','0.00^8.40^18.40^28.40^48.40^68.40^108.40^148.40^188.40',NULL,'52339','934','934','Pesalink Commission',NULL,'3'),
 ('KKCHAT',NULL,'KES','2000.00',NULL,NULL,NULL,NULL,NULL,'52324','172','173','Kati kati Loan Chattel Fees',NULL,'3'),
 ('KRACHARGE',NULL,'KES','350.00',NULL,NULL,NULL,NULL,NULL,'52333','808','808','KRA IB payment charge','KES','3'),
 ('KREPEAP',NULL,'KES','500.00','FLAT',NULL,NULL,NULL,NULL,'52338','641','642','EAP CHARGES',NULL,'3'),
 ('LAPFEE','PERCENTAGE','KES',NULL,'LEVEL','1.5',NULL,'1500.00',NULL,'52000','241','241','Loan App Fee',NULL,'3'),
 ('LAPFEEMSHA','PERCENTAGE','KES',NULL,'LEVEL','1.5',NULL,'1000.00',NULL,'52200','241','241','Loan App Fee- Mshahara',NULL,'3'),
 ('LAPPFEES','PERCENTAGE','KES',NULL,'LEVEL','1.5',NULL,'150.00',NULL,'52200','241','241','Loan Application Group Loan',NULL,'3'),
 ('LAPPFEES2',NULL,'KES','150.00','FLAT',NULL,NULL,NULL,NULL,'52200','241','241','Loan Application2 Group Loan',NULL,'3'),
 ('LAPPFEESIPO','PERCENTAGE','KES',NULL,'LEVEL','1.5',NULL,'1000.00',NULL,'52200','241','241','Loan Application Group Loan',NULL,'3'),
 ('LAPRFE','PERCENTAGE','KES',NULL,'LEVEL','1.5',NULL,'1500.00',NULL,'52200','241','241','Loan Appraisal Retail Loans',NULL,'3'),
 ('LCAMEND',NULL,'KES','1500.00',NULL,NULL,NULL,NULL,NULL,'52330','523','523','LC AEMNDMENT CHARGES',NULL,'3'),
 ('LCAMMEND',NULL,'KES','2000.00','FLAT',NULL,NULL,NULL,NULL,'52345','523','523','LC Amendment Commission',NULL,'3'),
 ('LCEXPADVC',NULL,'KES','2500.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC EXPORT ADVISING COMM CLIENT',NULL,'3'),
 ('LCEXPADVNC',NULL,'KES','3500.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC EXPORT ADVISING COMM NONCLIENT',NULL,'3'),
 ('LCEXPAMENDC',NULL,'KES','2500.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC EXPORT GENERAL AMENDMENT CLIENTS',NULL,'3'),
 ('LCEXPAMENDN',NULL,'KES','3000.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC EXPORT GENERAL AMEND NON CLIENT',NULL,'3'),
 ('LCEXPCNCL',NULL,'KES','5000.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC EXPORT CANCELLATION COMMISSION',NULL,'3'),
 ('LCEXPDOCEX',NULL,'KES','4000.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC EXPORT DOCUMENT EXAMINATION',NULL,'3'),
 ('LCEXPDOCHAN',NULL,'KES','500.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC PAYMENT COMM',NULL,'3'),
 ('LCEXPPAY',NULL,'KES','2000.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC EXPORT PAY COMM',NULL,'3'),
 ('LCEXPPOST',NULL,'KES','2000.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC EXPORT LOCAL POSTAGE COMM',NULL,'3'),
 ('LCEXPSWIFT',NULL,'KES','2500.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC EXPORT SWIFT COMM',NULL,'3'),
 ('LCIMPAMEND',NULL,'KES','3500.00','FLAT',NULL,NULL,NULL,NULL,'52345','523','523','LC Import General Amendments',NULL,'3'),
 ('LCIMPASTDUE',NULL,'KES','2000.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC IMPORT PASTDUE CHARGES',NULL,'3'),
 ('LCIMPCNCL',NULL,'KES','5000.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC IMPORT CANCELLATION COMM',NULL,'3'),
 ('LCIMPDISCR',NULL,'USD','100.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC IMPORT DISCREPANCY COMM',NULL,'3'),
 ('LCIMPDOCEX',NULL,'KES','4000.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC IMPORT DOCUMENT EXAMINATION',NULL,'3'),
 ('LCIMPDOCHAN',NULL,'KES','500.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC IMPORT DOCUMENT HANDLING',NULL,'3'),
 ('LCIMPDOCRL',NULL,'KES','3000.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC IMPORT DOCUMENT RELEASE COMM',NULL,'3'),
 ('LCIMPEXP',NULL,'KES','5000.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC IMPORT EXPIRED UNUTILISED COMM',NULL,'3'),
 ('LCIMPSWIFT',NULL,'KES','2500.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC IMPORT SWIFT COMM',NULL,'3'),
 ('LCOMIPO','PERCENTAGE','KES',NULL,'LEVEL','1',NULL,NULL,NULL,'52211','242','242','Committement fees',NULL,'3'),
 ('LCOPEN',NULL,'KES','2000.00','FLAT',NULL,NULL,NULL,NULL,'52345','514','518','LC OPENNING COMM',NULL,'3'),
 ('LCOPN',NULL,'KES','2000.00',NULL,NULL,NULL,NULL,NULL,'52345','514','518','LC OPEN CHARGE','KES','3'),
 ('LCPAY',NULL,'KES','2000.00','FLAT',NULL,NULL,NULL,NULL,'52345','501','500','LC PAYMENT COMM',NULL,'3'),
 ('LDSTO',NULL,'KES','200.00',NULL,NULL,NULL,NULL,NULL,'52216','172','173','Standing Order Loans',NULL,'3'),
 ('LDSTOM',NULL,'KES','50.00',NULL,NULL,NULL,NULL,NULL,'52216','172','173','Standing Order Loans',NULL,'3'),
 ('LDSTOW',NULL,'KES','10.00',NULL,NULL,NULL,NULL,NULL,'52216','172','173','Standing Order Loans',NULL,'3'),
 ('LIENPOSIPO',NULL,'KES','1030.00','FLAT',NULL,NULL,NULL,NULL,'52000','961','962','Lien and Postage Fees',NULL,'3'),
 ('LIF','PERCENTAGE','KES',NULL,'LEVEL','1',NULL,NULL,NULL,'KES1631000010000','243','243','Loan Insurance Fees',NULL,'3'),
 ('LIMPESA','PERCENTAGE','KES',NULL,'LEVEL','0.5',NULL,NULL,NULL,'KES1055600040000','789','789','Lipa na Mpesa Charges',NULL,NULL),
 ('LIMPESA1',NULL,'KES','0.00','FLAT',NULL,NULL,NULL,NULL,'KES1055600040000','789','789','Lipa na Mpesa Charges',NULL,NULL),
 ('LINSFEES','PERCENTAGE','KES',NULL,'LEVEL','1',NULL,NULL,NULL,'52000','961','962','Loan Insurance Fees',NULL,'3'),
 ('LOAN','PERCENTAGE','KES',NULL,'BAND','24',NULL,NULL,NULL,'52040','390','391','Flat Interest',NULL,'3'),
 ('MBTOPUP',NULL,'KES','10.00',NULL,NULL,NULL,NULL,NULL,'52263','260','260','Mobile Airtime Top-up',NULL,'3'),
 ('MCFCOMM','PERCENTAGE','KES',NULL,'LEVEL','5',NULL,NULL,NULL,'52307','249','249','MCF Commission',NULL,'3'),
 ('MF',NULL,'KES','200.00',NULL,NULL,NULL,NULL,NULL,'52200','172','173','MEMBERSHIP FEES',NULL,'3'),
 ('MFSINT','PERCENTAGE','KES',NULL,'LEVEL','3',NULL,NULL,NULL,'51000','289','319','Loan Commission',NULL,NULL),
 ('MGRCOM',NULL,'KES','100.00',NULL,NULL,NULL,NULL,NULL,'KES1055700010000','989','989','MoneyGram Commission',NULL,'3'),
 ('MOBCHG',NULL,'KES','25.00','FLAT',NULL,NULL,NULL,NULL,'52263','260','260','MOBILE BANKING CHARGE',NULL,'3'),
 ('MPESAIBCORP','PERCENTAGE','KES',NULL,'LEVEL^LEVEL^LEVEL^LEVEL^LEVEL','0.000000001^0.000000001^0.000000001^0.000000001^0.000000001','1000.00^10000.00^30000.00^70000.00','30.00^40.00^50.00^70.00^1000.00',NULL,'52334','260','260','Corporate Mpesa B2B IB',NULL,'3'),
 ('MPESAIBRET','PERCENTAGE','KES',NULL,'LEVEL^LEVEL^LEVEL^LEVEL^LEVEL','0.000000001^0.000000001^0.000000001^0.000000001^0.000000001','1000.00^10000.00^30000.00^70000.00','30.00^40.00^50.00^70.00^1000.00',NULL,'52333','260','260','Retail Mpesa B2B IB',NULL,'3'),
 ('MPTOAC','UNIT','KES',NULL,'BAND^BAND^BAND^BAND^BAND^BAND^BAND^BAND^BAND',NULL,'1000.00^2499.00^4999.00^9999.00^19999.00^34999.00^49999.00^70000.00',NULL,NULL,'52329','260','260','Mpesa to Account Commission',NULL,'3'),
 ('MSHACOM','PERCENTAGE','KES',NULL,'LEVEL','1.5',NULL,'1000.00',NULL,'52211','242','242','Mshahara Commitment Fees',NULL,'3'),
 ('MSHCOM','PERCENTAGE','KES',NULL,'LEVEL','2',NULL,'500.00',NULL,'52211','242','242','Mshahara Commitment Fees',NULL,'3'),
 ('NCBCQ',NULL,'KES','300.00',NULL,NULL,NULL,NULL,NULL,'52310','244','244','Bankers Chq Comm - Non Client',NULL,'3'),
 ('NCBCQ2',NULL,'KES','100.00','FLAT',NULL,NULL,NULL,NULL,'52310','244','244','Bankers Chq Charge',NULL,'3'),
 ('NCHARGE',NULL,'KES','0.00','FLAT',NULL,NULL,NULL,NULL,'52326','260','260','Bridge placeholder charge code',NULL,'3'),
 ('NCHARGEIB','UNIT','KES',NULL,'LEVEL^LEVEL^LEVEL^LEVEL^LEVEL',NULL,'1000.00^10000.00^30000.00^70000.00',NULL,NULL,'52333','260','260','Bridge placeholder charge code IB',NULL,'3'),
 ('NEGO',NULL,'KES','2000.00','FLAT',NULL,NULL,NULL,NULL,'52330','527','527','LC NEGOTIATION COMM',NULL,'3'),
 ('OC3',NULL,'KES','300.00',NULL,NULL,NULL,NULL,NULL,'52323','195','196','OVER THE COUNTER WITHDR',NULL,'3'),
 ('OCW',NULL,'KES','100.00',NULL,NULL,NULL,NULL,NULL,'52323','195','196','OVER THE COUNTER WITHDR',NULL,'3'),
 ('OCW50',NULL,'KES','50.00',NULL,NULL,NULL,NULL,NULL,'52323','195','196','OVER THE COUNTER CHARGES - 50 SHS',NULL,'3'),
 ('OCWM',NULL,'KES','50.00',NULL,NULL,NULL,NULL,NULL,'52323','195','196','OVER THE COUNTER WITHDR',NULL,'3'),
 ('OTC50',NULL,'KES','50.00',NULL,NULL,NULL,NULL,NULL,'52323','195','196','OVER THE COUNTER WITHDR YES',NULL,'3'),
 ('OUTREMCHG',NULL,'KES','500.00',NULL,NULL,NULL,NULL,NULL,'52107','206','206','Outward REMIT Charges',NULL,'3'),
 ('OUTREMITCHG',NULL,'KES','500.00','FLAT',NULL,NULL,NULL,NULL,'52107','206','206','Outward REMIT Charges',NULL,'3'),
 ('OUTSWIFT',NULL,'KES','2000.00',NULL,NULL,NULL,NULL,NULL,'52006','204','204','Outward Swift Charges',NULL,'3'),
 ('OUTSWIFTCHG',NULL,'KES','2000.00','FLAT',NULL,NULL,NULL,NULL,'52006','204','204','Outward SWIFT Charges',NULL,'3'),
 ('OUTSWIFTIB',NULL,'KES','2000.00','FLAT',NULL,NULL,NULL,NULL,'52333','204','204','Outward SWIFT Charges IB',NULL,'3'),
 ('OUTTELEXCHG',NULL,'KES^USD','0.00^20.00','FLAT^FLAT',NULL,NULL,NULL,NULL,'52106','205','205','Outward TELEX Charges',NULL,'3'),
 ('PB',NULL,'KES','100.00',NULL,NULL,NULL,NULL,NULL,'52200','172','173','PASS BOOK FEES',NULL,'3'),
 ('PERS',NULL,'KES','2.50',NULL,NULL,NULL,NULL,NULL,'KES1100700010000','192','193','STAMP DUTY ON CHEQUES',NULL,NULL),
 ('PESALINKCHG','PERCENTAGE','KES',NULL,'LEVEL^LEVEL','0.00001^0.00001','^501.00','0^11.60',NULL,'52339','934','934','Pesalink charges',NULL,'3'),
 ('POS',NULL,'KES','2000.00',NULL,NULL,NULL,NULL,NULL,'52330','530','530','LC POSTGE CHARGES',NULL,'3'),
 ('POSDEP','PERCENTAGE','KES',NULL,'LEVEL^LEVEL^LEVEL^LEVEL','0.00001^0.0001^0.0001^0.00001','5000.00^10000.00^20000.00','15.00^25.00^40.00^50.00',NULL,'KES1609500010000','313','313','POSAGNCY Deposit Charges',NULL,'3'),
 ('POSWITH','PERCENTAGE','KES',NULL,'LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL','0.00001^0.0001^0.0001^0.0001^0.00001^0.00001','2500.00^5000.00^10000.00^20000.00^35000.00','25.00^40.00^65.00^125.00^145.00^170.00',NULL,'52329','313','313','POSAGNCY Withdrawal Charge',NULL,'3'),
 ('PPACHG',NULL,'KES','75.00','FLAT',NULL,NULL,NULL,NULL,'52260','269','269','ATM CHARGES',NULL,'3'),
 ('PPACHGSTF',NULL,'KES','50.00','FLAT',NULL,NULL,NULL,NULL,'52260','269','269','ATM CHARGES',NULL,'3'),
 ('RBNHDTAX','PERCENTAGE','KES^EUR^CAD^AUD^USD^GBP',NULL,'LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL','0^0.05^0^0.05^0^0.05^0^0.05^0^0.05^0^0.05','499999.00',NULL,NULL,'KES1725800100000','790','790','Robin Hood Tax',NULL,NULL),
 ('RECOUP',NULL,'KES','100.00',NULL,NULL,NULL,NULL,NULL,'52322','272','272','RECOUP CHARGES',NULL,'3'),
 ('RTGSCHG',NULL,'KES','500.00','FLAT',NULL,NULL,NULL,NULL,'52338','206','206','RTGS Outward Charge',NULL,'3'),
 ('RTGSCHGIB',NULL,'KES','500.00','FLAT',NULL,NULL,NULL,NULL,'52333','206','206','RTGS Outward Charge IB',NULL,'3'),
 ('RTGSCOM',NULL,'KES','500.00',NULL,NULL,NULL,NULL,NULL,'52338','988','988','Rtgs Commission',NULL,'3'),
 ('RTGSIB2',NULL,'KES','0.00','FLAT',NULL,NULL,NULL,NULL,'52333','206','206','RTGS Outward Charge IB',NULL,'3'),
 ('RTGSIBCHG',NULL,'KES','500.00',NULL,NULL,NULL,NULL,NULL,'52333','206','206','RTGS Outward Charge IB',NULL,'3'),
 ('RTGSIBSTAFF',NULL,'KES','0.00',NULL,NULL,NULL,NULL,NULL,'52333','206','206','RTGS Outward Charge IB',NULL,'3'),
 ('SALADV',NULL,'KES','2000.00',NULL,NULL,NULL,NULL,NULL,'52510','172','173','Salary Advance Commission',NULL,'3'),
 ('SALAPROCESS',NULL,'KES','200.00',NULL,NULL,NULL,NULL,NULL,'52510','140','140','Salary Processing','KES','4'),
 ('SDCHQ','UNIT','KES',NULL,'LEVEL',NULL,NULL,NULL,NULL,'KES1100700010000','192','193','STAMP',NULL,'3'),
 ('SFCHAT',NULL,'KES','2000.00',NULL,NULL,NULL,NULL,NULL,'52324','172','173','School Fees Loan Chattel Fees',NULL,'3'),
 ('SFTVENDCHG',NULL,'KES','3.00','FLAT',NULL,NULL,NULL,NULL,'52265','933','933','Agent Deposit Commission',NULL,'3'),
 ('SFTVENDCHGW',NULL,'KES','3.00','FLAT',NULL,NULL,NULL,NULL,'52265','934','934','Agent Withdrawal Comm',NULL,'3'),
 ('SIDEAP',NULL,'KES','500.00',NULL,NULL,NULL,NULL,NULL,'52338','641','642','EAP CHARGES',NULL,'3'),
 ('STAF','UNIT','KES',NULL,'LEVEL^LEVEL',NULL,'40000.00','500.00',NULL,'52323','195','196','Staff Charges',NULL,'3'),
 ('STAFFTT',NULL,'KES','1000.00',NULL,NULL,NULL,NULL,NULL,'52006','247','247','TT Commision',NULL,'3'),
 ('STAMP',NULL,'KES','2.50',NULL,NULL,NULL,NULL,NULL,'KES1100800010000','635','636','STAMP DUTY',NULL,NULL),
 ('STF',NULL,'KES','500.00',NULL,NULL,NULL,NULL,NULL,'52323','195','196','Staff Charges',NULL,'3'),
 ('STMTCHARGE',NULL,'KES^USD','150.00^2.50','FLAT^FLAT',NULL,NULL,NULL,NULL,'52010','522','522','Statement Print Charge',NULL,'3'),
 ('STOCU',NULL,'KES','200.00',NULL,NULL,NULL,NULL,NULL,'52311','235','235','Standing Order Charges - Customer',NULL,'3'),
 ('STOEX',NULL,'KES','400.00',NULL,NULL,NULL,NULL,NULL,'52311','235','235','Standing Order Charges - External',NULL,'3'),
 ('STOEXSTAF',NULL,'KES','100.00',NULL,NULL,NULL,NULL,NULL,'52311','235','235','Standing Order Charges - External',NULL,'3'),
 ('STOP',NULL,'KES','500.00',NULL,NULL,NULL,NULL,NULL,'52318','135','135','Stop Payment Charges',NULL,'3'),
 ('STOPCHQ',NULL,'KES','500.00','FLAT',NULL,NULL,NULL,NULL,'52002','961','962','Cheque Stop Payment Charges',NULL,'3'),
 ('STOST',NULL,'KES','50.00',NULL,NULL,NULL,NULL,NULL,'52311','235','235','Standing Order Charges - Staff',NULL,'3'),
 ('STOUG',NULL,'KES','50.00',NULL,NULL,NULL,NULL,NULL,'52311','235','235','Standing Order Charges - Ungana',NULL,'3'),
 ('STOUP',NULL,'KES','2000.00',NULL,NULL,NULL,NULL,NULL,'52311','235','235','Standing Order Charges Unpaid',NULL,'3'),
 ('SWIFT',NULL,'KES','2000.00',NULL,NULL,NULL,NULL,NULL,'52330','641','642','SWIFT CHARGES',NULL,'3'),
 ('TAXMANUAL','PERCENTAGE','KES',NULL,'LEVEL','20',NULL,NULL,NULL,'KES1725700000000','464','465','Excise Duty',NULL,NULL),
 ('TCSALE','PERCENTAGE','KES',NULL,'LEVEL','0',NULL,NULL,NULL,'52051','961','962','Travellers Cheque Sales Charges',NULL,'3'),
 ('TCSCOM','PERCENTAGE','USD',NULL,'LEVEL','1.5',NULL,NULL,NULL,'52301','49','49','Sale of Traveller\'s Cheque',NULL,'3'),
 ('TCSCOM1','PERCENTAGE','USD',NULL,'LEVEL','1',NULL,NULL,NULL,'52301','49','49','Purchase of Traveller\'s Cheque',NULL,'3'),
 ('TECH',NULL,'KES','300.00','FLAT',NULL,NULL,NULL,NULL,'52000','961','962','UNPAID CHEQUE CHARGE',NULL,'3'),
 ('TRACE',NULL,'KES','1000.00',NULL,NULL,NULL,NULL,NULL,'52330','534','534','LC TRACER CHARGES',NULL,'3'),
 ('TTCOMM',NULL,'KES','2000.00',NULL,NULL,NULL,NULL,NULL,'52006','247','247','TT Commision',NULL,'3'),
 ('TXTCHG',NULL,'KES','20.00','FLAT',NULL,NULL,NULL,NULL,'52263','48','47','TXT CHARGE',NULL,'3'),
 ('UKCHAT',NULL,'KES','2000.00',NULL,NULL,NULL,NULL,NULL,'52324','172','173','Ukulima Chattel Fees',NULL,'3'),
 ('UNG',NULL,'KES','50.00',NULL,NULL,NULL,NULL,NULL,'52323','195','196','OVER THE COUNTER WITHDR UNG',NULL,'3'),
 ('UNPAYCHG',NULL,'KES','2500.00',NULL,NULL,NULL,NULL,NULL,'52004','874','874','Cheque Unpay Charge',NULL,'3'),
 ('VBBALENQ',NULL,'KES','10.00',NULL,NULL,NULL,NULL,NULL,'52328','296','296','Vibe Balance Charges','KES','4'),
 ('VBMINISTMT',NULL,'KES','10.00',NULL,NULL,NULL,NULL,NULL,'52328','522','522','Vibe Mini Statement Charges','KES','4'),
 ('VBSTATEMENT',NULL,'KES','10.00',NULL,NULL,NULL,NULL,NULL,'52328','522','522','Vibe Statement Charges','KES','4'),
 ('VBWITH','PERCENTAGE','KES',NULL,'LEVEL^LEVEL^LEVEL^LEVEL^LEVEL^LEVEL','0.00001^0.0001^0.0001^0.0001^0.0001^0.00001','99.00^20000.00^50000.00^75000.00^100000.00','0^50.00^100.00^125.00^150.00^200.00',NULL,'52329','934','934','Agent Withdrawl Commission',NULL,'3'),
 ('WUCOM',NULL,'KES','100.00',NULL,NULL,NULL,NULL,NULL,'KES1055000010000','990','990','WesternUnionCommission',NULL,'3'),
 ('YES',NULL,'KES','100.00',NULL,NULL,NULL,NULL,NULL,'52323','195','196','OVER THE COUNTER WITHDR YES',NULL,'3'),
 ('ZERO','RATEPERLOT','KES',NULL,'LOT',NULL,NULL,NULL,NULL,'52474','661','660','Derivatives Zero Commission',NULL,'3'),
 ('ZEROCHG',NULL,'KES','0.00','FLAT',NULL,NULL,NULL,NULL,'52601','626','625','ZERO CHARGES AND COMMISSIONS',NULL,'3');
/*!40000 ALTER TABLE `bnk_charge$types` ENABLE KEYS */;




/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
