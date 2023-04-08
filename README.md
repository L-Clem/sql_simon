# Ma (première) DB

- Groupe G1
  - Arnaud BOYER
  - Clément LAFON
  - Clément LO-CASCIO

## TOC

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
    + [1](#1)
    + [2](#2)

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

Vue permettant d'afficher l'ensemble des comptes par client.

```sql
CREATE VIEW clientaccounts
AS
  SELECT a.id_client,
         c.last_name,
         c.first_name,
         a.id AS accountIndex,
         a.balance,
         a.iban
  FROM   account a
         inner join client c
                 ON a.id_client = c.id
  ORDER  BY a.id_client; 
```



### 2 - Montants comptes clients

Vue permettant d'afficher les 10 plus grosses fortunes.

```sql
CREATE VIEW top_10_wealthiest_people
AS
SELECT
	a3.id_client,
	(SUM(a3.balance) + sub2.total_sa + sub2.total_ln) as total_account_amounts_by_client
FROM (
	SELECT 
		a2.id_client as id_client,
		SUM(sa.balance) as total_sa,
		sub.total_ln
	FROM (
			SELECT a.id_client, SUM(l.balance) as total_ln
			FROM loan l 
				inner join account a ON a.id = l.id_account
			GROUP BY a.id_client 
		) sub
		INNER join account a2 ON a2.id_client = sub.id_client
		inner join saving_account sa ON a2.id = sa.id_account  
	GROUP BY a2.id_client
) sub2
	inner join account a3 ON sub2.id_client = a3.id_client 
GROUP BY sub2.id_client
ORDER BY total_account_amounts_by_client DESC 
LIMIT 10
```



### 3 - Montants prêts clients

Vue permettant d'afficher le total des montants des prêts par clients.

```sql
CREATE VIEW clientTotalBalanceLoans 
AS
SELECT a.id_client,
       c.last_name,
       c.first_name,
       SUM(l.balance) AS totalLoanBalance
FROM   account a
       INNER JOIN client c
               ON a.id_client = c.id
       INNER JOIN loan l ON a.id = l.id_account 
GROUP BY c.id
ORDER  BY a.id_client;
```



### 4 - Montants épargnes clients

Vue permettant d'afficher le total des montants des épargnes par clients.

```sql
CREATE VIEW clientTotalBalanceSavings
AS
SELECT a.id_client,
       c.last_name,
       c.first_name,
       SUM(sa.balance) AS totalSavingBalance
FROM   account a
       INNER JOIN client c
               ON a.id_client = c.id
       INNER JOIN saving_account sa ON a.id = sa.id_account 
GROUP BY c.id
ORDER  BY a.id_client;
```



### 5 - Montant des agios

```sql
CREATE VIEW 
AS
```



<br>

## Procédures stockées

### 1 - Total des actifs

Procédure permettant d'obtenir le total des actifs d'un client (comptes, prêts, épargnes).

```sql
DELIMITER //
CREATE PROCEDURE getClientTotalOfAssets 
(IN client_id INT, OUT totalOfAssets DECIMAL(9,2))
	BEGIN
		DECLARE tab DECIMAL(8,2);
	    DECLARE tlb DECIMAL(8,2);
	    DECLARE tsb DECIMAL(8,2);
		
		SELECT totalAccountBalance
		INTO tab
		FROM clientTotalBalanceAllTypes
		WHERE id = client_id;
	
		SELECT totalLoanBalance
		INTO tlb
		FROM clientTotalBalanceAllTypes
		WHERE id = client_id;
	
		SELECT totalSavingBalance
		INTO tsb
		FROM clientTotalBalanceAllTypes
		WHERE id = client_id;	
	
		SET totalOfAssets = tab + tlb + tsb;
	END //
DELIMITER ;
```



### 2

Procédure permettant d'obtenir les agences les plus proches d'un client.


### 3 

Procédure permettant de dire si un client à la  possibilité d'obtenir un crédit

