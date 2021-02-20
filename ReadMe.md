# AirGarage Low Quality Parking Lot Finder 
### Version 1.0 2/20/2021
### Author: Josh Burdett

1. This app takes user input in the following format: 'city, state', and returns a list of up to 50 low 
parking lots in thea area, listed in ascending order according to the metric: parking_lot_score

2. Parking_lot score is defined as: score = ( number of reviews * rating ) / (number of reviews + 1)

3. Yelp's API enables this app.  If a user enters an invalid city or state, the user will be redirected to an error 
page prompting them to enter a valid input.

4. Pandas dataframes are used to create the table of data according to AirGarage's API requirements. 

5. To run locally as a test web app, download the code directory and run app.py as a flask project.  Then open your browser and 
go to the following URL: http://127.0.0.1:5000/

6. Project requirements: https://www.notion.so/Lowest-Rated-Parking-Lots-Coding-Challenge-1e29d723606048bf833e6661cfd3aed5

7. Project dependencies: Python 3.7, YelpAPI, Pandas
