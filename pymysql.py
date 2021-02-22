import mysql.connector
import json

config = json.loads(open("./config.json","r").read())

mydb = mysql.connector.connect(
  host=config["db"]["host"],
  user=config["db"]["user"],
  password=config["db"]["password"],
  database=config["db"]["name"]
)

sql = mydb.cursor()


def executeSql(self, cmd):
    mydb.connect()
    print("Executing: " + cmd)
    if cmd.startswith("SELECT"):
        sql.execute(cmd)
        result = sql.fetchall()
        mydb.close()
        return result
    else:
        # insert, update or delete
        sql.execute(cmd)
        mydb.commit()
        mydb.close()
        return
