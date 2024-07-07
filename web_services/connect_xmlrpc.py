import xmlrpc.client

HOST = 'localhost'
PORT = 8069
DB = 'odoo17_db'
USER = 'admin'
PASS = 'admin'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

# 1- Login
common = xmlrpc.client.ServerProxy(ROOT + 'common')
uid = common.login(DB, USER, PASS)
print("Logged in as %s (uid: %d)" % (USER, uid))

# Object server proxy
call = xmlrpc.client.ServerProxy(ROOT + 'object')

# Read the sessions
search_domain = [('seats', '>', 0)]  # Search domain to filter sessions 
fields_to_read = ['name', 'seats']  # Fields to read for each session
sessions = call.execute(DB, uid, PASS, 'test_app.session', 'search_read', search_domain, fields_to_read)

for session in sessions:
    print("Session: ", session['name'])
    print("Number of seats: ", session['seats'])
    print()

# Create a new session with course id
course_id = call.execute(DB, uid, PASS, 'test_app.course', 'search', [('name', 'ilike', 'design')])[0] #search about the course_id by course_name, [0] get first one if found more than one
args = {
    'name': 'new session with XML-RPC',
    'course_id': course_id,
    'seats':5
}
session_id = call.execute(DB, uid, PASS, 'test_app.session', 'create', args)
print("New session is created with ID:", session_id)
