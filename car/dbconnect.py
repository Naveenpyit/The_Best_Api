from .mainconnection import connection

class Api_db:
    @staticmethod
    def get_connect(query):
        try:
            conn=connection.db_connection()
            cur=conn.cursor()
            cur.execute(query)
            cols=[des[0]for des in cur.description]
            rows=cur.fetchall()
            conn.close()
            cur.close()
            res=[dict(zip(cols,row))for row in rows]
            return res
        except Exception as err:
            return {"Error":str(err)}
    @staticmethod
    def post_common(query):
        try:
            conn=connection.db_connection()
            cur=conn.cursor()
            cur.execute(query)
            conn.commit()
            conn.close()
            cur.close()
            return {"Message":"Data Submitted Successfully!"}
        except Exception as err:
            return {"Error":str(err)}