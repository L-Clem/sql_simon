CREATE TABLE `address` (
	`pk_address` INT PRIMARY KEY AUTO_INCREMENT,
	`street_number` SMALLINT NOT NULL,
	`street` VARCHAR(250) NOT NULL,
	`address_complement` VARCHAR(100),
	`fk_city` INT NOT NULL
);

CREATE TABLE `city` (
	`pk_city` INT PRIMARY KEY AUTO_INCREMENT,
	`name` VARCHAR(50) UNIQUE NOT NULL,
	`postal_code` VARCHAR(5) NOT NULL,
	`fk_department` INT NOT NULL
);

CREATE TABLE `region` (
	`pk_region` INT PRIMARY KEY AUTO_INCREMENT,
	`name` VARCHAR(25) UNIQUE NOT NULL
);

CREATE TABLE `department` (
	`pk_departement` INT PRIMARY KEY AUTO_INCREMENT,
	`code` CHAR(3) UNIQUE NOT NULL,
	`name` VARCHAR(25) UNIQUE NOT NULL,
	`fk_region` INT NOT NULL
);

CREATE TABLE `client` (
	`pk_client` INT PRIMARY KEY AUTO_INCREMENT,
	`first_name` VARCHAR(1000) NOT NULL,
	`last_name` VARCHAR(1000) NOT NULL,
	`salary_per_month` decimal(8,2) NOT NULL,
	`fk_advisor` INT NOT NULL
);

CREATE TABLE `client_account_type` (
	`fk_client` INT,
	`fk_account_type` INT,
	PRIMARY KEY (`fk_client`, `fk_account_type`)
);


CREATE TABLE `agency` (
	`pk_agency` INT PRIMARY KEY AUTO_INCREMENT,
	`name` VARCHAR(500) NOT NULL,
	`phone_number` VARCHAR(13) NOT NULL,
	`fw_address` INT NOT NULL
);

CREATE TABLE `agency_advisor` (
	`fk_agency` INT,
	`fk_advisor` INT,
	PRIMARY KEY (`fk_agency`, `fk_advisor`)
);

CREATE TABLE `advisor` (
	`pk_advisor` INT PRIMARY KEY AUTO_INCREMENT,
	`first_name` VARCHAR(1000) NOT NULL,
	`last_name` VARCHAR(1000) NOT NULL,
	`status` ENUM ('working', 'vacation', 'gone') NOT NULL
);

CREATE TABLE `transaction` (
	`pk_transaction` INT PRIMARY KEY AUTO_INCREMENT,
	`amount` DECIMAL(8,2) NOT NULL,
	`emission` DATETIME NOT NULL,
	`fk_sender_client` INT NOT NULL,
	`fk_receiver_client` INT NOT NULL
);

CREATE TABLE `account_type` (
	`pk_account_type` INT PRIMARY KEY AUTO_INCREMENT,
	`interest_rate` FLOAT(3,2) DEFAULT NULL,
	`opening` DATETIME DEFAULT NULL, 
	`ending` DATETIME DEFAULT NULL,
	`risk` ENUM ('low', 'medium', 'high') NOT NULL
);

/*CREATE INDEX `account_index_0` ON `account` (`iban`, `swift`);

CREATE INDEX `advisor_index_1` ON `advisor` (`status`);

CREATE INDEX `loan_index_2` ON `loan` (`opening`);*/

ALTER TABLE `address` ADD FOREIGN KEY (`fk_city`) REFERENCES `city` (`pk_city`);

ALTER TABLE `city` ADD FOREIGN KEY (`fk_department`) REFERENCES `department` (`pk_departement`);

ALTER TABLE `department` ADD FOREIGN KEY (`fk_region`) REFERENCES `region` (`pk_region`);

ALTER TABLE `client` ADD FOREIGN KEY (`fk_advisor`) REFERENCES `advisor` (`pk_advisor`);

ALTER TABLE `client_account_type` ADD FOREIGN KEY (`fk_client`) REFERENCES `client`(`pk_client`);
ALTER TABLE `client_account_type` ADD FOREIGN KEY (`fk_account_type`) REFERENCES `account_type`(`pk_account_type`);

ALTER TABLE `transaction` ADD FOREIGN KEY (`fk_sender_client`) REFERENCES `client` (`pk_client`);

ALTER TABLE `transaction` ADD FOREIGN KEY (`fk_receiver_client`) REFERENCES `client` (`pk_client`);

ALTER TABLE `agency_advisor` ADD FOREIGN KEY (`fk_agency`)  REFERENCES `agency` (`pk_agency`);

ALTER TABLE `agency_advisor` ADD FOREIGN KEY (`fk_advisor`)  REFERENCES `advisor` (`pk_advisor`);

ALTER TABLE `agency` ADD FOREIGN KEY (`fw_address`)  REFERENCES `address` (`pk_address`);
