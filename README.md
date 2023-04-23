# Ma (première) DB

- Groupe G1
  - Arnaud BOYER
  - Clément LAFON
  - Clément LO-CASCIO

- [Ma (première) DB](#ma--premi-re--db)
  * [TOC](#toc)
  * [But](#but)
    + [ERD](#erd)
  * [Indexes](#indexes)
    + [1 - Loan: opening](#1---loan--opening)
    + [2 - Advisor: status](#2---advisor--status)
    + [3 - Account: iban, swift](#3---account--iban--swift)
  * [Vues](#vues)
    + [1 - Comptes client](#1---comptes-client)
    + [2 - Montants comptes clients](#2---montants-comptes-clients)
    + [3 - Montants prêts clients](#3---montants-pr-ts-clients)
    + [4 - Montants épargnes clients](#4---montants--pargnes-clients)
    + [5 - Montants clients](#5---montants-clients)
  * [Procédures stockées](#proc-dures-stock-es)
    + [1 - Total des actifs](#1---total-des-actifs)
    + [2 - Agences les plus proches](#2---agences-les-plus-proches)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

<br>


## But

Notre base représente une structure de banque simplifiée.

### ERD
![ERD](erd.png)

<br>

## Indexes

### 1 - Loan: opening

Afin de pouvoir trier la table par date d'ouverture d'un crédit plus rapidement lors de calculs de temps.



### 2 - Advisor: status

Afin de pouvoir trier la table par états des employées. Pour retrouver plus rapidement les employées en service ou ceux en vacances par exemple.



### 3 - Account: iban, swift

Afin de pouvoir chercher plus rapidement les comptes lors de transactions inter-bancaires.

<br>

## Vues 

### 1 - Comptes client

  * Retourne le solde des comptes d'un client et le type de compte associée

```sql
CREATE VIEW clientaccounts
AS
  CALL simon_sql.get_balance_account(9725);

  SELECT 
      account_type.name as 'Account Name',
      temp_get_balance_account.Balance,
      temp_get_balance_account.On
  FROM temp_get_balance_account
      inner join account_type ON account_type.pk_account_type = temp_get_balance_account.pk_account_type
```

```sql
Procédure qui permet de retourner le solde d un compte 

DROP PROCEDURE IF EXISTS get_balance_account;

CREATE PROCEDURE `simon_sql`.`get_balance_account`(IN id_client INT)
BEGIN
	DROP TEMPORARY TABLE IF EXISTS temp_get_balance_account;
	
	CREATE TEMPORARY TABLE temp_get_balance_account
	SELECT
		account_type.pk_account_type,
		sum(amount) as 'Balance', 
		DATE_FORMAT(LAST_DAY(transaction.emission), "%Y-%m-%d") as 'On'
	FROM `transaction` 
		inner join account_type ON account_type.pk_account_type = transaction.fk_sender_account_type 
	WHERE fk_sender_client = id_client 
	GROUP BY YEAR(emission), MONTH (emission);
END
```



### 2 - Gains d'un client sur 12 mois

  * Vue qui permet d'obtenir tous les gains d'un client sur 12 mois.

```sql
CREATE VIEW earning_of_client
AS
SELECT 
	CONCAT(receiver.first_name, ' ', receiver.last_name) as 'Receive',
	CONCAT(sender.first_name, ' ', sender.last_name) as 'From',
	CONCAT(transaction.amount, ' €') as 'Amount',
	DATE_FORMAT(transaction.emission , "%d/%m/%Y") as 'on' 
FROM `transaction`
	inner join client as sender ON transaction.fk_sender_client = sender.pk_client 
	inner join client as receiver ON transaction.fk_receiver_client  = receiver.pk_client 
WHERE sender.pk_client = 7852 and transaction.amount > 0 and transaction.emission BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE()
ORDER BY emission DESC;

SELECT * FROM earning_of_client;
```



### 3 - Montants intérets des placements d'un client

 * Vue qui permet de retourner le montant des intérets du placement d'un client au cours de sa durée de vie

```sql
CREATE VIEW savings_clients
AS
SELECT 
	CONCAT(client.first_name, ' ', client.last_name) as 'Who',
	SUM(amount) as 'Saves',
	((SUM(amount) * account_type.interest_rate) / 100) as 'Bank Interest',
	(SUM(amount) + ((SUM(amount) * account_type.interest_rate) / 100)) as 'New Balance',
	t.emission as 'On'
FROM `transaction` t 
	inner join account_type ON t.fk_receiver_account_type = account_type.pk_account_type 
	inner join client on t.fk_receiver_client = client.pk_client 
WHERE t.fk_receiver_account_type = 3 and t.fk_receiver_client = 7123 
GROUP BY YEAR(t.emission), MONTH (t.emission)
ORDER BY t.emission DESC;

SELECT * FROM savings_clients;
```


### 4 - Montants épargnes clients

Procédure qui permet de déterminer si le compte est à découvert depuis plus de 3 mois

```sql
DROP PROCEDURE IF EXISTS check_open_a_consumer_loan;
    
CREATE PROCEDURE check_open_a_consumer_loan(IN id_client INTEGER, IN end_date VARCHAR(25), INOUT open_a_consumer_credit BOOLEAN)
BEGIN
  DECLARE is_done INTEGER DEFAULT 0;
  DECLARE c_balance DECIMAL(8,2);
 
  DECLARE c_counter INTEGER DEFAULT 0;
 
  -- déclare le curseur
  DECLARE account_cursor CURSOR FOR
    SELECT temp_get_balance_account.Balance FROM temp_get_balance_account inner join account_type ON account_type.pk_account_type = temp_get_balance_account.pk_account_type where account_type.name LIKE 'Compte Bancaire%' AND temp_get_balance_account.On BETWEEN DATE_SUB(end_date, INTERVAL 3 MONTH) AND end_date;

  DECLARE CONTINUE HANDLER FOR NOT FOUND SET is_done = 1;
  
  -- ouvre le curseur
  OPEN account_cursor;

  get_list: LOOP
  FETCH account_cursor INTO c_balance;
 
  IF is_done = 1 THEN
  LEAVE get_list;
  END IF;
 
  IF c_balance < 0 THEN
  SET c_counter = c_counter + 1;
  END IF;
  END LOOP get_list;
  -- ferme le curseur
  CLOSE account_cursor;
 
  IF c_counter >= 3 THEN
  SET open_a_consumer_credit = open_a_consumer_credit + 1;
  END IF;
  SET open_a_consumer_credit = open_a_consumer_credit + 0;
END 
```



### 5 - Montant des agios

```sql
CREATE VIEW 
AS
```


