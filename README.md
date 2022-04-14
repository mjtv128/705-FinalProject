# IDS705 Machine Learning Final Project: The Tipping Point
<p align="center">
<img src="https://github.com/mjtv128/705-FinalProject/blob/main/30_images/chicago-bean.jpeg" width = "700" height = "400">
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
<img src="https://github.com/mjtv128/705-FinalProject/blob/main/30_images/flowchart3.png" width = "500" height = "900">
</p>

## Results
We trained our data on a simple Logistic Regression model with variables that the drivers have autonomy over, a Logistic Regression model with all variables, a Random Forest Classifier and a XGBoost Classifier. All four models were evaluated on held-out test set from the period on which they were trained. The ROC curves and Precision/Recall (PR) curves are shown in Figure 1 below. As is visible from the AUC and average precision, XGBoost model performed the best, but all models did not achieve high performance. 

<p align="center">
  <img alt="Light" src="https://github.com/mjtv128/705-FinalProject/blob/main/30_images/roc_auc.png" width="45%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="Dark" src="https://github.com/mjtv128/705-FinalProject/blob/main/30_images/pr_title.png" width="45%">
</p>
<p align = "center">
Figure 1. ROC Curves for Four Final Models on Pre-covid Data 
</p>

We also evaluated generalization performance in a new time period. Specifically, we utilized data from April through July 2020. Theoretically, this new data was a strong test of generalization, because research suggested that tipping behavior did change during the pandemic \cite{CONLISK2021}. The ROC and PR curves are included here for this data in Figure 2 below. Surprisingly, the models performed similarly on data from this time period. In fact, the simple logistic regression performed noticeably better on this data than on the original test data. This indicated that despite relatively poor performance, our models were quite robust.
<p align="center">
  <img alt="Light" src="https://github.com/mjtv128/705-FinalProject/blob/main/30_images/roc_auc_cov.png" width="45%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="Dark" src="https://github.com/mjtv128/705-FinalProject/blob/main/30_images/pr_cov_title.png" width="45%">
</p>
<p align = "center">
Figure 2. ROC Curves for Four Final Models on Post-covid Data 
</p>

## Conclusion
Overall, the baseline logistic regression model appears to be the ideal model in this space. Machine learning methods with a more flexible form only marginally increased performance, while dramatically decreasing explainability and interpretation. The findings are consistent with previous research that suggests tipping behavior is difficult to predict, while extending the analysis to a new functional form (ride-share). Also, despite the pandemic, the models predicative ability remained steady during this new time frame.

However, there are some key limitations to this study. By nature, the analysis is only relevant for rides within Chicago, and even then only rides that begin and end within city boundaries. While only using 0.1\% of the total available data made analysis feasible, it also may have limited the insights available. Future work in this space could include a cloud-computing based approach to attempt a larger data sample. Continually, combination of rideshare data with survey data about passenger and driver characteristics could provide better insights.

## User Instructions
**Step 1: Clone the GitHub repository**
```
git clone https://github.com/mjtv128/705-FinalProject.git
```

**Step 2: Create a virtual environment for the project (pip or conda)**

**Step 3: Install required packages**
```
pip install -r requirements.txt
```

**Step 4: Download data**
This requires a Socrata Application Token, which can be obtained here: https://evergreen.data.socrata.com/. After receiving the token, enter it into the token field in `00_original_data/import_data.py`
```
python 00_original_data/import_data.py
```








