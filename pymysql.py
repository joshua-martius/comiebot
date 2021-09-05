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


def executeSql(cmd, log=False):
    mydb.connect()
    if log:
      print("Executing: " + cmd)
    
    sql.execute(cmd)

    if cmd.startswith("SELECT"):
        result = sql.fetchall()
        mydb.close()
        return result
    else:
        # insert, update or delete
        mydb.commit()
        mydb.close()
        return
