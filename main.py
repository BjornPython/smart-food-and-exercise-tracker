from TESTER_1 import *

calculator = aiBrain()

food = input("what did you eat?")
meal = input("what meal was that?")
calculator.record_food(food, meal)

cardio = input("What cardio did you do?")
calculator.record_cardio(cardio)
