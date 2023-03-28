import psycopg2
import datetime

class HistoryDatabase:
    # Initialize database.
    def __init__(self):
        self.connection = None
        self.cursor = None

    # Connect to database.
    def connect(self):
        try:
            # Try connecting to database.
            self.connection = psycopg2.connect(
                host="138.26.48.83",
                database="Team4DB",
                user="Team4",
                password="team4"
            )
		
            # Create a cursor.
            self.cursor = self.connection.cursor()

            # Successfully established connection.
            print('Database successfully connected!')

        # Failed to connect to database.
        except (Exception, psycopg2.DatabaseError) as error:
            print('Database failed to connect:', error)

    # Disconnect from database.
    def disconnect(self):
        if (self.connection is not None) and (self.cursor is not None):
            self.cursor.close()
            self.connection.close()
            print('Database connection closed.')
    
    # Commit changes to database.
    def commitChanges(self):
        self.connection.commit()
    
    # Get PostgreSQL database server version.
    def getVersion(self):
        # Execute select statement to get version.
        self.cursor.execute('SELECT version()')

        # Display the PostgreSQL database server version.
        db_version = self.cursor.fetchone()
        print('PostgreSQL database version:', db_version)

    # Get all tables in database.
    def getTables(self):
        self.cursor.execute("""SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'""")
        for table in self.cursor.fetchall():
            print(table)

    # Create HistoryDatabase table.
    def createTable(self):
        self.cursor.execute("""
        CREATE TABLE history_database (
            DATE_TIME TIMESTAMPTZ PRIMARY KEY,
            EXTERIOR_TEMPERATURE FLOAT NOT NULL,
            TOTAL_WATTS FLOAT NOT NULL,
            TOTAL_GALLONS FLOAT NOT NULL,
            TOTAL_ELECTRICITY_COST FLOAT NOT NULL,
            TOTAL_WATER_COST FLOAT NOT NULL
        )
        """)
        
    # Clear all contents in the HistoryDatabase table.
    def wipeTable(self):
        self.cursor.execute("DELETE FROM history_database")

    # Delete HistoryDatabase table.
    def deleteTable(self):
        self.cursor.execute("DROP TABLE history_database")

    # Method to get all historical data from database
    def getAllHistoricalData(self):
        self.cursor.execute("SELECT * FROM history_database")
        data = self.cursor.fetchall()
        historicalData = []
        for row in data:
            historicalData.append({
                "DateTime": row[0],
                "ExteriorTemperature": row[1],
                "TotalWatts": row[2],
                "TotalGallons": row[3],
                "TotalElectricityCost": row[4],
                "TotalWaterCost": row[5],
            })

        return historicalData

    
    # TODO: Method to get historical data by date from database
    def getHistoricalDataByDate(self, date):
        return

    # Method to insert historical data to database
    def insertHistoricalData(self, datetime, exteriorTemperature, totalWatts, totalGallons, totalElectricityCost, totalWaterCost):
        self.cursor.execute(
            """
            INSERT INTO
            history_database(DATE_TIME, EXTERIOR_TEMPERATURE, TOTAL_WATTS, TOTAL_GALLONS, TOTAL_ELECTRICITY_COST, TOTAL_WATER_COST)
            VALUES(%s, %s, %s, %s, %s, %s)
            """,
            (datetime, exteriorTemperature, totalWatts, totalGallons, totalElectricityCost, totalWaterCost)
        )

# Test driver
if __name__=='__main__':
    database = HistoryDatabase()
    database.connect()

    print(database.getAllHistoricalData())

    database.disconnect()
