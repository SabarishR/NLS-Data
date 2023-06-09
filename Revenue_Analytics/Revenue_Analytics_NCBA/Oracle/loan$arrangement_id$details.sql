CREATE TABLE  loan$arrangement_id$details (
  ID NUMBER GENERATED BY DEFAULT AS IDENTITY,
  START_DATE date NOT NULL,
  END_DATE date NOT NULL,
  TOTAL_LOAN CLOB NOT NULL,
  CHARGED_LOAN CLOB NOT NULL,
  NOT_CHARGED_LOAN CLOB NOT NULL,
  STAFF_LOAN CLOB NOT NULL,
  CREATED_BY varchar(200) DEFAULT NULL,
  CREATED_ON TIMESTAMP DEFAULT NULL,
  UPDATED_BY varchar(200) DEFAULT NULL,
  UPDATED_ON TIMESTAMP DEFAULT NULL);
  
ALTER TABLE loan$arrangement_id$details ADD CONSTRAINT loan$arrangement_id$details_PK PRIMARY KEY ( ID ) ;