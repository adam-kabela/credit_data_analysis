"""
task 2.2
Sep 4, 2023
adam kabela
"""
import pandas

application_columns = ['SK_ID_CURR','AMT_INCOME_TOTAL','AMT_CREDIT','NAME_INCOME_TYPE']
application = pandas.read_csv('data/application_train.csv', usecols = application_columns)
#print(application.head(10)) # see a few rows to get a basic idea 
print("Number of applicaions:", len(application.index))

#is AMT_INCOME_TOTAL the client's annual income (or is it monthly and should by multiplied by 12?)
#credit_card_balance_columns = ['SK_ID_CURR','MONTHS_BALANCE','AMT_BALANCE','AMT_DRAWINGS_CURRENT','AMT_PAYMENT_TOTAL_CURRENT','AMT_TOTAL_RECEIVABLE']
#credit_card_balance = pandas.read_csv('data/credit_card_balance.csv', usecols = credit_card_balance_columns)
#spent_and_income = pandas.merge(application, credit_card_balance, on ='SK_ID_CURR')
#spent_and_income = spent_and_income[spent_and_income['AMT_BALANCE'] > 0]
#spent_and_income = spent_and_income.sort_values(['SK_ID_CURR','MONTHS_BALANCE'])
#spent_and_income.to_csv('amounts_to_maybe_look_at.csv')
#ok, AMT_INCOME_TOTAL is annual. This conclusion is based on this look, the resulting DTI values and googling...

# we suppose that all items have the same CREDIT_CURRENCY
bureau_columns = ['SK_ID_CURR','CREDIT_ACTIVE','AMT_CREDIT_SUM']
bureau = pandas.read_csv('data/bureau.csv', usecols = bureau_columns)

active_credits = bureau[bureau['CREDIT_ACTIVE'] == 'Active']
active_credits_summed = active_credits.groupby('SK_ID_CURR')['AMT_CREDIT_SUM'].sum().reset_index(name ='CREDIT_TOTAL')
incomplete_all_info_merged = pandas.merge(application, active_credits_summed, on ='SK_ID_CURR')
all_info_merged = pandas.merge(application, active_credits_summed, on ='SK_ID_CURR', how = 'left')
print("The wrong merge covered only:", len(incomplete_all_info_merged.index))
print("The left merge covers all:", len(all_info_merged.index))
#print(incomplete_all_info_merged.head(10))
#print(all_info_merged.head(10))

# add a new column DEBT_TO_INCOME = (CREDIT_TOTAL + AMT_CREDIT)/client's annual income
# if CREDIT_TOTAL is NaN, the sum treats it as 0
to_be_summed = ['CREDIT_TOTAL', 'AMT_CREDIT'] 
all_info_merged['DEBT_TO_INCOME'] = all_info_merged[to_be_summed].sum(axis=1) / all_info_merged['AMT_INCOME_TOTAL']
#print(all_info_merged.head(10))

output = all_info_merged.groupby('NAME_INCOME_TYPE').agg({'DEBT_TO_INCOME': ['mean', 'size']})
output.columns = ['MEDIAN_DEBT_TO_INCOME', 'SAMPLE_SIZE']
output = output.sort_values('MEDIAN_DEBT_TO_INCOME')
print(output.head(10))
output.to_csv('median_DTI_output/median_DTI_by_income_type.csv')
