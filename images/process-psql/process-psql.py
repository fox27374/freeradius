#!/usr/bin/env python
# #!/usr/local/bin/python

from csv import DictReader as csv_read
from os import environ as env
from requests import post

def get_csv_values(csv_file):
    with open(csv_file, 'r', newline='') as csv:
        reader = csv_read(csv)
        data = [row for row in reader]
    return data

class PG:
    def __init__(self):
        # Load DB parameters
        self.url = f"http://{env['DB_HOST']}:{env['PGRST_PORT']}/"

        # Load nas clients and user mappings
        self.nas_clients = get_csv_values(env['CLIENTS_FILE'])
        self.rad_users = get_csv_values(env['USERS_FILE'])
        self.rad_groups = get_csv_values(env['GROUPS_FILE'])

    def post(self, table, json):
        headers = {'Content-type': 'application/json'}
        url = f"{self.url}{table}"
        print(url)
        r = post(url, headers=headers, json=json)

    def nas_table(self):
        """ Insert data to nas table """
        db = 'nas'
        
        for client in self.nas_clients:
            data = {
                "nasname": client['ip'],
                "shortname": client['name'],
                "secret": client['secret']
            }
            self.post(db, data)

    def user_group_table(self):
        """ Insert data radcheck and radusergroup table """
        db = ["radcheck", "radusergroup"]
        
        for user in self.rad_users:
            data = {
                "username": user['mac'],
                "attribute": "Cleartext-Password",
                "op": "=:",
                "value": user['mac']
            }

            self.post(db[0], data)

            data = {
                "username": user['mac'],
                "groupname": user['group'],
                "priority": "0"
            }

            self.post(db[1], data)

    def reply_table(self):
        """ Insert data into radgroupreply table"""
        db = "radgroupreply"
        
        for group in self.rad_groups:
            data = {
                "groupname": group['group'],
                "attribute": "Tunnel-Type",
                "op": "=",
                "value": "vlan"
            }

            self.post(db, data)

            data = {
                "groupname": group['group'],
                "attribute": "Tunnel-Medium-Type",
                "op": "=",
                "value": "802"
            }

            self.post(db, data)

            data = {
                "groupname": group['group'],
                "attribute": "Tunnel-Private-Group-ID",
                "op": "=",
                "value": group['vlan']
            }

            self.post(db, data)


if __name__ == '__main__':
    pg = PG()
    pg.nas_table()
    pg.user_group_table()
    pg.reply_table()

