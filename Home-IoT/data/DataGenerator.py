# Approach
#   1. Generator runs for (X days of data divided into 30 seconds) iterations.
#      (i.e., loop will run for 90 days split into 30 second increments)
#   2. During each 30 second loop:
#      - adjust "current" date and time
#      - check for all events (i.e., door open = adjust indoor temperature)
#      - randomly trigger events (i.e., dishwasher is used 4x a week but on random days)
#      - make adjustments to all house data
#   3. Push to database at the end of each day.

import datetime
import random
from Temperature import getDailyTemperature
from HistoryDatabase import HistoryDatabase

############################################################################################

# This model will be updated to the database once everyday for 90 days.
CurrentData = {
    "DateTime": datetime.datetime.today() - datetime.timedelta(days=30),
    "ExteriorTemperature": 0,
    "TotalWatts": 0,
    "TotalElectricityCost": 0,
    "TotalGallons": 0,
    "TotalWaterCost": 0,
}

# Desired internal temperature of house.
DESIRED_INTERIOR_TEMPERATURE = 70

# Actual temperature of house.
ACTUAL_INTERIOR_TEMPERATURE = 70

# Returns cost of watts and gallons used.
def calculateCost(watts, gallons):
    # Electricity Cost
    # - $0.12 per kWh ( 1w = 1/1000 kw) 
    electricityCost = 0.12 * (watts/1000)

    # Water Cost
    # - $2.52 per 100 Cubic Feet of water 
    # - 1 Cubic Feet of water is 7.48 Gallons 
    # - 100 Cubic Feet is 748 Gallons 
    # - So 748 Gallons costs $2.52
    # - 1 gallon costs $0.00336898395
    waterCost = gallons * 0.00336898395

    return (electricityCost, waterCost)

# Checks if date is a weekday or weekend.
def checkIfWeekday(date):
    day = date.weekday()
    if (day < 5): # 0, 1, 2, 3, 4 = Mon-Fri
        return True
    else: # 5, 6 = Sat-Sun
        return False

