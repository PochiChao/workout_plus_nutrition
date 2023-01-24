import requests
import os
from datetime import datetime

APP_ID = os.environ.get('APP_ID')
API_KEY = os.environ.get('API_KEY')
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
SHEETY_URL = os.environ.get('SHEETY_URL')

today = datetime.now()
minute = today.strftime('%M')
second = today.strftime('%S')

headers = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
    'x-remote-user-id': '0'
}

exercise_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'
exercise_input = input('Tell me which exercises you did: ')

data = {
    "query": exercise_input,
    "gender": "male",
    "weight_kg": 77,
    "height_cm": 173,
    "age": 28
}

exercise_response = requests.post(url=exercise_endpoint, json=data, headers=headers)
exercise_json = exercise_response.json()
print(exercise_json)

# THIS DOES NOT WORK - SHEETY APPARENTLY CANNOT ITERATE THROUGH MULTIPLE WORKOUTS IN ONE REQUEST?
# workouts_data = [{
#         'date': f'{today.day}/{today.month}/{today.year}',
#         'time': f'{today.hour}:{minute}:{second}',
#         'exercise': exercise['name'],
#         'duration': exercise['duration_min'],
#         'calories': exercise['nf_calories'],
#     } for exercise in exercise_json['exercises']]
#
# print(workouts_data)

exercise_headers = {
    'Authorization': f'Bearer {BEARER_TOKEN}'
}

for exercise in exercise_json['exercises']:
    workout_data = {
        'workout': {
            'date': f'{today.day}/{today.month}/{today.year}',
            'time': f'{today.hour}:{minute}:{second}',
            'exercise': exercise['name'].title(),
            'duration': exercise['duration_min'],
            'calories': exercise['nf_calories'],
        }
    }

    print(workout_data)

    sheety_url = SHEETY_URL

    sheety_add_row = requests.post(url=sheety_url, json=workout_data, headers=exercise_headers)
    print(sheety_add_row.text)
