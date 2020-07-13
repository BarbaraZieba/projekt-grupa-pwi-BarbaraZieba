import psycopg2
import sys, json
conn = psycopg2.connect("dbname=student user=app password=qwerty")

cur = conn.cursor()


if '--init' in sys.argv:
    sql_file = open('init.sql','r')
    cur.execute(sql_file.read())
    conn.commit()
    print('Successful initialization')

functions = ["node", "trip", "catalog", "closest_nodes"]

def node(body, dict):
    cur.execute("INSERT INTO points(id_point, geog, description) VALUES (%s,'SRID=4326;POINT(%s %s)', %s)"
    , (body["node"], body["lon"], body["lat"], body["description"]))
    conn.commit()

def trip(body, dict):
    cur.execute("INSERT INTO cyclists (SELECT * FROM (VALUES (%s)) A(name) WHERE name NOT IN (SELECT * FROM cyclists))", (body["cyclist"],))
    cur.execute("INSERT INTO trips(id_route, cyclist_name, start_date) VALUES (%s, %s, %s)"
    , (body["version"], body["cyclist"], body["date"]))
    conn.commit()

def catalog(body, dict): 
    cur.execute("INSERT INTO routes VALUES (%s)"
    , (body["version"],))
    i=0
    for node in body["nodes"]:
        cur.execute("INSERT INTO route_stages(id_route, day, id_point) VALUES (%s, %s, %s)"
        , (body["version"], i, node))
        i = i+1
    conn.commit()

def closest_nodes(body, dict):
    select = (
        "SELECT id_point, ST_X(geog::geometry),ST_Y(geog::geometry), ST_Distance("
        "ST_GeographyFromText('POINT(%s %s)'),geog) dist "
        "FROM points "
        "ORDER BY dist ASC, id_point DESC "
        "LIMIT 3;"
    )
    cur.execute(select, (body["ilon"], body["ilat"]))
    out = cur.fetchall()
    dict["data"] = []
    for row in out:
        dict["data"].append({"node": row[0], "olat": row[2],
        "olon": row[1], "distance": int(round(row[3]))})
    conn.commit()

for line in sys.stdin:
    # print(line)
    if 'q' == line.rstrip():
        break
    else:
        dict_out ={"status": None}
        json_in = json.loads(line)
        if json_in["function"] in functions:
            globals()[json_in["function"]](json_in["body"], dict_out)
            dict_out["status"] = "OK"
        else:
            dict_out["status"] = "ERROR"
        json_out = json.dumps(dict_out, indent = 4)
        print(json_out)
print("quit")

cur.close()
conn.close()