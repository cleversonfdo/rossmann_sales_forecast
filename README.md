## Disclaimer

This project is based on the dataset of Rossmann european drugstore. The data is available in kaggle site for a closed data competition. The values on the dataset are real, but the scenario used is ficticious. The source of the dataset and website company can be viewed on the links below:

https://www.kaggle.com/c/rossmann-store-sales

https://www.rossmann.de/de/

Due to machine processing limit, the raw dataset was randomly reduced to 500.000 rows.

# 1. Business Problem

Rossmann drugstore needs to know the sales forecast for all its pharmacies over the next 6 weeks. The purpose of this forecast is to account the revenue and thus plan a standardized renovation in the stores according to the local revenue of each one. As the company operates around 3000 drugstores in 7 European countries, the forecast of each store will vary greatly, assuming peculiar values. Each stores’s revenue is primarily influenced by promotions, competition, school and state holidays, seasonality and location.

# 2. Business Assumptions

## 2.1 Data Available

To forecast the sales the next data descriptions provided by the company will be assumed. Besides of that, the interval of the data comprends 30 months of sales of the hole company.

Most of the others fields are self-explantory.

- **Store:** a unique Id for each store
- **Sales:** the turnover for any given day
- **Customers:** the number of customers on a given day
- **Open:** an indicator for whether the store was open: 0 = closed, 1 = open
- **StateHoliday:** indicates a state holiday. Normally all stores, with few exceptions, are closed on state holidays. Note that all schools are closed on public holidays and weekends. A = public holiday, b = Easter holiday, c = Christmas, 0 = None
- **SchoolHoliday:** indicates if the Store was affected by the closure of public schools
- **StoreType:** differentiates between 4 different store models: a, b, c, d
- **Assortment:** describes an assortment level: a = basic, b = extra, c = extended
- **CompetitionDistance:** distance in meters to the nearest competitor store
- **CompetitionOpenSince[Month/Year]:** gives the approximate year and month of the time 	the nearest competitor was opened
- **Promo:** indicates whether a store is running a promo on that day
- **Promo2:** Promo2 is a continuing and consecutive promotion for some stores: 0 = store is not participating, 1 = store is participating
- **Promo2Since[Year/Week]:** describes the year and calendar week when the store started participating in Promo2
- **PromoInterval:** describes the consecutive intervals Promo2 is started, naming the months the promotion is started anew. E.g. "Feb,May,Aug,Nov" means each round starts in February, May, August, November of any given year for that store

## 2.2 Assumptions

- **CompetitionDistance:** it will assumed that when there is no values in this field the competition doesn’t exist at all. So the field will be filled with 200000 meters, a value much higher than the max distance provided by the dataset, which is 75860 meters. This field couldn’t be filled with zero, because wouldo no make sense and the Machine Learning model would be biased.
- **CompetitionOpenSince[Month/Year] and Promo2Since[Year/Week]:** for the NaN values of these fields, it will be assumed the date column value of the corresponding store row.
- **Sales:** if there is no sales, the store will be assumed as closed in that date.

# 3. Solution Strategy

## 3.1 Final Product

It will be delivered an online forecast product with sales by day granularity, so the managers can consult the sales prediction by cellphone with internet access.
The model applied was an regression model and the purpose of the model is sales prediction.

## 3.2 Tools

Python 3.8.0

Jupyter Notebook

Telegram App

Git and Github

## 3.3 Process
	
