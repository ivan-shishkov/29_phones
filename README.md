# Microservice for Search Index of Phone Numbers

This service allows you to normalize the phone numbers in the table with orders info for the online store database.
This will make it convenient and quick to search for orders by phone number.

# Quickstart

For service launch need to install Python 3.5 and then install all dependencies:

```bash

$ pip install -r requirements.txt

```

## Used Environment Variables

* **DATABASE_URI** - a database URI

## Adding a New Column to a Database Table

To perform this operation, you must have access to the database with permissions to change the structure of the tables.

To add a new column in which phone numbers will be stored in a normalized form, you need to run:

```bash

$ export DATABASE_URI='postgresql://username:password@db_host/db_name'
$ alembic upgrade head

```

## Running of Phone Numbers Normalization Script in Background

To run the phone numbers normalization script in background need to execute:

```bash

$ nohup python3 normalize_phones.py &

```

After that, the script will periodically check the appearance of orders with unnormalized telephone numbers in the background and perform their normalization.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
