from flask import Flask, render_template, request, redirect
from data import RealtimeDatabase, HistoryDatabase
import datetime

app = Flask(__name__)

REALTIME_DATABASE = RealtimeDatabase.RealtimeDatabase()
HISTORY_DATABASE = HistoryDatabase.HistoryDatabase()

# index.html route
@app.route('/', methods=['GET', 'POST'])
def index():
    # Update if any changes are made on the control panel.
    if request.method == 'POST':
        # Living Room overhead
        isLivingRoomOverheadOn = request.form.get("livingRoomOverhead")
        if isLivingRoomOverheadOn != None:
            REALTIME_DATABASE.updateLivingRoomOverheadStatus(True)
        else:
            REALTIME_DATABASE.updateLivingRoomOverheadStatus(False)
        # Living Room lamp 1
        isLivingRoomLamp1On = request.form.get("livingRoomLamp1")
        if isLivingRoomLamp1On != None:
            REALTIME_DATABASE.updateLivingRoomLamp1Status(True)
        else:
            REALTIME_DATABASE.updateLivingRoomLamp1Status(False)
        # Living Room lamp 2
        isLivingRoomLamp2On = request.form.get("livingRoomLamp2")
        if isLivingRoomLamp2On != None:
            REALTIME_DATABASE.updateLivingRoomLamp2Status(True)
        else:
            REALTIME_DATABASE.updateLivingRoomLamp2Status(False)
        # Master Bedroom overhead
        isMasterBedroomOverheadOn = request.form.get("masterBedroomOverhead")
        if isMasterBedroomOverheadOn != None:
            REALTIME_DATABASE.updateMasterBedroomOverheadStatus(True)
        else:
            REALTIME_DATABASE.updateMasterBedroomOverheadStatus(False)
        # Master Bedroom lamp 1
        isMasterBedroomLamp1On = request.form.get("masterBedroomLamp1")
        if isMasterBedroomLamp1On != None:
            REALTIME_DATABASE.updateMasterBedroomLamp1Status(True)
        else:
            REALTIME_DATABASE.updateMasterBedroomLamp1Status(False)
        # Master Bedroom lamp 2
        isMasterBedroomLamp2On = request.form.get("masterBedroomLamp2")
        if isMasterBedroomLamp2On != None:
            REALTIME_DATABASE.updateMasterBedroomLamp2Status(True)
        else:
            REALTIME_DATABASE.updateMasterBedroomLamp2Status(False)
        # Master Bathroom overhead
        isMasterBathroomOverheadOn = request.form.get("masterBathroomOverhead")
        if isMasterBathroomOverheadOn != None:
            REALTIME_DATABASE.updateBathroom1OverheadStatus(True)
        else:
            REALTIME_DATABASE.updateBathroom1OverheadStatus(False)
        # Bedroom 1 overhead
        isBedroom1OverheadOn = request.form.get("bedroom1Overhead")
        if isBedroom1OverheadOn != None:
            REALTIME_DATABASE.updateBedroom1OverheadStatus(True)
        else:
            REALTIME_DATABASE.updateBedroom1OverheadStatus(False)
        # Bedroom 1 lamp 1
        isBedroom1Lamp1On = request.form.get("bedroom1Lamp1")
        if isBedroom1Lamp1On != None:
            REALTIME_DATABASE.updateBedroom1Lamp1Status(True)
        else:
            REALTIME_DATABASE.updateBedroom1Lamp1Status(False)
        # Bedroom 1 lamp 2
        isBedroom1Lamp2On = request.form.get("bedroom1Lamp2")
        if isBedroom1Lamp2On != None:
            REALTIME_DATABASE.updateBedroom1Lamp2Status(True)
        else:
            REALTIME_DATABASE.updateBedroom1Lamp2Status(False)
        # Bedroom 2 overhead
        isBedroom2OverheadOn = request.form.get("bedroom2Overhead")
        if isBedroom2OverheadOn != None:
            REALTIME_DATABASE.updateBedroom2OverheadStatus(True)
        else:
            REALTIME_DATABASE.updateBedroom2OverheadStatus(False)
        # Bedroom 2 lamp 1
        isBedroom2Lamp1On = request.form.get("bedroom2Lamp1")
        if isBedroom2Lamp1On != None:
            REALTIME_DATABASE.updateBedroom2Lamp1Status(True)
        else:
            REALTIME_DATABASE.updateBedroom2Lamp1Status(False)
        # Bedroom 2 lamp 2
        isBedroom2Lamp2On = request.form.get("bedroom2Lamp2")
        if isBedroom2Lamp2On != None:
            REALTIME_DATABASE.updateBedroom2Lamp2Status(True)
        else:
            REALTIME_DATABASE.updateBedroom2Lamp2Status(False)
        # Front door
        isFrontDoorOpen = request.form.get("frontDoor")
        if isFrontDoorOpen != None:
            REALTIME_DATABASE.updateFrontDoorStatus(True)
        else:
            REALTIME_DATABASE.updateFrontDoorStatus(False)
        # Back door
        isBackDoorOpen = request.form.get("backDoor")
        if isBackDoorOpen != None:
            REALTIME_DATABASE.updateBackDoorStatus(True)
        else:
            REALTIME_DATABASE.updateBackDoorStatus(False)
        # Garage door
        isGarageDoorOpen = request.form.get("garageDoor")
        if isGarageDoorOpen != None:
            REALTIME_DATABASE.updateGarageDoorStatus(True)
        else:
            REALTIME_DATABASE.updateGarageDoorStatus(False)
        # Guest bathroom overhead
        isGuestBathroomOverheadOn = request.form.get("guestBathroomOverhead")
        if isGuestBathroomOverheadOn != None:
            REALTIME_DATABASE.updateBathroom2OverheadStatus(True)
        else:
            REALTIME_DATABASE.updateBathroom2OverheadStatus(False)
        # Kitchen overhead
        isKitchenOverheadOn = request.form.get("kitchenOverhead")
        if isKitchenOverheadOn != None:
            REALTIME_DATABASE.updateKitchenOverheadStatus(True)
        else:
            REALTIME_DATABASE.updateKitchenOverheadStatus(False)

        # Save changes to database.
        REALTIME_DATABASE.commitChanges()

    # Get current status of every sensor and HVAC.
    currentStatus = {
        # Temperature status
        "ThermostatTemperature": REALTIME_DATABASE.getThermostatTemperature(),
        # Living Room status
        "isLivingRoomOverheadOn": REALTIME_DATABASE.getIsLivingRoomOverheadOn(),
        "isLivingRoomLamp1On": REALTIME_DATABASE.getIsLivingRoomLamp1On(),
        "isLivingRoomLamp2On": REALTIME_DATABASE.getIsLivingRoomLamp2On(),
        "isLivingRoomTVOn": REALTIME_DATABASE.getIsLivingRoomTVOn(),
        # Master Bedroom status
        "isMasterBedroomOverheadOn": REALTIME_DATABASE.getIsMasterBedroomOverheadOn(),
        "isMasterBedroomLamp1On": REALTIME_DATABASE.getIsMasterBedroomLamp1On(),
        "isMasterBedroomLamp2On": REALTIME_DATABASE.getIsMasterBedroomLamp2On(),
        "isMasterBedroomTVOn": REALTIME_DATABASE.getIsBedroomTVOn(),
        "isMasterBathroomOverheadOn": REALTIME_DATABASE.getIsBathroom1OverheadOn(),
        # Bedroom 1 status
        "isBedroom1OverheadOn": REALTIME_DATABASE.getIsBedroom1OverheadOn(),
        "isBedroom1Lamp1On": REALTIME_DATABASE.getIsBedroom1Lamp1On(),
        "isBedroom1Lamp2On": REALTIME_DATABASE.getIsBedroom1Lamp2On(),
        # Bedroom 2 status
        "isBedroom2OverheadOn": REALTIME_DATABASE.getIsBedroom2OverheadOn(),
        "isBedroom2Lamp1On": REALTIME_DATABASE.getIsBedroom2Lamp1On(),
        "isBedroom2Lamp2On": REALTIME_DATABASE.getIsBedroom2Lamp2On(),
        # Doors status
        "isFrontDoorOpen": REALTIME_DATABASE.getIsFrontDoorOpen(),
        "isBackDoorOpen": REALTIME_DATABASE.getIsBackDoorOpen(),
        "isGarageDoorOpen": REALTIME_DATABASE.getIsGarageDoorOpen(),
        # Miscellaneous status
        "isGuestBathroomOverheadOn": REALTIME_DATABASE.getIsBathroom2OverheadOn(),
        "isKitchenOverheadOn": REALTIME_DATABASE.getIsKitchenOverheadOn()
    }

    return render_template('index.html', status=currentStatus)

# data.html route
@app.route('/data', methods=['GET'])
def data():
    # Get all historical data from database.
    data = HISTORY_DATABASE.getAllHistoricalData()

    labels = []
    electricValues = []
    waterValues = []

    # Sort through data to be passed to HTML.
    for row in data:
        date = str(row["DateTime"])
        labels.append(date[:10])
        electricValues.append(row["TotalElectricityCost"])
        waterValues.append(row["TotalWaterCost"])
    
    # Find total cost of water and electricity.
    SumElectric = sum(electricValues)
    SumWater = sum(waterValues)

    totalBeforeRound = (SumElectric + SumWater)
    roundDec = f'{totalBeforeRound:.2f}'

    return render_template('data.html', labels=labels, electricValues=electricValues, waterValues=waterValues, roundDec=roundDec)

# about.html route
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

# Main driver function
if __name__ == '__main__':
    # Initialize the databases.
    REALTIME_DATABASE.connect()
    HISTORY_DATABASE.connect()

    # Run the app.
    # app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)