#!/usr/bin/env python
import sys
from crew1.crew import PythonCrew  

def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'description': """
        Think of a Python app called "MealSmart" that helps you figure out
        what to cook and what to buy for groceries. You just tell it what foods you like,
        what you're allergic to, and how much you want to spend, and it gives you a meal plan
        for the week along with recipes and a shopping list that changes if you tweak your meal plan. 
        It's built with Python using some handy tools to keep everything running smoothly on the web.
        """
    }

    # Kick off the crew with the provided inputs
    PythonCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()

