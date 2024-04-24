import pandas as pd
import numpy as np
import os

"""
To answer the following questions, make use of datasets: 
    'scheduled_loan_repayments.csv'
    'actual_loan_repayments.csv'
These files are located in the 'data' folder. 

All loans have a loan term of 2 years with an annual interest rate of 10%. Repayments are scheduled monthly.
A type 1 default will occur on a loan when a repayment is missed.
A type 2 default will occur on a loan when more than 15% of the expected total payments are unpaid for the year.

"""


def calculate_df_balances(df_scheduled,df_actual):
    """ 
        This is a utility function that creates a merged dataframe that will be used in the following questions. 
        This function will not be graded directly.

        Args:
            df_scheduled (DataFrame): Dataframe created from the 'scheduled_loan_repayments.csv' dataset
            df_actual (DataFrame): Dataframe created from the 'actual_loan_repayments.csv' dataset
        
        Returns:
            DataFrame: A merged Dataframe 

            Columns after the merge should be: 
            ['RepaymentID', 'LoanID', 'Month', 'ActualRepayment', 'LoanAmount', 'ScheduledRepayment']

            Additional columns to be used in later questions should include: 
            ['UnscheduledPrincipal', 'LoanBalanceStart, 'LoanBalanceEnd'] 
            Note: 'LoanBalanceStart' for the first month of each loan should equal the 'LoanAmount'

            You may create other columns to assist you in your calculations. e.g:
            ['InterestPayment']

    """

    #merges dataframes from both tbls
    df_merged = pd.merge(df_scheduled, df_actual, on=['LoanID'], how='left')  
    # extra paid on loan
    df_merged['UnscheduledPrincipal'] = df_merged['ActualRepayment'] - df_merged['ScheduledRepayment']
    
    df_merged['LoanBalanceStart'] = df_merged.groupby('LoanID')['LoanAmount'].shift(1).fillna(df_merged['LoanAmount'])
    df_merged['LoanBalanceEnd'] = df_merged['LoanBalanceStart'] - df_merged['ActualRepayment']

    #select relevant columns
    df_balances = df_merged[['RepaymentID', 'LoanID', 'Month', 'ActualRepayment', 'LoanAmount', 'ScheduledRepayment', 'UnscheduledPrincipal',  'LoanBalanceStart', 'LoanBalanceEnd']]
        
    return df_balances



#Do not edit these directories
root = os.getcwd()

if 'Task_2' in root:
    df_scheduled = pd.read_csv('data/scheduled_loan_repayments.csv')
    df_actual = pd.read_csv('data/actual_loan_repayments.csv')
else:
    df_scheduled = pd.read_csv('Task_2/data/scheduled_loan_repayments.csv')
    df_actual = pd.read_csv('Task_2/data/actual_loan_repayments.csv')

df_balances = calculate_df_balances(df_scheduled,df_actual)





def question_1(df_balances):
    """ 
        Calculate the percent of loans that defaulted as per the type 1 default definition 
        
        Args:
            df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function
        
        Returns:
            float: The percentage of defaulted loans (type 1)

    """

    #payment missed if actual repayment = 0
    defaulted_loans = df_balances.groupby('LoanID').apply(lambda x: (x['ActualRepayment'] == 0).any()).sum()
    #total number of loans in db
    total_loans = df_balances['LoanID'].nunique()
    default_rate_percent = (defaulted_loans / total_loans) * 100
    
    return default_rate_percent






def question_2(df_scheduled, df_balances):
    """ 
        Calculate the percent of loans that defaulted as per the type 2 default definition 
        
        Args:
            df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function
            df_scheduled (DataFrame): Dataframe created from the 'scheduled_loan_repayments.csv' dataset
        
        Returns:
            float: The percentage of defaulted loans (type 2)

    """

    #amounts expected for loans in that year
    total_expected_repayments = df_scheduled.groupby('LoanID')['ScheduledRepayment'].sum() * 12
    
    # total amount paid towards loan
    total_actual_repayments = df_balances.groupby('LoanID')['ActualRepayment'].sum()
    
    # percent unpaid for each loan
    unpaid_percent = ((total_expected_repayments - total_actual_repayments) / total_expected_repayments) * 100
    total_loans = df_balances['LoanID'].nunique()

    # percent of loans that are more than 15% unpaid
    default_rate_percent = unpaid_percent[unpaid_percent > 15].count() / total_loans * 100

    return default_rate_percent






def question_3(df_balances):
    """ 
        Calculate the anualized CPR (As a %) from the geometric mean SMM.
        SMM is calculated as: (Unscheduled Principal)/(Start of Month Loan Balance)
        CPR is calcualted as: 1 - (1- SMM_mean)^12  

        Args:
            df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function

        Returns:
            float: The anualized CPR of the loan portfolio as a percent.
            
    """

    smm = df_balances['UnscheduledPrincipal'] / df_balances['LoanBalanceStart']
    
    # geometric mean of SMM
    smm_mean = np.exp(smm.mean())
    
    #annualized CPR
    cpr_percent = 1 - (1 - smm_mean)**12

    return cpr_percent



def question_4(df_balances):
    """ 
        Calculate the predicted total loss for the second year in the loan term.
        Use the equation: probability_of_default * total_loan_balance * (1 - recovery_rate).
        The probability_of_default value must be taken from either your question_1 or question_2 answer. 
        Decide between the two answers based on which default definition you believe to be the more useful metric.
        Assume a recovery rate of 80% 
        
        Args:
            df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function
        
        Returns:
            float: The predicted total loss for the second year in the loan term.
            
    """
    recovery_rate = 0.8

    #assuming that scheduled payments include interest and that total loan balance is calculated at the end of the first year
    total_loan_balance = (df_balances['ScheduledRepayment'].sum()) * 12 - df_balances['ActualRepayment'].sum()

    probability_of_default = question_1 (df_balances)
    total_loss = probability_of_default * total_loan_balance * (1 - recovery_rate)
    

    return total_loss
