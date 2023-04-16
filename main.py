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

fake = Faker('fr_FR')

print(mydb)
mycursor = mydb.cursor()

country = ['France', 'Canada', 'Suisse', 'Angleterre']

account_type = [{
  'name': 'Livret A',
  'interest_rate': 3,
}, {
  'name': 'LDDS',
  'interest_rate': 3,
}, {
  'name': 'LEP',
  'interest_rate': 6.1,
}, {
  'name': 'Livret Jeune',
  'interest_rate': 3,
}, {
  'name': 'CEL',
  'interest_rate': 2,
  'taxation': True
}, {
  'name': 'PEL',
  'interest_rate': 2,
  'taxation': True
}, {
  'name': 'PREP',
  'interest_rate': None,
  'taxation': True
}, {
  'name': 'CAT',
  'interest_rate': 3,
  'taxation': True
}, {
  'name': 'Compte Bancaire Individuel',
  'interest_rate': None,
  'is_external': True
}, {
  'name': 'Compte Bancaire Joint',
  'interest_rate': None,
  'is_external': True
}]

#######################################################################################
# Utils
#######################################################################################


def insert_many(table, fields, values, n_values):
  request = "INSERT INTO {} ({}) VALUES ({})".format(table, fields, n_values)
  mycursor.executemany(request, values)
  mydb.commit()


def select(table, fields, conditions):
  request = "SELECT {} FROM {} WHERE {}".format(fields, table, conditions)
  mycursor.execute(request)
  return mycursor.fetchall()


#######################################################################################
# Generators
#######################################################################################


# id, name vc(25)
def insert_region(loop_number):
  values = []
  for _ in range(loop_number):
    values.append((
      fake.unique.region(),
      country[random.randint(0, 3)],
    ))
  insert_many("region", "name, country", values, "%s, %s")


# id, code char(3), name varchar(25), id_region
def insert_department(loop_number):
  id = 1
  values = []
  for _ in range(loop_number):
    dpt = fake.unique.department()
    values.append((
      dpt[0],
      dpt[1],
      id,
    ))
    id += 1
  insert_many("department", "code, name, fk_region", values, "%s, %s, %s")


# id, name vc(50), postal_code vc(5), id_department
def insert_city(loop_number):
  id = 1
  values = []
  for _ in range(loop_number):
    values.append((
      fake.unique.city(),
      fake.unique.postcode(),
      id,
    ))
    id += 1
  insert_many("city", "name, postal_code, fk_department", values, "%s, %s, %s")


# id, street_number smallint, street vc(250), address_complement vc(100), id_city
def insert_address(loop_number, max_fk_city):
  values = []
  for _ in range(loop_number):
    values.append((
      fake.building_number(),
      fake.street_name(),
      fake.street_prefix(),
      random.randint(1, max_fk_city),
    ))
  insert_many("address", "street_number, street, address_complement, fk_city",
              values, "%s, %s, %s, %s")


# id, name vc(500), phone_number vc(13), id_address
def insert_agency(loop_number, max_fw_address):
  values = []
  for _ in range(loop_number):
    values.append((
      fake.company(),
      fake.msisdn(),
      random.randint(1, max_fw_address),
    ))
  insert_many("agency", "name, phone_number, fw_address", values, "%s, %s, %s")


# id, first_name, last_name, id_address
def insert_advisor(loop_number):
  values = []
  for _ in range(loop_number):
    values.append((
      fake.first_name(),
      fake.last_name(),
      random.randint(1, 3),
    ))
  insert_many("advisor", "first_name, last_name, status", values, "%s, %s, %s")


# id_agency, id_advisor
def insert_agency_advisor(loop_number, max_fk_agency, max_fk_advisor):
  values = []
  for _ in range(loop_number):
    values.append((
      random.randint(1, max_fk_agency),
      random.randint(1, max_fk_advisor),
    ))
  insert_many("agency_advisor", "fk_agency, fk_advisor", values, "%s, %s")


def insert_account_type():
  values = []
  for i in range(len(account_type)):
    values.append((
      account_type[i]['name'],
      account_type[i]['interest_rate'],
      random.randint(1, 3),
      account_type[i]['taxation'] if 'taxation' in account_type[i] else False,
      account_type[i]['is_external']
      if 'is_external' in account_type[i] else False,
    ))
  insert_many("account_type",
              "name, interest_rate, risk, taxation, is_external", values,
              "%s, %s, %s, %s, %s")


