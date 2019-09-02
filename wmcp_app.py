import json
import datetime
import decimal
import os

def get_all_users():
    return getdata('SELECT * from findme.contacts')


def getdata(sql="SHOW TABLES", fmt='json'):
    msg = ''
    import MySQLdb
    try:
        cnx = connect_to_cloudsql()
        cursor = cnx.cursor()
        if sql is None:
          sql = "SHOW TABLES"
        print(sql)
        cursor.execute(sql)
        query_result = [dict(line) \
            for line in [zip([column[0] \
                for column in cursor.description], row) \
                    for row in cursor.fetchall() \
            ] \
        ]
        '''
        numrows = cursor.rowcount
        for x in xrange(0, numrows):
            result = cursor.fetchone()
            d = [ dict(line) for line in [zip([ column[0] for column in cursor.description], result)
            msg += json.dump(result, d)
            if x != numrows:
                msg += ","
        '''
        cursor.close()
        if fmt == 'json':
            return jsondumps(query_result)
        else:
            return query_result
    except MySQLdb.DatabaseError as err:
        return err
    else:
        cnx.close()
    return msg

def connect_to_cloudsql():
    import MySQLdb
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    db = MySQLdb.connect(
        host="wmcp-mysql", port=3306, db="findme", user="dbuser", passwd="MySQL123!")

    return db

###
# JSON: set specific json.dumps behavior and filter
##
def jsondumps(myobj):
    return json.dumps(myobj, indent=4, skipkeys=True, ensure_ascii=False, sort_keys=True,\
        separators=(',', ':'), default=jsonfilter)

def jsonfilter(myobj):
    if type(myobj) is dict:
        return dict(myobj)
    if type(myobj) is datetime.date or type(myobj) is datetime.datetime:
        return myobj.isoformat()
    if type(myobj) is decimal.Decimal:
        return float(myobj)
