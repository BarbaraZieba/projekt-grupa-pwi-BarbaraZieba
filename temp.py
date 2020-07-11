import psycopg2
import sys, json
conn = psycopg2.connect("dbname=student user=app password=qwerty")

cur = conn.cursor()

sql_file = open('init.sql','r')
# cur.execute(sql_file.read())


functions = ["node","trip"]

def node(body):
    cur.execute("INSERT INTO points(id_point, geog, description) VALUES (%s,'SRID=4326;POINT(%s %s)', %s)"
    , (body["node"], body["lon"], body["lat"], body["description"]))

def trip(body):
    cur.execute("INSERT INTO cyclists (SELECT * FROM (VALUES (%s)) A(name) WHERE name NOT IN (SELECT * FROM cyclists))", (body["cyclist"],))
    cur.execute("INSERT INTO trips(id_route, cyclist_name, start_date) VALUES (%s, %s, %s)"
    , (body["version"], body["cyclist"], body["date"]))

# for line in sys.stdin:
#     if 'q' == line.rstrip():
#         break
#     data = json.loads(line)
#     !!!
# print("quit")


#    cur.execute("INSERT INTO cyclists (VALUES (%s) NOT IN (SELECT * FROM cyclists)"
#    , body["cyclist"])

line =  '{ "function": "trip", "body": { "cyclist": "piotr", "date": "2020-06-16", "version": 27}}'
json_in = json.loads(line)
if json_in["function"] in functions:
    out = globals()[json_in["function"]](json_in["body"])

else:
    out = "ERROR"


#{ "function": "node", "body": { "node": 12346, "lat": 51.198127, "lon": 16.919484, "description": "another nice place, is a must-see"}}


cur.execute("SELECT * FROM trips")
print(cur.fetchall())

conn.commit()
cur.close()
conn.close()