import pymssql

def connectDB(strServer, strDatabase):
    # ---------------------------------------------------------------------------------
    # Connect to a database, when the name and server is provided
    
    # @Args:
    #       - strServername:    DNS Name of the server, where the Database is located.
    #       - strDatabase:      Name of the Database
    # @Returns:
    #       - conn:             connection object
    #       - cur:              database cursor object
    # ---------------------------------------------------------------------------------
    conn = pymssql.connect (server = strServer, database = strDatabase)
    cur = conn.cursor(as_dict=True)
    #cur.execute('select * from hce.series.series_test')
    return conn, cur

