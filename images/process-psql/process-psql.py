#!/usr/bin/env python
# #!/usr/local/bin/python

from csv import DictReader as csv_read
from os import environ as env
from psycopg2 import connect as db_connect, DatabaseError


#map_file=env['USER_VLAN_MAP']

#print(data)

params = {
        "host": env['DB_HOST'],
        "port": env['DB_PORT'],
        "database": env['DB_NAME'],
        "user": env['DB_USER'],
        "password": env['DB_PASS']
}

def get_csv_values(csv_file):
    with open(csv_file, 'r', newline='') as csv:
        reader = csv_read(csv)
        data = [row for row in reader]
    return data

class PG:
    def __init__(self):
        # Load DB parameters
        self.db_params = params

        # Load nas clients and user mappings
        self.nas_clients = get_csv_values(env['CLIENTS_FILE'])
        self.rad_users = get_csv_values(env['USERS_FILE'])
        self.rad_groups = get_csv_values(env['GROUPS_FILE'])
        
        # Connect to PostgreSQL server and create the conn and cur objects
        self.connect()

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            self.conn = db_connect(**self.db_params)
            self.cur = self.conn.cursor()
            
        except (Exception, DatabaseError) as error:
            print(error)

    def execute(self, query):
        """ Execute SQL query and commit the connection """
        try:
            self.cur.execute(query)
        except (Exception, DatabaseError) as error:
            print(error)
        self.conn.commit()

    def delete(self, db):
        """ Delete database contents and reset id field """
        try:
            for item in db:
                query = f"DELETE FROM {item}"
                self.cur.execute(query)

            for item in db:
                query = f"ALTER SEQUENCE {item}_id_seq RESTART WITH 1"
                self.cur.execute(query)
        except (Exception, DatabaseError) as error:
            print(error)
        self.conn.commit()

    def disconnect(self):
        """ Disconnect from the PostgreSQL database server """
        try:
        # close the communication with the PostgreSQL
            self.cur.close()
        except (Exception, DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
                print('Database connection closed.')

    def nas_table(self):
        """ Recreate the nas table to define radius clients"""
        # Delete all entries
        db_name = ["nas"]
        self.delete(db_name)
        
        for client in self.nas_clients:
            self.execute(f"insert into {db_name[0]} (nasname, shortname, secret) values ('{client['ip']}', '{client['name']}', '{client['secret']}')")

    def user_group_table(self):
        """ Recreate the radcheck and radusergroup table"""
        # Delete all entries
        db_name = ["radcheck", "radusergroup"]
        self.delete(db_name)
        
        for user in self.rad_users:
            self.execute(f"insert into {db_name[0]} (username, attribute, op, value) values ('{user['mac']}', 'Cleartext-Password', '=:', '{user['mac']}')")
            self.execute(f"insert into {db_name[1]} (username, groupname, priority) values ('{user['mac']}', '{user['group']}', '0')")

    def reply_table(self):
        """ Recreate the radcheck and radusergroup table"""
        # Delete all entries
        db_name = ["radgroupreply"]
        self.delete(db_name)
        
        for group in self.rad_groups:
            self.execute(f"insert into {db_name[0]} (groupname, attribute, op, value) values ('{group['group']}', 'Tunnel-Type', '=', 'vlan')")
            self.execute(f"insert into {db_name[0]} (groupname, attribute, op, value) values ('{group['group']}', 'Tunnel-Medium-Type', '=', '802')")
            self.execute(f"insert into {db_name[0]} (groupname, attribute, op, value) values ('{group['group']}', 'Tunnel-Private-Group-ID', '=', '{group['vlan']}')")


if __name__ == '__main__':
    pg = PG()
    pg.nas_table()
    pg.user_group_table()
    pg.reply_table()
    pg.disconnect()
