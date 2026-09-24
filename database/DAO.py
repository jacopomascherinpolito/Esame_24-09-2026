from database.DB_connect import DBConnect
from model.airport import Airport
from model.compagnie import Compagnia


class DAO:

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_compagnie(soglia):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.ID as ID, a.IATA_CODE as IATA_CODE, a.AIRLINE as AIRLINE
                    from airlines a join flights f on a.id=f.AIRLINE_ID  
                    group by a.ID
                    having count(distinct f.ORIGIN_AIRPORT_ID) >= %s"""

        cursor.execute(query, (soglia,))

        for row in cursor:
            r = Compagnia(row["ID"],
                      row["IATA_CODE"],
                          row["AIRLINE"],)
            result.append(r)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_tratte():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a1.id as c1, a2.id as c2, count(*) as peso
                    from airlines a1, airlines a2, flights f1, flights f2
                    where a1.id = f1.AIRLINE_ID and a2.id = f2.AIRLINE_ID and a1.id <> a2.ID 
                            and f1.ORIGIN_AIRPORT_ID = f2.ORIGIN_AIRPORT_ID and f1.DESTINATION_AIRPORT_ID = f2.DESTINATION_AIRPORT_ID 
                    group by c1,c2  
                    having count(*)>0"""

        cursor.execute(query)

        for row in cursor:
            result.append([row['c1'], row['c2'], row['peso']])

        cursor.close()
        conn.close()
        return result





