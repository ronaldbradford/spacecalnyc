CREATE SCHEMA IF NOT EXISTS spacecalnyc;
DROP USER spacecalnyc@localhost;
CREATE USER spacecalnyc@localhost IDENTIFIED BY 'challenge';
GRANT SELECT,INSERT,UPDATE,DELETE ON spacecalnyc.* TO spacecalnyc@localhost;

USE spacecalnyc;
DROP TABLE IF EXISTS schedule;
CREATE TABLE schedule(
  _id     VARCHAR(50) NOT NULL,
  source  ENUM('XMM-Newton','Fermi','AGILE','Chandra','INTEGRAL','NuStar','RXTE','Suzaku','Swift','Herschel','Spitzer','Hubble') NOT NULL,
  target  VARCHAR(50) NOT NULL,
  start   DATETIME NOT NULL,
  end     DATETIME NOT NULL,
  ra      DECIMAL(8,5) NOT NULL,
  `dec`     DECIMAL(8,5) NOT NULL,
  ra_str  VARCHAR(15) NOT NULL,
  dec_str VARCHAR(15) NOT NULL,
  l       FLOAT NOT NULL,
  b       FLOAT NOT NULL,
  observation VARCHAR(30) NOT NULL,
  created TIMESTAMP,
PRIMARY KEY(_id),
INDEX (start, end, source),
INDEX (source),
INDEX (target)
) ENGINE =InnoDB;
