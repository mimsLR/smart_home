import psycopg2

class RealtimeDatabase:
    # Initialize database.
    def __init__(self):
        self.connection = None
        self.cursor = None
        #self.connect()

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

    # Create RealtimeDatabase table.
    def createTable(self):
        self.cursor.execute("""
        CREATE TABLE realtime_database (
            REALTIME_ID INT PRIMARY KEY,
            THERMOSTAT_TEMPERATURE INT DEFAULT 70,
            IS_BEDROOM_TV_ON BOOLEAN DEFAULT 't',
            IS_LIVINGROOM_TV_ON BOOLEAN DEFAULT 't',
            IS_FRONTDOOR_OPEN BOOLEAN DEFAULT 't',
            IS_BACKDOOR_OPEN BOOLEAN DEFAULT 't',
            IS_GARAGEDOOR_OPEN BOOLEAN DEFAULT 't',
            IS_MASTERBEDROOM_OVERHEAD_ON BOOLEAN DEFAULT 't',
            IS_MASTERBEDROOM_LAMP1_ON BOOLEAN DEFAULT 't',
            IS_MASTERBEDROOM_LAMP2_ON BOOLEAN DEFAULT 't',
            IS_BEDROOM1_OVERHEAD_ON BOOLEAN DEFAULT 't',
            IS_BEDROOM1_LAMP1_ON BOOLEAN DEFAULT 't',
            IS_BEDROOM1_LAMP2_ON BOOLEAN DEFAULT 't',
            IS_BEDROOM2_OVERHEAD_ON BOOLEAN DEFAULT 't',
            IS_BEDROOM2_LAMP1_ON BOOLEAN DEFAULT 't',
            IS_BEDROOM2_LAMP2_ON BOOLEAN DEFAULT 't',
            IS_LIVINGROOM_OVERHEAD_ON BOOLEAN DEFAULT 't',
            IS_LIVINGROOM_LAMP1_ON BOOLEAN DEFAULT 't',
            IS_LIVINGROOM_LAMP2_ON BOOLEAN DEFAULT 't',
            IS_KITCHEN_OVERHEAD_ON BOOLEAN DEFAULT 't',
            IS_BATHROOM1_OVERHEAD_ON BOOLEAN DEFAULT 't',
            IS_BATHROOM2_OVERHEAD_ON BOOLEAN DEFAULT 't'
        )
        """)
    
    # Initializes database with realtime data.
    def initializeRealtimeData(self):
        self.cursor.execute(
            """
            INSERT INTO
            realtime_database(REALTIME_ID)
            VALUES(1)
            """
        )

    # Clear all contents in the RealtimeDatabase table.
    def wipeTable(self):
        self.cursor.execute("DELETE FROM realtime_database")

    # Delete RealtimeDatabase table.
    def deleteTable(self):
        self.cursor.execute("DROP TABLE realtime_database")

    # Method to get all realtime data from database
    def getAllRealtimeData(self):
        self.cursor.execute("SELECT * FROM realtime_database")
        return self.cursor.fetchall()[0]

    # Get thermostat temperature.
    def getThermostatTemperature(self):
        data = self.getAllRealtimeData()
        return data[1]

    # Update thermostat temperature.
    def updateThermostatTemperature(self, temperature):
        self.cursor.execute("UPDATE realtime_database SET THERMOSTAT_TEMPERATURE = %s WHERE REALTIME_ID = %s", (temperature, 1))

    # Check if bedroom TV is on.
    def getIsBedroomTVOn(self):
        data = self.getAllRealtimeData()
        return data[2]
    
    # Update bedroom TV status.
    def updateBedroomTVStatus(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_BEDROOM_TV_ON = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_BEDROOM_TV_ON = %s WHERE REALTIME_ID = %s", (False, 1))

    # Check if living room TV is on.
    def getIsLivingRoomTVOn(self):
        data = self.getAllRealtimeData()
        return data[3]

    # Update living room TV status.
    def updateLivingRoomTVStatus(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_LIVINGROOM_TV_ON = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_LIVINGROOM_TV_ON = %s WHERE REALTIME_ID = %s", (False, 1))

    # Check if front door is open.
    def getIsFrontDoorOpen(self):
        data = self.getAllRealtimeData()
        return data[4]

    # Update front door status.
    def updateFrontDoorStatus(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_FRONTDOOR_OPEN = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_FRONTDOOR_OPEN = %s WHERE REALTIME_ID = %s", (False, 1))
    
    # Check if back door is open.
    def getIsBackDoorOpen(self):
        data = self.getAllRealtimeData()
        return data[5]

    # Update back door status.
    def updateBackDoorStatus(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_BACKDOOR_OPEN = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_BACKDOOR_OPEN = %s WHERE REALTIME_ID = %s", (False, 1))
    
    # Check if garage door is open.
    def getIsGarageDoorOpen(self):
        data = self.getAllRealtimeData()
        return data[6]
    
    # Update garage door status.
    def updateGarageDoorStatus(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_GARAGEDOOR_OPEN = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_GARAGEDOOR_OPEN = %s WHERE REALTIME_ID = %s", (False, 1))

    # Check if master bedroom overhead light is on.
    def getIsMasterBedroomOverheadOn(self):
        data = self.getAllRealtimeData()
        return data[7]

    # Update master bedroom overhead status.
    def updateMasterBedroomOverheadStatus(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_MASTERBEDROOM_OVERHEAD_ON = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_MASTERBEDROOM_OVERHEAD_ON = %s WHERE REALTIME_ID = %s", (False, 1))

    # Check if master bedroom lamp 1 is on.
    def getIsMasterBedroomLamp1On(self):
        data = self.getAllRealtimeData()
        return data[8]

    # Update master bedroom lamp 1 status.
    def updateMasterBedroomLamp1Status(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_MASTERBEDROOM_LAMP1_ON = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_MASTERBEDROOM_LAMP1_ON = %s WHERE REALTIME_ID = %s", (False, 1))

    # Check if master bedroom lamp 2 is on.
    def getIsMasterBedroomLamp2On(self):
        data = self.getAllRealtimeData()
        return data[9]

    # Update master bedroom lamp 2 status.
    def updateMasterBedroomLamp2Status(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_MASTERBEDROOM_LAMP2_ON = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_MASTERBEDROOM_LAMP2_ON = %s WHERE REALTIME_ID = %s", (False, 1))

    # Check if bedroom 1 overhead light is on.
    def getIsBedroom1OverheadOn(self):
        data = self.getAllRealtimeData()
        return data[10]

    # Update bedroom 1 overhead status.
    def updateBedroom1OverheadStatus(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_BEDROOM1_OVERHEAD_ON = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_BEDROOM1_OVERHEAD_ON = %s WHERE REALTIME_ID = %s", (False, 1))

    # Check if bedroom 1 lamp 1 is on.
    def getIsBedroom1Lamp1On(self):
        data = self.getAllRealtimeData()
        return data[11]

    # Update bedroom 1 lamp 1 status.
    def updateBedroom1Lamp1Status(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_BEDROOM1_LAMP1_ON = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_BEDROOM1_LAMP1_ON = %s WHERE REALTIME_ID = %s", (False, 1))

    # Check if bedroom 1 lamp 2 is on.
    def getIsBedroom1Lamp2On(self):
        data = self.getAllRealtimeData()
        return data[12]

    # Update bedroom 1 lamp 2 status.
    def updateBedroom1Lamp2Status(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_BEDROOM1_LAMP2_ON = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_BEDROOM1_LAMP2_ON = %s WHERE REALTIME_ID = %s", (False, 1))

    # Check if bedroom 2 overhead light is on.
    def getIsBedroom2OverheadOn(self):
        data = self.getAllRealtimeData()
        return data[13]

    # Update bedroom 2 overhead status.
    def updateBedroom2OverheadStatus(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_BEDROOM2_OVERHEAD_ON = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_BEDROOM2_OVERHEAD_ON = %s WHERE REALTIME_ID = %s", (False, 1))

    # Check if bedroom 2 lamp 1 is on.
    def getIsBedroom2Lamp1On(self):
        data = self.getAllRealtimeData()
        return data[14]

    # Update bedroom 2 lamp 1 status.
    def updateBedroom2Lamp1Status(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_BEDROOM2_LAMP1_ON = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_BEDROOM2_LAMP1_ON = %s WHERE REALTIME_ID = %s", (False, 1))

    # Check if bedroom 2 lamp 2 is on.
    def getIsBedroom2Lamp2On(self):
        data = self.getAllRealtimeData()
        return data[15]

    # Update bedroom 2 lamp 2 status.
    def updateBedroom2Lamp2Status(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_BEDROOM2_LAMP2_ON = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_BEDROOM2_LAMP2_ON = %s WHERE REALTIME_ID = %s", (False, 1))

    # Check if living room overhead light is on.
    def getIsLivingRoomOverheadOn(self):
        data = self.getAllRealtimeData()
        return data[16]

    # Update living room overhead status.
    def updateLivingRoomOverheadStatus(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_LIVINGROOM_OVERHEAD_ON = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_LIVINGROOM_OVERHEAD_ON = %s WHERE REALTIME_ID = %s", (False, 1))

    # Check if living room lamp 1 is on.
    def getIsLivingRoomLamp1On(self):
        data = self.getAllRealtimeData()
        return data[17]

    # Update living room lamp 1 status.
    def updateLivingRoomLamp1Status(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_LIVINGROOM_LAMP1_ON = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_LIVINGROOM_LAMP1_ON = %s WHERE REALTIME_ID = %s", (False, 1))

    # Check if living room lamp 2 is on.
    def getIsLivingRoomLamp2On(self):
        data = self.getAllRealtimeData()
        return data[18]

    # Update living room lamp 2 status.
    def updateLivingRoomLamp2Status(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_LIVINGROOM_LAMP2_ON = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_LIVINGROOM_LAMP2_ON = %s WHERE REALTIME_ID = %s", (False, 1))

    # Check if kitchen overhead light is on.
    def getIsKitchenOverheadOn(self):
        data = self.getAllRealtimeData()
        return data[19]

    # Update kitchen overhead light status.
    def updateKitchenOverheadStatus(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_KITCHEN_OVERHEAD_ON = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_KITCHEN_OVERHEAD_ON = %s WHERE REALTIME_ID = %s", (False, 1))

    # Check if bathroom 1 overhead light is on.
    def getIsBathroom1OverheadOn(self):
        data = self.getAllRealtimeData()
        return data[20]

    # Update bathroom 1 overhead light status.
    def updateBathroom1OverheadStatus(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_BATHROOM1_OVERHEAD_ON = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_BATHROOM1_OVERHEAD_ON = %s WHERE REALTIME_ID = %s", (False, 1))

    # Check if bathroom 2 overhead light is on.
    def getIsBathroom2OverheadOn(self):
        data = self.getAllRealtimeData()
        return data[21]

    # Update bathroom 2 overhead light status.
    def updateBathroom2OverheadStatus(self, status):
        if status == True:
            self.cursor.execute("UPDATE realtime_database SET IS_BATHROOM2_OVERHEAD_ON = %s WHERE REALTIME_ID = %s", (True, 1))
        else:
            self.cursor.execute("UPDATE realtime_database SET IS_BATHROOM2_OVERHEAD_ON = %s WHERE REALTIME_ID = %s", (False, 1))

# Test driver
if __name__=='__main__':
    database = RealtimeDatabase()
    database.connect()

    print(database.getAllRealtimeData())

    database.disconnect()
    