def openDoors(date):
    # Exterior door is open 30 seconds each time a person enters or leaves the house 
    # Must open door between 5AM-7:30AM and 4PM-10:30PM
    # 3 exterior doors
    # For every 10 deg F difference in external temp, interior temp will +/- 2 deg F per 5 min door is open

    global DESIRED_INTERIOR_TEMPERATURE
    global ACTUAL_INTERIOR_TEMPERATURE
    isWeekday = checkIfWeekday(date)
    exteriorTemperature = CurrentData['ExteriorTemperature']
    
    # Get difference of exterior temperature and desired interior temperature.
    difference = abs(exteriorTemperature - DESIRED_INTERIOR_TEMPERATURE)

    if isWeekday:
        # Mon - Fri: 16 exits each day so (16 door opens x 30 seconds) = 480 seconds total
        # Therefore, there will be 1 occurrence of +/- 2 degree change.
        if exteriorTemperature >= DESIRED_INTERIOR_TEMPERATURE:
            # Since interior temperature changes 2 degrees for every 10 degree difference,
            # it will change 0.25 degrees for every 1.25 degree difference.
            ACTUAL_INTERIOR_TEMPERATURE += 0.25 * (difference // 1.25)
        else:
            ACTUAL_INTERIOR_TEMPERATURE -= 0.25 * (difference // 1.25)
    else:
        # Sat–Sun: 32 exit/enter events per day
        # 32 * 30 = 960 / 60 = 16 minutes of the door being opened 
        # Therefore, there will be 3 occurrences of +/- of 2 degree change. (6 degrees total)
        if exteriorTemperature >= DESIRED_INTERIOR_TEMPERATURE:
            # Since interior temperature changes 2 degrees for every 10 degree difference, it will
            # change 0.25 degrees for every 1.25 degree difference, or 0.75 degrees for 3 doors.
            ACTUAL_INTERIOR_TEMPERATURE += 0.75 * (difference // 1.25)
        else:
            ACTUAL_INTERIOR_TEMPERATURE -= 0.75 * (difference // 1.25)

    #print(ACTUAL_INTERIOR_TEMPERATURE, difference, exteriorTemperature, isWeekday)

def openWindows(date):
    # 8 total windows in house
    # Open Window - For every 10 deg F difference in external temp, interior temp will +/- 1 deg F per 5 min window is open
    global DESIRED_INTERIOR_TEMPERATURE
    global ACTUAL_INTERIOR_TEMPERATURE
    isWeekday = checkIfWeekday(date)
    exteriorTemperature = CurrentData['ExteriorTemperature']
    
    # Get difference of exterior temperature and desired interior temperature.
    difference = abs(exteriorTemperature - DESIRED_INTERIOR_TEMPERATURE)

    if isWeekday:
        # Mon-Fri: Assume 4 of 8 windows are open for 20 minutes each day.
        # Therefore, there will be 4 occurrences of +/- 1 degree change.
        if exteriorTemperature >= DESIRED_INTERIOR_TEMPERATURE:
            # Since interior temperature changes 1 degrees for every 10 degree difference,
            # it will change 0.125 degrees for every 1.25 degree difference.
            ACTUAL_INTERIOR_TEMPERATURE += (0.125 * 4) * (difference // 1.25)
        else:
            ACTUAL_INTERIOR_TEMPERATURE -= (0.125 * 4) * (difference // 1.25)
    else:
        # Sat-Sun: Assume 4 of 8 windows are open for 1 hour each day.
        # Therefore, there will be 12 occurrences of +/- 1 degree change.
        if exteriorTemperature >= DESIRED_INTERIOR_TEMPERATURE:
            # Since interior temperature changes 1 degrees for every 10 degree difference,
            # it will change 0.125 degrees for every 1.25 degree difference.
            ACTUAL_INTERIOR_TEMPERATURE += (0.125 * 12) * (difference // 1.25)
        else:
            ACTUAL_INTERIOR_TEMPERATURE -= (0.125 * 12) * (difference // 1.25)

def useHVAC(date):
    # HVAC Operation - +/- 1 deg F per minute of operation 
    # - HVAC will maintain the set temp within 2 degrees (i.e. if the inside temp goes beyond 2
    #   degrees of the set temp, then it will start operation to bring the temp back to the set temp).
    # - HVAC – 3500w
    global DESIRED_INTERIOR_TEMPERATURE
    global ACTUAL_INTERIOR_TEMPERATURE

    # Open all doors and windows for the given day to get the resulting interior temperature.
    openDoors(date)
    openWindows(date)

    # Get difference of actual interior temperature and desired interior temperature.
    difference = abs(ACTUAL_INTERIOR_TEMPERATURE - DESIRED_INTERIOR_TEMPERATURE)

    # Calculate how many minutes the HVAC had to run to bring house back to desired temperature.
    if difference > 2:
        totalMinutes = difference - 2
    else:
        totalMinutes = 0

    # Get total electricity used from total minutes the HVAC was running.
    totalElectric = (3500 / 60) * totalMinutes

    return totalElectric

def useRefrigerator():
    # 150w
    # Runs 24/7
    return 150 * 24

def useMicrowave(date):
    # 1100w
    isWeekday = checkIfWeekday(date)
    # Mon–Fri: 20 min/day 
    if isWeekday:
        return (1100 / 60) * 20

    # Sat–Sun: 30 min/day
    else:
        return (1100 / 60) * 30

def useStove(date):
    # 3500 watts
    isWeekday = checkIfWeekday(date)
    # Mon–Fri: 15 min/day 
    if isWeekday:
        return (3500 / 60) * 15

    # Sat–Sun: 30 min/day
    else:
        return (3500 / 60) * 30

def useOven(date):
    # 4000 watts 
    isWeekday = checkIfWeekday(date)
    # Mon–Fri: 45 min/day 
    if isWeekday:
        return (4000 / 60) * 45

    # Sat–Sun: 60 min/day
    else:
        return 4000

def useLivingRoomTV(date):
    # 636 watts
    isWeekday = checkIfWeekday(date)
    # Mon–Fri: 4 hrs/day 
    if isWeekday:
        return 636 * 4

    # Sat–Sun: 8 hrs/day
    else:
        return 636 * 8

def useBedroomTV(date):
    # 100 watts
    isWeekday = checkIfWeekday(date)
    # Mon–Fri: 2 hrs/day 
    if isWeekday:
        return 100 * 2

    # Sat–Sun: 4 hrs/day
    else:
        return 100 * 4

def useBath(date):
    # Shower – 25 gallons of water used (65% hot water, 35% cold water) 
    # Bath – 30 gallons of water used (65% hot water, 35% cold water)
    # Bath exhaust fan – 30w
    totalElectric = 0
    totalWater = 0

    isWeekday = checkIfWeekday(date)
    # Mon–Fri: 2 showers and 2 baths per day  
    if isWeekday:
        totalElectric += (30 / 60) * 30 # Exhaust (est. 30 mins for 4 showers/baths)
        totalWater += (25) * 2          # Showers
        totalWater += (30) * 2          # Baths

    # Sat–Sun: 3 showers and 3 baths per day 
    else:
        totalElectric += (30 / 60) * 45 # Exhaust (est. 45 mins for 6 showers/baths)
        totalWater += (25) * 3          # Showers
        totalWater += (30) * 3          # Baths

    # Calculate hot water heater usage
    # - 4500w 
    # - 4 minutes to heat 1 gallon of water
    # - 65% hot water, 35% cold water
    hotWaterAmount = (65 / 100) * totalWater
    minutesHotWaterHeaterInUse = 4 * hotWaterAmount
    totalElectric += (4500 / 60) * minutesHotWaterHeaterInUse

    return (totalElectric, totalWater)

def useDishwasher(date):
    # 1800 watts
    totalWater = 0
    totalElectric = 0

    # 4 loads of dishes per week (pick 4 random dates to use dishwasher)
    if date.weekday() in [1, 3, 5, 6]:
        totalElectric += (1800 / 60) * 45 # Runs 45 min per load
        totalWater += 6 # 6 gallons of hot water per load

        # Calculate hot water heater usage
        # - 4500w 
        # - 4 minutes to heat 1 gallon of water
        minutesHotWaterHeaterInUse = 4 * totalWater
        totalElectric += (4500 / 60) * minutesHotWaterHeaterInUse

    return (totalElectric, totalWater)

def useClothesWasher(date):
    # 500 watts
    totalWater = 0
    totalElectric = 0

    # 4 loads of clothes per week (pick 4 random dates to use clothes washer)
    if date.weekday() in [0, 2, 4, 6]:
        totalElectric += (500 / 60) * 30 # Runs 30 min per load
        totalWater += 20 # 20 gallons of water (85% hot water, 15% cold water) per load

        # Calculate hot water heater usage
        # - 4500w 
        # - 4 minutes to heat 1 gallon of water
        # - 85% hot water, 15% cold water
        hotWaterAmount = (85 / 100) * totalWater
        minutesHotWaterHeaterInUse = 4 * hotWaterAmount
        totalElectric += (4500 / 60) * minutesHotWaterHeaterInUse

    return (totalElectric, totalWater)

def useClothesDryer(date):
    # 3000 watts
    totalElectric = 0

    # 4 loads of clothes per week (pick 4 random dates to use clothes dryer)
    if date.weekday() in [0, 2, 4, 6]:
        totalElectric += (3000 / 60) * 30 # Runs 30 min per load

    return totalElectric

def useLights():
    # 8 total lights in house
    # All light Bulbs are 60w
    # Adults wake at 5AM, go to bed at 10:30PM 
    # Kids wake at 6AM, go to bed at 8:30PM 
    # Adults leave for work at 7:30AM, return home at 5:30PM 
    # Kids leave for school at 7:30AM, return home at 4PM

    # Given above details, the lights are estimated to be on from:
    # 5AM - 7:30AM (2.5 hours)
    # 4PM - 10:30PM (6.5 hours)
    return ((60 / 60) * (2.5 + 6.5)) * 8

# Uses every electrical applicance on given date.
def useElectricAppliances(date):
    return (useRefrigerator() + useMicrowave(date) + useStove(date) +
            useOven(date) + useLivingRoomTV(date) + useBedroomTV(date) +
            useLights() + useClothesDryer(date) + useHVAC(date) + random.randint(100,8000))

# Uses every water appliance on given date.
def useWaterAppliances(date):
    bathElectric, bathWater = useBath(date)
    dishwasherElectric, dishwasherWater = useDishwasher(date)
    clotheswasherElectric, clotheswasherWater = useClothesWasher(date)
    totalElectric = bathElectric + dishwasherElectric + clotheswasherElectric + random.randint(100,8000)
    totalWater = bathWater + dishwasherWater + clotheswasherWater + random.randint(20,60)
    return (totalElectric, totalWater)

############################################################################################

def GenerateHistoricalData():
    global CurrentData
    global ACTUAL_INTERIOR_TEMPERATURE

    # Amount of days of historical data (only edit this constant.. others are based on this)
    DAYS = 30

    # Start date and time of historical data
    TODAY = [int(i) for i in str(datetime.date.today()).split("-")]
    GENERATOR_DATETIME = datetime.datetime(TODAY[0], TODAY[1], TODAY[2], 0, 0, 0) - datetime.timedelta(days=DAYS)

    # Open connection to database.
    DATABASE = HistoryDatabase()
    DATABASE.connect()
    
    # Wipe HistoryTable before adding new data.
    DATABASE.wipeTable()

    print("Generating data...")
    for i in range(DAYS):

        # Get current temperature data from Weather API
        EXTERIOR_TEMPERATURE = round(getDailyTemperature(GENERATOR_DATETIME), 2)

        # Execute all tasks in house
        totalElectric, totalWater = useWaterAppliances(GENERATOR_DATETIME)
        totalElectric += useElectricAppliances(GENERATOR_DATETIME)

        # Update data model
        totalElectricityCost, totalWaterCost = calculateCost(totalElectric, totalWater)
        CurrentData["TotalWatts"] += round(totalElectric, 2)
        CurrentData["TotalGallons"] += round(totalWater, 2)
        CurrentData["TotalElectricityCost"] += round(totalElectricityCost, 2)
        CurrentData["TotalWaterCost"] += round(totalWaterCost, 2)
        CurrentData["ExteriorTemperature"] = EXTERIOR_TEMPERATURE

        # Check if it is the first iteration
        if (i != 0):
            # print("Attempting to insert historical data for date:", GENERATOR_DATETIME)

            # TODO: Push current day's data records to database
            DATABASE.insertHistoricalData(
                CurrentData["DateTime"],
                CurrentData["ExteriorTemperature"],
                CurrentData["TotalWatts"],
                CurrentData["TotalGallons"],
                CurrentData["TotalElectricityCost"],
                CurrentData["TotalWaterCost"]
            )
            
            # Reset data after pushing to database
            CurrentData = {
                "DateTime": GENERATOR_DATETIME,
                "ExteriorTemperature": EXTERIOR_TEMPERATURE,
                "TotalWatts": 0,
                "TotalElectricityCost": 0,
                "TotalGallons": 0,
                "TotalWaterCost": 0,
            }
            ACTUAL_INTERIOR_TEMPERATURE = 70

        # Add 30 seconds to generator's current datetime
        GENERATOR_DATETIME = GENERATOR_DATETIME + datetime.timedelta(days=1)
    
    print("Finished data generation.")

    # Commit changes to database.
    DATABASE.commitChanges()

    # Disconnect from database.
    DATABASE.disconnect()

# Test driver
if __name__=="__main__":
    GenerateHistoricalData()
    pass
