# IDS705 Machine Learning Final Project: The Tipping Point
<p align="center">
<img src="https://github.com/mjtv128/705-FinalProject/blob/main/26_images/chicago-bean.jpeg" width = "700" height = "400">
</p>

In 2009, Uber introduced the first ridesharing application, allowing users to "hail" a cab from their phones, which led to the rise in ridesharing platforms such as Lyft and Via. They subsequently incorporated a tip feature for riders to tip their drivers on top of the original fare. A research paper analyzed over 40 million Uber trips, and found approximately 15\% of rides ended with a tip, while nearly 60\% of riders never tip. Given the lowered rate of drivers' base salary, tips can be a crucial aspect of making ridesharing a profitable venture. A natural question for rideshare drivers is thus: “what makes a ride tip-worthy?” Are there strategic decisions drivers can make to increase their probability of receiving a tip? In this project, we analyzed rideshare data for Chicago between 2018 and 2020 to investigate the most important factors that impact tipping. We will also explore the trade-off between interpretability and accuracy, determining whether tips are predictable from available data and whether that prediction is understandable. 

## Data
In April 2019, Chicago required all ride-sharing companies to report data on rides beginning or ending within city limits. This data is available publicly, and contains the following information:
- Trip start time and end time (rounded to nearest 15 minutes)
- item Trip length (miles)
- item Trip duration (seconds)
- item Pickup and drop-off location (census tract)
- item Fare (rounded to nearest \$2.50)
- item Tip (rounded to nearest \$1)

The dataset can be found here: https://data.cityofchicago.org/Transportation/Transportation-Network-Providers-Trips/m6dm-c72p/data

We also used the weather API from the National Oceanic & Atmospheric Administration to include daily weather information in our analysis.

The dataset can be found here: https://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted

Due to the large size of the dataset, we used the Socrata Open Data API to retrieve the rideshare data. Specific instructions can be found below. 

## Experimental Design
<p align="center">
<img src="https://github.com/mjtv128/705-FinalProject/blob/main/26_images/flowchart3.png" width = "500" height = "900">
</p>

## Results
<p align="center">
  <img alt="Light" src="https://github.com/mjtv128/705-FinalProject/blob/main/26_images/roc_auc.png" width="45%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="Dark" src="https://github.com/mjtv128/705-FinalProject/blob/main/26_images/pr.png" width="45%">
</p>



