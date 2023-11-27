# Freeradius with PostgreSQL
Freeradius with preconfigured PostgreSQL database based on Docker and Docker Compose.
No freeradius clients.conf is needed, the nas clients are read from the database as well.

## Usage
Rename the **.env_template** to **.env** and change the database credentials accordingly.
If you change the user, password or database name, also update the file **images/postgres/sql**.

## Additional
The main focus was to create a user/vlan mapping for Cisco wireless clients based on a CSV file.
Therefore there is an additional container running a python script to insert the CSV data into the database.
