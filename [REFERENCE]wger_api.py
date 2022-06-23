import requests, csv
from datetime import date

#dictionary of all wger API requests
request_URIs = {
    "day": "https://wger.de/api/v2/day/",
    "set": "https://wger.de/api/v2/set/",
    "setting": "https://wger.de/api/v2/setting/",
    "workout": "https://wger.de/api/v2/workout/",
    "templates": "https://wger.de/api/v2/templates/",
    "public-templates": "https://wger.de/api/v2/public-templates/",
    "workoutsession": "https://wger.de/api/v2/workoutsession/",
    "workoutlog": "https://wger.de/api/v2/workoutlog/",
    "schedulestep": "https://wger.de/api/v2/schedulestep/",
    "schedule": "https://wger.de/api/v2/schedule/",
    "daysofweek": "https://wger.de/api/v2/daysofweek/",
    "language": "https://wger.de/api/v2/language/",
    "license": "https://wger.de/api/v2/license/",
    "userprofile": "https://wger.de/api/v2/userprofile/",
    "setting-repetitionunit": "https://wger.de/api/v2/setting-repetitionunit/",
    "setting-weightunit": "https://wger.de/api/v2/setting-weightunit/",
    "exerciseinfo": "https://wger.de/api/v2/exerciseinfo/",
    "exercisebaseinfo": "https://wger.de/api/v2/exercisebaseinfo/",
    "exercise": "https://wger.de/api/v2/exercise/",
    "equipment": "https://wger.de/api/v2/equipment/",
    "exercisecategory": "https://wger.de/api/v2/exercisecategory/",
    "exerciseimage": "https://wger.de/api/v2/exerciseimage/",
    "video": "https://wger.de/api/v2/video/",
    "exercisecomment": "https://wger.de/api/v2/exercisecomment/",
    "muscle": "https://wger.de/api/v2/muscle/",
    "ingredient": "https://wger.de/api/v2/ingredient/",
    "ingredientinfo": "https://wger.de/api/v2/ingredientinfo/",
    "weightunit": "https://wger.de/api/v2/weightunit/",
    "ingredientweightunit": "https://wger.de/api/v2/ingredientweightunit/",
    "nutritionplan": "https://wger.de/api/v2/nutritionplan/",
    "nutritionplaninfo": "https://wger.de/api/v2/nutritionplaninfo/",
    "nutritiondiary": "https://wger.de/api/v2/nutritiondiary/",
    "meal": "https://wger.de/api/v2/meal/",
    "mealitem": "https://wger.de/api/v2/mealitem/",
    "weightentry": "https://wger.de/api/v2/weightentry/",
    "gallery": "https://wger.de/api/v2/gallery/",
    "measurement": "https://wger.de/api/v2/measurement/",
    "measurement-category": "https://wger.de/api/v2/measurement-category/"
}

headers = {
    'Accept':'application/json',
    'Authorization':'Token 91dad18afbc519b965b96ce6184e8e7aa880c8a6'
}

#check if there already exists an entry for today
def check_entry_date(results) -> bool:
    duplicate_date = False    
    if results[-1]["date"] == str(date.today()): #only need to check the last entry
        duplicate_date = True
   
    return duplicate_date

#get data from the API
def get_weight_data():
    response = requests.get(url=request_URIs["weightentry"], headers=headers)
    weight_data = response.json()
    return weight_data["results"]

#post a new entry
def set_weight_entry(weight):
    
    data = {
        "date":str(date.today()),
        "weight":float(weight),
    }

    results = get_weight_data()
    if check_entry_date(results) == False:
        response = requests.post(url=request_URIs["weightentry"], headers=headers, data=data)
    else:
        response = "Entry already submitted today."

    return response

#export "results" data to csv
def export_to_csv():
    results = get_weight_data()
    file_name = r'server\data\weight_data.csv'

    with open(file_name, "w", newline='') as outFile:
        csv_writer = csv.writer(outFile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)

        #enter the keys once as csv header
        formatted_data = results[0].keys()
        csv_writer.writerow(formatted_data)

        #iterate through list of dictionaries and extract values
        for element in results:
            #convert "weight" values from string to float for graph plotting
            element["weight"] = float(element["weight"])
            csv_writer.writerow(element.values())
        
        outFile.close()
    return file_name
