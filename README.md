# mystrom-importer

Import mystrom data from daily email reports

The mystrom switch sends optionally a daily report to an email address. This email holds a reports.zip with a random named csv file inside. 
This program extract all data from all emails of the configured IMAP inbox to the given database. 
Existing data (compared by timestamp) will be skipped.

## Setup
- place a .env file in root directory with:
```
SQL_URL=sqlite+pysqlite:///mystrom.sqlite3
```
- place a .env file in importer directory with:
```
MAIL_SERVER=server address
MAIL_SERVER_PORT=port number
MAIL_USER=username
MAIL_PASSWD=password
MAIL_INBOX=INBOX
```
