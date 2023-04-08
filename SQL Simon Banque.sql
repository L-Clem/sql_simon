CREATE TABLE `address` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `street_number` SMALLINT NOT NULL,
  `street` VARCHAR(250) NOT NULL,
  `address_complement` VARCHAR(100),
  `id_city` INT NOT NULL
);

CREATE TABLE `city` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(50) UNIQUE NOT NULL,
  `postal_code` VARCHAR(5) NOT NULL,
  `id_department` INT NOT NULL
);

CREATE TABLE `region` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(25) UNIQUE NOT NULL
);

CREATE TABLE `department` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `code` CHAR(3) UNIQUE NOT NULL,
  `name` VARCHAR(25) UNIQUE NOT NULL,
  `id_region` INT NOT NULL
);

CREATE TABLE `client` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `first_name` VARCHAR(1000) NOT NULL,
  `last_name` VARCHAR(1000) NOT NULL,
  `id_address` INT NOT NULL,
  `id_agency` INT NOT NULL,
  `salary_per_month` decimal(8,2) NOT NULL
);

CREATE TABLE `account` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `balance` DECIMAL(8,2) NOT NULL,
  `iban` VARCHAR(34) UNIQUE NOT NULL,
  `swift` CHAR(8) NOT NULL,
  `id_client` INT NOT NULL
);

CREATE TABLE `transaction` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `amount` DECIMAL(8,2) NOT NULL,
  `label` VARCHAR(500) NOT NULL,
  `id_emitter` INT NOT NULL,
  `id_receiver` INT NOT NULL,
  `sent_on` date NOT NULL
);

CREATE TABLE `agency` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(500) NOT NULL,
  `phone_number` VARCHAR(13) NOT NULL,
  `id_address` INT NOT NULL
);

CREATE TABLE `agency_advisor` (
  `id_agency` INT,
  `id_advisor` INT,
  PRIMARY KEY (`id_agency`, `id_advisor`)
);

CREATE TABLE `advisor` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `first_name` VARCHAR(1000) NOT NULL,
  `last_name` VARCHAR(1000) NOT NULL,
  `status` ENUM ('working', 'vacation', 'gone') NOT NULL,
  `id_address` INT NOT NULL
);

CREATE TABLE `saving_account` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `balance` DECIMAL(8,2) NOT NULL,
  `interest_rate` FLOAT(3,2) NOT NULL,
  `id_account` INT NOT NULL,
  `id_product` INT NOT NULL
);

CREATE TABLE `product_name` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL
);

CREATE TABLE `loan` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `balance` DECIMAL(8,2) NOT NULL,
  `interest_rate` FLOAT(3,2) NOT NULL,
  `opening` DATE NOT NULL,
  `ending` DATE NOT NULL,
  `risk` ENUM ('low', 'medium', 'high') NOT NULL,
  `id_account` INT NOT NULL
);

CREATE INDEX `account_index_0` ON `account` (`iban`, `swift`);

CREATE INDEX `advisor_index_1` ON `advisor` (`status`);

CREATE INDEX `loan_index_2` ON `loan` (`opening`);

ALTER TABLE `address` ADD FOREIGN KEY (`id_city`) REFERENCES `city` (`id`);

ALTER TABLE `city` ADD FOREIGN KEY (`id_department`) REFERENCES `department` (`id`);

ALTER TABLE `department` ADD FOREIGN KEY (`id_region`) REFERENCES `region` (`id`);

ALTER TABLE `client` ADD FOREIGN KEY (`id_address`) REFERENCES `address` (`id`);

ALTER TABLE `client` ADD FOREIGN KEY (`id_agency`) REFERENCES `agency` (`id`);

ALTER TABLE `account` ADD FOREIGN KEY (`id_client`) REFERENCES `client` (`id`);

ALTER TABLE `transaction` ADD FOREIGN KEY (`id_emitter`) REFERENCES `account` (`id`);

ALTER TABLE `transaction` ADD FOREIGN KEY (`id_receiver`) REFERENCES `account` (`id`);

ALTER TABLE `agency` ADD FOREIGN KEY (`id_address`) REFERENCES `address` (`id`);

ALTER TABLE `agency_advisor` ADD FOREIGN KEY (`id_agency`) REFERENCES `agency` (`id`);

ALTER TABLE `agency_advisor` ADD FOREIGN KEY (`id_advisor`) REFERENCES `advisor` (`id`);

ALTER TABLE `advisor` ADD FOREIGN KEY (`id_address`) REFERENCES `address` (`id`);

ALTER TABLE `saving_account` ADD FOREIGN KEY (`id_account`) REFERENCES `account` (`id`);

ALTER TABLE `saving_account` ADD FOREIGN KEY (`id_product`) REFERENCES `product_name` (`id`);

ALTER TABLE `loan` ADD FOREIGN KEY (`id_account`) REFERENCES `account` (`id`);
