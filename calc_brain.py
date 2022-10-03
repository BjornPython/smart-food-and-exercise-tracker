import requests
from main2 import *
import os
import json


class AiBrain:

    def __init__(self):
        self.nutritionix_nutri_endpt = "https://trackapi.nutritionix.com/v2/natural"
        self.nutritionix_key = os.environ.get("NUTRITIONIX_KEY")
        self.nutritionix_id = os.environ.get("NUTRITIONIX_ID")
        self.HEADERS = {
            "x-app-id": self.nutritionix_id,
            "x-app-key": self.nutritionix_key,
            "content-type": "application/json"

        }
        self.date_now = dt.today().strftime("%m/%d/%y")
        self.total_calories = {"breakfast": {"food_cals": [], "total_calories": 0},

                               "lunch": {"food_cals": [], "total_calories": 0},

                               "dinner": {"food_cals": [], "total_calories": 0},

                               "snack": {"food_cals": [], "total_calories": 0},

                               "total_calories": 0
                               }

        self.total_protein = {"breakfast": {"food_pro": [], "total_calories": 0},

                              "lunch": {"food_pro": [], "total_calories": 0},

                              "dinner": {"food_pro": [], "total_calories": 0},

                              "snack": {"food_pro": [], "total_calories": 0},

                              "total_protein": 0
                              }

    def record_food(self, food_query, meal):
        meal = "breakfast"
        nutri_parameters = {
            "query": food_query
        }
        response = requests.post(url=f"{self.nutritionix_nutri_endpt}/nutrients",
                                 json=nutri_parameters, headers=self.HEADERS)
        foods = response.json()["foods"]

        body = self.get_nutri(foods, meal)

        self.update_cal_file()
        self.update_pro_file()
        return body

    def record_cardio(self, exercise_query):
        ecise_parameters = {
            "query": exercise_query
        }

        response = requests.post(url=f"{self.nutritionix_nutri_endpt}/exercise",
                                 json=ecise_parameters, headers=self.HEADERS)

        exercises = response.json()["exercises"]
        body = ""
        t_cals_burned = 0
        for ex in exercises:
            exercise = ex["name"]
            calories_burned = ex["nf_calories"]
            t_cals_burned += int(calories_burned)
            body += f"EXERCISE: {exercise}\nCALORIES BURNED: {calories_burned}.\n\n"
        body += f"TOTAL CALORIES BURNED: {t_cals_burned}"
        return body

    def get_nutri(self, foods, meal):
        body = ""
        t_cal = 0
        t_pro = 0
        for food in foods:
            food_name = food["food_name"]
            nf_calories = food["nf_calories"]
            nf_protein = food["nf_protein"]
            t_cal += int(nf_calories)
            t_pro += int(nf_protein)

            self.total_calories[meal]["food_cals"].append({food_name: nf_calories})
            self.total_protein[meal]["food_pro"].append({food_name: nf_protein})

            body += f"FOOD: {food_name}\nCALORIES: {nf_calories}\nPROTEIN: {nf_protein}\n\n"

        self.total_calories["total_calories"] += t_cal
        self.total_protein["total_protein"] += t_pro
        body += f"TOTAL PROTEIN: {t_pro}\nTOTAL CALORIES: {t_cal}"

        return body

    def update_cal_file(self):
        try:
            with open("cals_history.json", "r") as data_file:  # Loads the data if the file exists.
                data = json.load(data_file)
        except FileNotFoundError:  # If the file does not exist, create the file and dump the info.
            with open("cals_history.json", "w") as data_file:
                data = {self.date_now: self.total_calories}
                json.dump(data, data_file, indent=4)
        else:  # If the file exists, dump the data into the file.
            data[self.date_now] = self.total_calories

            with open("cals_history.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

    def update_pro_file(self):
        try:
            with open("pro_history.json", "r") as data_file:  # Loads the data if the file exists.
                data = json.load(data_file)
        except FileNotFoundError:  # If the file does not exist, create the file and dump the info.
            with open("pro_history.json", "w") as data_file:
                data = {self.date_now: self.total_protein}
                json.dump(data, data_file, indent=4)
        else:  # If the file exists, dump the data into the file.
            data[self.date_now] = self.total_protein

            with open("pro_history.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
