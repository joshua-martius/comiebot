import pymysql

class configwrapper: 
    def getEntry(key):
        cmd = "SELECT cValue FROM tblConfig WHERE cKey = '%s'" % (key)
        result = pymysql.executeSql(cmd)
        if len(result) > 1:
            return result[0]
        else:
                try:
                    return str(result[0][0])
                except:
                    print("Key %s doesnt exist!" % key)
                    return