# id, first_name, last_name, address, id_agency
def insert_client(loop_number, max_fk_advisor, max_fk_address):
  values = []
  for _ in range(loop_number):
    values.append((
      fake.first_name(),
      fake.last_name(),
      random.randint(1, 15000),
      random.randint(1, max_fk_advisor),
      random.randint(1, max_fk_address),
    ))
  insert_many(
    "client",
    "first_name, last_name, salary_per_month, fk_advisor, fk_address", values,
    "%s, %s, %s, %s, %s")


def insert_client_account_type(loop_number, max_fk_client,
                               max_fk_account_type):
  values = []
  for _ in range(loop_number):
    start_date = fake.date_between()
    end_date = datetime.date(2029, 1, 1)
    values.append((
      random.randint(1, max_fk_client),
      random.randint(1, max_fk_account_type),
      start_date,
      fake.date_between(start_date, end_date),
    ))
  insert_many("client_account_type",
              "fk_client, fk_account_type, opening, ending", values,
              "%s, %s, %s, %s")


# id, amount, label, id_emitter, id_reciever
def insert_transaction_of_current_vie(loop_number, max_fk_client):
  values = []
  account_type = select('account_type', 'pk_account_type', "is_external=1")
  for _ in range(loop_number):
    start_date = fake.date_between()
    end_date = datetime.date(2029, 1, 1)
    values.append((
      random.randint(-10000, 10000),
      fake.date_between(start_date, end_date),
      account_type[random.randint(0,
                                  len(account_type) - 1)][0],
      account_type[random.randint(0,
                                  len(account_type) - 1)][0],
      random.randint(1, max_fk_client),
      random.randint(1, max_fk_client),
    ))

  # Allows to insert 100000 per 100000
  for element in [values[x:x + 100000] for x in range(0, len(values), 100000)]:
    insert_many(
      "transaction",
      "amount, emission, fk_sender_account_type, fk_receiver_account_type, fk_sender_client, fk_receiver_client",
      element, "%s, %s, %s, %s, %s, %s")


def insert_internal_transaction(loop_number, max_fk_client):
  values = []
  for _ in range(loop_number):
    start_date = fake.date_between()
    end_date = datetime.date(2029, 1, 1)

    client_choose = random.randint(1, max_fk_client)

    client_account_type = select(table='client_account_type',
                                 fields='fk_account_type',
                                 conditions='fk_client=' + str(client_choose))

    size = len(client_account_type) - 1
    if size > 0:
      values.append((
        random.randint(-10000, 10000),
        fake.date_between(start_date, end_date),
        client_account_type[random.randint(0,
                                           len(client_account_type) - 1)][0],
        client_account_type[random.randint(0,
                                           len(client_account_type) - 1)][0],
        client_choose,
        client_choose,
      ))
    elif size <= 0:
      continue

  # Allows to insert 100000 per 100000
  for element in [values[x:x + 100000] for x in range(0, len(values), 100000)]:
    insert_many(
      "transaction",
      "amount, emission, fk_sender_account_type, fk_receiver_account_type, fk_sender_client, fk_receiver_client",
      element, "%s, %s, %s, %s, %s, %s")


#######################################################################################
# Runners
#######################################################################################

insert_region(loop_number=10)
insert_department(loop_number=10)
insert_city(loop_number=10)
insert_address(loop_number=1_000, max_fk_city=10)
insert_agency(loop_number=500, max_fw_address=1_000)
insert_advisor(loop_number=1_000)
insert_agency_advisor(loop_number=250, max_fk_agency=500, max_fk_advisor=1_000)

insert_account_type()
insert_client(loop_number=10_000, max_fk_advisor=1_000, max_fk_address=1_000)
insert_client_account_type(loop_number=20_000, max_fk_client=10_000, max_fk_account_type=len(account_type))

insert_transaction_of_current_vie(loop_number=500_000, max_fk_client=10_000)
insert_internal_transaction(loop_number=500_000, max_fk_client=10_000)

print('OK')
