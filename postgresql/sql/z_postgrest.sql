CREATE ROLE anon nologin;
CREATE ROLE authenticator noinherit login password 'authenticator';
GRANT anon TO authenticator;

GRANT ALL on nas TO anon;
GRANT ALL on radcheck TO anon;
GRANT ALL on radgroupcheck TO anon;
GRANT ALL on radgroupreply TO anon;
GRANT ALL on radreply TO anon;
GRANT ALL on radusergroup TO anon;

GRANT ALL on nas_id_seq TO anon;
GRANT ALL on radcheck_id_seq TO anon;
GRANT ALL on radgroupcheck_id_seq TO anon;
GRANT ALL on radgroupreply_id_seq TO anon;
GRANT ALL on radreply_id_seq TO anon;
GRANT ALL on radusergroup_id_seq TO anon;