create table tbl_recon_nostro$virtual$possible$match (
ID int(11) NOT NULL AUTO_INCREMENT,
ACCOUNT_NO varchar(500) NOT NULL,
STATEMENT_DETAIL_ID varchar(1000) NOT NULL,
MATCH_TABLE varchar(1000) NOT NULL,
MATCH_ID varchar(1000) NOT NULL,
MATCH_AMOUNT double NOT NULL,
VARIANCE double NOT NULL,
ISMATCHED bool DEFAULT NULL,
CREATED_BY varchar(200) DEFAULT NULL,
CREATED_ON datetime NOT NULL,
UPDATED_BY varchar(200) DEFAULT NULL,
UPDATED_ON datetime DEFAULT NULL,
PRIMARY KEY (`ID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
