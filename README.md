# credit_data_analysis


Two data analysis tasks on credit data from Home Credit Kaggle Credit Risk.
Each task is solved with a separate short code using pandas.
The datasets are available as https://www.kaggle.com/competitions/home-credit-default-risk/data.

## A task on median DTI

For each credit application in the train dataset, consider the ratio of the total amount of all client's credits (including the credit in the application) over client's anual income.
Take groups of clients based on by their type of income, and calculate the median of the considered value for each group.


The ration is obtained as (CREDIT_TOTAL + AMT_CREDIT)/AMT_INCOME_TOTAL. The grouping is done by NAME_INCOME_TYPE.


## A task on non-delinquent contracts per application

For each credit application for cash loan in the train dataset, consider all previous credits of the client in credit bureau. 
Go month by month back in the past before the time of the application and track the number of non-delinquent contracts of the client.
For each month (relative to application time), sum these numbers and divide the sum by the total number of cash loan applications.
Relative to application times, the ratios give the averages of the number of non-delinquent contracts per application. 
Create a chart showing this average value changed in time (relative to application time).
Add a filter to consider only non-delinquent contracts based on the type of credit.


The cash loan type of application is indicated by NAME_CONTRACT_TYPE, the type of credit is in CREDIT_TYPE.
