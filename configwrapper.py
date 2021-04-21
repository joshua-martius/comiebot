import pymysql

class configwrapper: 
    def getEntry(key):
        cmd = "SELECT cValue FROM tblConfig WHERE cKey = '%s'" % (key)
        result = pymysql.executeSql(cmd)
        if len(result) > 1:
            return result
        else:
                try:
                    if result[0][0].isnumeric():
                        return int(result[0][0])
                    else: 
                        return result[0][0]
                except:
                    print("Key %s doesnt exist!" % key)
                    return