**Step 01.** Data Description: in this step some adaptations are made in the dataset so it is possible to identify dimension, types, presence of nan values and change types. Identify numerical and categorical features and appply some statistical metrics to analyze mean, median, maximum, minimum, range, skew, kurtosis and standard deviation.
**Step 02.** Feature Engineering: in this step new features are created and some are modified to better understand the columns date, competition and promo time interval and assortment and state holiday columns.
**Step 03.** Data Filtering: in this step some rows and columns are dropped if it doesn’t make sense for the project scope or there isn’t enough information to deal with that feature.
**Step 04.** Exploratory Data Analysis: in this step the data is analyzed to better understand the impact of the features in the project and model learn, and get insights from results.
**Step 05.** Data Preparation: in this step some transformations such as numerical and nature transformation are made to prepare the data for the machine learning model.
**Step 06.** Feature Selection: in this step Boruta Algorithm is used to select the better attributes  that better represents the target feature (sales) and use them to train the model.
**Step 07.** Machine Learning Modeling: in this step the machine learning model training is made and regardless of the result the XGBoost model was used for study purpose.
**Step 08.** Hyperparameter Fine Tunning: in this step the XGBoost model is tuned with some aditional hyperparameters to get the final model.
**Step 09.** Understang Model Performance for Business Results: this is the most important step where the model performance is translated to a business results.
**Step 10.** Deploy Model to Production: in this step the model is published in a cloud platform for other peoples or devices access the solution proposed. The cloud platform choosed was Heroku.
**Step 11.** Telegram Bot: in this step the already online tool is made available for the user from the Telegram App. The user will be able to request the performance of a store just by informing the store id.

# 4. Data Insights

Top three Hyphotesis:

**H1:** Stores should sell more through the years

False: even that the year 2015 is not finished yet, the amount of sells is decreasing, it’s a concern insight. 







**H2:** Stores should sell more on the second semester

False: The majority of sells are in the first seven months.






**H2:** Stores should sell more on the second semester

False: The majority of sells are in the first seven months.








**H3:** For each month, stores should sell more after the 10th day.

True: Although the mean sell decrease through the month, the amount of sell after the 10th day is above the amount of sells in the first 10 days.





# 5. Business Results

## 5.1 Machine Learning Performance

It was evaluated four machine learning models, they are: Linear Regression, Lasso, Random Forest Regressor and XGBoost Regressor. The table below ilustrates the cross-validation performance of each model tested.


Model Name
MAE CV
MAPE CV
RMSE CV
Linear Regression
2083.37+/-299.73
0.3+/-0.02
2953.27+/-471.41
Lasso
2118.62+/-343.52
0.29+/-0.01
3059.92+/-507.1
Random Forest Regressor
913.25+/-289.67
0.13+/-0.03
1361.05+/-447.88
XGBoost Regressor
7351.2+/-602.71
1.0+/-0.0
8003.64+/-702.78

Although the Random Forest Regressor model performed better, for study purpose the XGBoost Regressor was used. After the hyperparameter fine tuning the final model of machine learning get the performance ilustrated in the table below. Note that MPE is slightly negative, so the model are smoothly superestimating the sales.

Model Name
MAE
MAPE
RMSE
MPE
XGBoost Regressor
1021.659361
0.153375
1484.171493
-0.023586

## 5.2 Business Performance

The table below shows the final information get from product proposed with the most important business parameters to help the business team to make better decisions.

store
prediction
worst_scenario
best_scenario
MAE
MAPE
1
85812.804688
85377.153605
86248.455770
435.651082
0.096281
2
89881.062500
89394.285482
90367.839518
486.777018
0.106782
3
112075.726562
111530.881256
112620.571869
544.845306
0.073738
4
205741.937500
204548.615808
206935.259192
1193.321692
0.116214
5
83999.531250
83606.047877
84393.014623
393.483373
0.096854

In general, the results profit expected for all company in the next 6 weeks are in the table below.


Scenario
Values
prediction
R$137,971,264.00
worst_scenario
R$136,824,335.10
best_scenario
R$139,118,187.61


# 6. Conclusion

For the first iteration of the project cycle the final results is good enough to the business team starts to implement new better decisions, once the MAPE (Mean Absolute Percentage Error) is just 0.15. But, however, for some stores the MAPE error is too big, errors above 0.5. So for these stores the prediction of the model is much less accurate.

# 7. Next Steps

For the next iterations of the project cycle:
- the big errors encountered for some stores needs to analysed
- train the machine learning model with more parameters
- get more business information to better use the features
- increase the information provided by the app, such as best_scenario and worst_scenario, for example.

**Appendix:**

Telegram APP bot working:
