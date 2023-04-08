import os
import random
import mysql.connector
from faker import Faker
import datetime

mydb = mysql.connector.connect(host=os.environ['db_url'],
                               port=os.environ['db_port'],
                               database=os.environ['db_name'],
                               user=os.environ['db_user'],
                               password=os.environ['db_pwd'])

Faker.seed(2)
fake = Faker('fr_FR')

print(mydb)
mycursor = mydb.cursor()

#######################################################################################
# Utils
#######################################################################################


def insert_many(table, fields, values, n_values):
  request = "INSERT INTO {} ({}) VALUES ({})".format(table, fields, n_values)
  mycursor.executemany(request, values)
  mydb.commit()


#######################################################################################
# Generators
#######################################################################################


# id, name vc(25)
def insert_region(n):
  values = []
  for _ in range(n):
    values.append((fake.unique.region(), ))
  insert_many("region", "name", values, "%s")


# id, code char(3), name varchar(25), id_region
def insert_department(n):
  id = 1
  values = []
  for _ in range(n):
    dpt = fake.unique.department()
    values.append((
      dpt[0],
      dpt[1],
      id,
    ))
    id += 1
  insert_many("department", "code, name, id_region", values, "%s, %s, %s")


# id, name vc(50), postal_code vc(5), id_department
def insert_city(n):
  id = 1
  values = []
  for _ in range(n):
    values.append((
      fake.unique.city(),
      fake.unique.postcode(),
      id,
    ))
    id += 1
  insert_many("city", "name, postal_code, id_department", values, "%s, %s, %s")


# id, street_number smallint, street vc(250), address_complement vc(100), id_city
def insert_address(n, max1):
  values = []
  for _ in range(n):
    values.append((
      fake.building_number(),
      fake.street_name(),
      fake.street_prefix(),
      random.randint(1, max1),
    ))
  insert_many("address", "street_number, street, address_complement, id_city",
              values, "%s, %s, %s, %s")


# id, name vc(100)
def insert_product_name(n):
  values = []
  for _ in range(n):
    values.append((fake.catch_phrase(), ))
  insert_many("product_name", "name", values, "%s")


# id, name vc(500), phone_number vc(13), id_address
def insert_agency(n, max1):
  values = []
  for _ in range(n):
    values.append((
      fake.company(),
      fake.msisdn(),
      random.randint(1, max1),
    ))
  insert_many("agency", "name, phone_number, id_address", values, "%s, %s, %s")


# id, first_name, last_name, id_address
def insert_advisor(n, max1):
  values = []
  for _ in range(n):
    values.append((
      fake.first_name(),
      fake.last_name(),
      random.randint(1, 3),
      random.randint(1, max1),
    ))
  insert_many("advisor", "first_name, last_name, status, id_address", values,
              "%s, %s, %s, %s")


# id_agency, id_advisor
def insert_agency_advisor(n, max1, max2):
  values = []
  for _ in range(n):
    values.append((
      random.randint(1, max1),
      random.randint(1, max2),
    ))
  insert_many("agency_advisor", "id_agency, id_advisor", values, "%s, %s")


# id, first_name, last_name, address, id_agency
def insert_client(n, max1, max2):
  values = []
  for _ in range(n):
    values.append((
      fake.first_name(),
      fake.last_name(),
      random.randint(1, max1),
      random.randint(1, max2),
      random.randint(1, 15000),
    ))
  insert_many(
    "client", "first_name, last_name, id_address, id_agency, salary_per_month",
    values, "%s, %s, %s, %s, %s")


# id, balance, iban, swift, id_client
def insert_account(n, max1):
  values = []
  for _ in range(n):
    values.append((
      round(random.uniform(100.00, 100_000.00), 2),
      fake.unique.iban(),
      fake.swift8(),
      random.randint(1, max1),
    ))
  insert_many("account", "balance, iban, swift, id_client", values,
              "%s, %s, %s, %s")


# id, balance, interest_rate, opening, ending, id_account
def insert_loan(n, max1):
  values = []
  for _ in range(n):
    start_date = fake.date_between()
    end_date = datetime.date(2029, 1, 1)
    values.append((
      round(random.uniform(100.00, 10_000.00), 2),
      round(random.uniform(0.00, 9.99), 2),
      start_date,
      fake.date_between(start_date, end_date),
      random.randint(1, 3),
      random.randint(1, max1),
    ))
  insert_many("loan",
              "balance, interest_rate, opening, ending, risk, id_account",
              values, "%s, %s, %s, %s, %s, %s")


# id, balance, interest_rate, id_account, id_product
def insert_saving_account(n, max1, max2):
  values = []
  for _ in range(n):
    values.append((
      round(random.uniform(100.00, 10_000.00), 2),
      round(random.uniform(0.00, 9.99), 2),
      random.randint(1, max1),
      random.randint(1, max2),
    ))
  insert_many("saving_account",
              "balance, interest_rate, id_account, id_product", values,
              "%s, %s, %s, %s")


# id, amount, label, id_emitter, id_reciever
def insert_transaction(n, max1, max2):
  values = []
  for _ in range(n):
    values.append((
      random.randint(-10000, 10000),
      fake.sentence(nb_words=random.randint(1, 10)),
      random.randint(1, max1),
      random.randint(1, max2),
      fake.date(),
    ))
  # Allows to insert 100000 per 100000
  for element in [values[x:x+100000] for x in range(0, len(values), 100000)]:
    insert_many("transaction", "amount, label, id_emitter, id_receiver, sent_on",
                element, "%s, %s, %s, %s, %s")
  
#######################################################################################
# Runners
#######################################################################################
  
N_ENTRIES = 100_000

insert_region(10)
insert_department(10)
insert_city(10)
insert_address(1_000, 10)
insert_product_name(1_000)
insert_agency(500, 1_000)
insert_advisor(1_000, 1_000)
insert_agency_advisor(250, 500, 1_000)
insert_client(10_000, 1_000, 500)
insert_account(50_000, 10_000)
insert_loan(50_000, 50_000)
insert_saving_account(100_000, 50_000, 1_000)
insert_transaction(7_000_000, 10_000, 10_000)
