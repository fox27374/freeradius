# Clients
insert into nas (nasname, shortname, secret) values ('10.140.60.250', 'WLC', 'yLfeCF258ZRjntagVN9JDP');
insert into nas (nasname, shortname, secret) values ('10.140.60.249', 'Testclient', 'yLfeCF258ZRjntagVN9JDP');

# Users
insert into radcheck (username, attribute, op, value) values ('test', 'Cleartext-Password', ':=', 'test');
insert into radcheck (username, attribute, op, value) values ('f2270f1e2ea4', 'Cleartext-Password', ':=', 'f2270f1e2ea4');

# User Group Mapping
insert into radusergroup (username, groupname, priority) values ('test', 'TESTGROUP', '0');
insert into radusergroup (username, groupname, priority) values ('f2270f1e2ea4', 'mobile', '0');

# Radius reply by group
# TESTGROUP
insert into radgroupreply (groupname, attribute, op, value) values ('TESTGROUP', 'Tunnel-Type', '=', 'VLAN');
insert into radgroupreply (groupname, attribute, op, value) values ('TESTGROUP', 'Tunnel-Medium-Type', '=', '802');
insert into radgroupreply (groupname, attribute, op, value) values ('TESTGROUP', 'Tunnel-Private-Group-ID', '=', '63');

# mobile
insert into radgroupreply (groupname, attribute, op, value) values ('mobile', 'Tunnel-Type', '=', 'VLAN');
insert into radgroupreply (groupname, attribute, op, value) values ('mobile', 'Tunnel-Medium-Type', '=', '802');
insert into radgroupreply (groupname, attribute, op, value) values ('mobile', 'Tunnel-Private-Group-ID', '=', '60');

update radcheck set value = 'yLfeCF258ZRjntagVN9JDP' where username = 'f2270f1e2ea4';
update radgroupreply set value = '60' where attribute = 'Tunnel-Private-Group-ID';