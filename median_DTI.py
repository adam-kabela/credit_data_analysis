"""
task 2.2
Sep 4, 2023
adam kabela
"""
import pandas

# is AMT_INCOME_TOTAL the client's annual income (or is it monthly and should by multiplied by 12?)
application_columns = ['SK_ID_CURR','AMT_INCOME_TOTAL','AMT_CREDIT','NAME_INCOME_TYPE']
application = pandas.read_csv('data/application_train.csv', usecols = application_columns)
#print(application.head(10)) # see a few rows to get a basic idea 

# we suppose that all items have the same CREDIT_CURRENCY
bureau_columns = ['SK_ID_CURR','CREDIT_ACTIVE','AMT_CREDIT_SUM']
bureau = pandas.read_csv('data/bureau.csv', usecols = bureau_columns)

active_credits = bureau[bureau['CREDIT_ACTIVE'] == 'Active']
active_credits_summed = active_credits.groupby('SK_ID_CURR')['AMT_CREDIT_SUM'].sum().reset_index(name ='CREDIT_TOTAL')
all_info_merged = pandas.merge(application, active_credits_summed, on ='SK_ID_CURR')

# add a new column DEBT_TO_INCOME = (CREDIT_TOTAL + AMT_CREDIT)/client's annual income
to_be_summed = ['CREDIT_TOTAL', 'AMT_CREDIT'] 
all_info_merged['DEBT_TO_INCOME'] = all_info_merged[to_be_summed].sum(axis=1) / all_info_merged['AMT_INCOME_TOTAL']

output = all_info_merged.groupby('NAME_INCOME_TYPE').agg({'DEBT_TO_INCOME': ['mean', 'size']})
output.columns = ['MEDIAN_DEBT_TO_INCOME', 'SAMPLE_SIZE']
output = output.sort_values('MEDIAN_DEBT_TO_INCOME')
print(output.head(10))
output.to_csv('median_DTI_output/median_DTI_by_income_type.csv')