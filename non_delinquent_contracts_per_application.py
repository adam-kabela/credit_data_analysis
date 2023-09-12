"""
task 2.3
Sep 10, 2023
adam kabela
"""
import pandas
import matplotlib.pyplot

output_folder = 'non-delinquent_contracts_output/'

application_columns = ['SK_ID_CURR','NAME_CONTRACT_TYPE']
application = pandas.read_csv('data/application_train.csv', usecols = application_columns)
#print(application.head(3)) # see a few rows to get a basic idea
#name_contract_types = application.groupby(['NAME_CONTRACT_TYPE']).count()
#print(name_contract_types.head(20))
#ok, so the TRAIN data contain only two name_contract_types 'Cash loans' and 'Revolving loans' 
cash_application = application[application['NAME_CONTRACT_TYPE'] == 'Cash loans']
number_of_cash_appliactions = len(cash_application.index)

bureau_columns = ['SK_ID_CURR','SK_ID_BUREAU','CREDIT_TYPE']
bureau = pandas.read_csv('data/bureau.csv', usecols = bureau_columns)

bureau_balance_columns = ['SK_ID_BUREAU','MONTHS_BALANCE','STATUS']
bureau_balance = pandas.read_csv('data/bureau_balance.csv', usecols = bureau_balance_columns)
bureau_balance_no_DPD = bureau_balance[bureau_balance['STATUS'] == '0'] # 0 stands for non-delinquent

bureau_merged = pandas.merge(bureau, bureau_balance_no_DPD, on = 'SK_ID_BUREAU')
all_merged = pandas.merge(cash_application, bureau_merged, on = 'SK_ID_CURR')

result = all_merged.groupby(['MONTHS_BALANCE'])['SK_ID_BUREAU'].count() / number_of_cash_appliactions
result.columns = ['MONTHS_BALANCE', 'CNT_NO_DPD_CONTRACTS_AVG'] 
result.to_csv(output_folder + 'montly_development_of_non-delinquent_contracts_(relative_to_application_time).csv')

matplotlib.pyplot.figure(figsize = (20, 5))
chart = result.plot.bar(title='Montly development of non-delinquent contracts');
chart.set(xlabel="Months before application", ylabel="Average number of non-delinquent contracts\n per cash loan application")
matplotlib.pyplot.savefig(output_folder + 'montly_development_of_non-delinquent_contracts.pdf')  # saves the current figure

#to simplify calculations in tableau free trial
preprocessed_for_tableau = all_merged.groupby(['MONTHS_BALANCE','CREDIT_TYPE'])['SK_ID_BUREAU'].count().reset_index(name='CONTRIBUTION_TO_AVERAGE')
preprocessed_for_tableau['CONTRIBUTION_TO_AVERAGE'] = preprocessed_for_tableau['CONTRIBUTION_TO_AVERAGE'] / number_of_cash_appliactions
preprocessed_for_tableau.to_csv(output_folder + 'tableau_input.csv')