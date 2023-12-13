# sqlalchemy-challenge
 This challenge was divided into two distinct parts:
 
 In the first part, we used SQLAlchemy to analyze a weather measurement database.
 We loaded in two tables, one with weather measurements and the other with station info.
 We filtered the final year of precipitation in the table and saved it to a pandas dataframe.
 Then we plotted the data, and last found the summary statistics
 The first thing we did with the station data was count the number of unique stations.
 We then used a row count to identify the most active station.
 We found the final year of temperature data from the most active station and saved it to a pandas dataframe.
 We then plotted the frequency of each temperature reading onto a histogram.

 In the second part, we used Flask to create an API to display the data.
 We created a landing page that displayed all available routes.
 One route has a dictionary of the final year of precipitation data.
 One has a list of all the station information.
 Another has the final year of temperature data from the most active station.
 The last route can display max/min/mean temperature data across any date range in the dataset.

 I used in-class examples to complete most of the assignment, with a quick peek back at the matplotlib module.
 I engaged with ChatGPT to debug my final branch and get the date ranges working properly.
