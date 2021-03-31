import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import math 

if __name__ == "__main__":
    # load table 
    df = pd.read_csv("RandomuserdataforAnalystcasestudy_2021-2-3_1516.csv")
    df['signup_date'] = pd.to_datetime(df['signup_date'])  
    df['age'] = df['signup_date'].dt.year - df['year_of_birth']
    df.hist(column='age')    
    # count number of successful transactions per unique user 
    # store them in a map from user id --> number of successful transactions
    user_to_num_successful_transactions = {}
    user_to_num_charge_failed_transactions = {}
    user_to_num_cancelled_transactions = {}
    user_to_age = {}
    users = {}
    for id in df.user_id.unique():
        df2 = df[df.user_id==id]
        user_to_num_successful_transactions[id] = len(df2[df2.status=='SUCCESS'])        
        user_to_num_charge_failed_transactions[id] = len(df2[df2.status=='CHARGE_FAILED'])        
        user_to_num_cancelled_transactions[id] = len(df2[df2.status=='CANCELLED'])        
        user_to_age[id] = df2.age.iloc[0]
       
    # iterate over the map and calculate different conversion rates 
    num_more_than_zero_successful_transactions = 0
    num_more_than_zero_charge_failed_transactions = 0
    num_more_than_zero_charge_failed_and_more_than_zero_success_transactions = 0
    num_more_than_one_successful_transactions = 0
    num_more_than_two_successful_transactions = 0
    num_more_than_zero_cancelled_transactions = 0
    num_more_than_zero_cancelled_and_more_than_zero_success_transactions = 0
    num_age_over_25_below_50_more_than_zero_charge_failed_transactions = 0
    num_age_over_25_below_50_more_than_zero_charge_failed_more_than_zero_success_transactions = 0
    num_age_over_49_more_than_zero_charge_failed_transactions = 0
    num_age_over_49_more_than_zero_charge_failed_more_than_zero_success_transactions = 0
    sum_of_successful_transactions = 0        
    num_nan_age = 0 
    num_nan_age_and_more_than_zero_success_transactions = 0 
    num_age_over_25_below_50 = 0
    num_age_over_25_below_50_more_than_zero_success_transactions = 0    
    num_age_over_49 = 0
    num_age_over_49_more_than_zero_success_transactions = 0 
    list_of_user_ids_no_dob_no_success_transactions = []
    list_of_user_ids_no_dob = []
    for id in user_to_num_successful_transactions:    
        num_success_per_user = user_to_num_successful_transactions[id]
        num_charge_failed_per_user = user_to_num_charge_failed_transactions[id]
        num_cancelled_per_user = user_to_num_cancelled_transactions[id]
        age_per_user = user_to_age[id]
        if num_success_per_user > 0:
            num_more_than_zero_successful_transactions += 1
        if num_success_per_user > 1:
            num_more_than_one_successful_transactions += 1        
        if num_success_per_user > 2:
            num_more_than_two_successful_transactions += 1
        if num_charge_failed_per_user > 0:
            num_more_than_zero_charge_failed_transactions += 1
        if num_charge_failed_per_user > 0 and num_success_per_user > 0:
            num_more_than_zero_charge_failed_and_more_than_zero_success_transactions += 1 
        if num_cancelled_per_user > 0:
            num_more_than_zero_cancelled_transactions += 1
        if num_cancelled_per_user > 0 and num_success_per_user > 0:
            num_more_than_zero_cancelled_and_more_than_zero_success_transactions += 1
        if math.isnan(age_per_user):
            num_nan_age += 1
            list_of_user_ids_no_dob.append(id)
        if math.isnan(age_per_user) and  num_success_per_user > 0:
            num_nan_age_and_more_than_zero_success_transactions += 1
        if math.isnan(age_per_user) and  num_success_per_user == 0:
            list_of_user_ids_no_dob_no_success_transactions.append(id)           
        if age_per_user > 25 and age_per_user < 50: 
            num_age_over_25_below_50 += 1            
        if age_per_user > 25 and age_per_user < 50 and num_success_per_user > 0: 
            num_age_over_25_below_50_more_than_zero_success_transactions += 1
        if age_per_user > 25 and age_per_user < 50 and num_charge_failed_per_user > 0: 
            num_age_over_25_below_50_more_than_zero_charge_failed_transactions += 1
        if age_per_user > 25 and age_per_user < 50 and num_charge_failed_per_user > 0 and num_success_per_user > 0: 
            num_age_over_25_below_50_more_than_zero_charge_failed_more_than_zero_success_transactions += 1            
        if age_per_user > 49: 
            num_age_over_49 += 1            
        if age_per_user > 49 and num_success_per_user > 0:              
            num_age_over_49_more_than_zero_success_transactions += 1
        if age_per_user > 49 and num_charge_failed_per_user > 0:              
            num_age_over_49_more_than_zero_charge_failed_transactions += 1
        if age_per_user > 49 and num_charge_failed_per_user > 0 and num_success_per_user > 0: 
            num_age_over_49_more_than_zero_charge_failed_more_than_zero_success_transactions += 1
         
           
    num_users_signed_up = len(user_to_num_successful_transactions)        
    conversion_rate_0 = num_more_than_zero_successful_transactions/num_users_signed_up
    print ("conversion rate 0:\t"+str(conversion_rate_0))
    conversion_rate_1 = num_more_than_one_successful_transactions/num_more_than_zero_successful_transactions
    print ("conversion rate 1:\t"+str(conversion_rate_1))
    conversion_rate_2 = num_more_than_two_successful_transactions/num_more_than_one_successful_transactions
    print ("conversion rate 2:\t"+str(conversion_rate_2))
    
    print("success ratio age>49:\t"+str(num_age_over_49_more_than_zero_success_transactions/num_age_over_49))
    print("success ratio 25<age<50:\t"+str(num_age_over_25_below_50_more_than_zero_success_transactions/num_age_over_25_below_50))
        
    # Alternative metrics:     
    # corresponds to num_more_than_one_successful_transactions/num_users_signed_up
    conversion_rate_01 = conversion_rate_0*conversion_rate_1 
    # corresponds to num_more_than_two_successful_transactions/num_users_signed_up
    conversion_rate_012 = conversion_rate_0*conversion_rate_1*conversion_rate_2
    
    # calculate some more statistics on num_successful_transactions
    npa = np.array(list(user_to_num_successful_transactions.values()))
    print ("min:\t" + str(np.min(npa)))
    print ("max:\t" + str(np.max(npa)))
    print ("argmax:\t" + str(max(user_to_num_successful_transactions, key=user_to_num_successful_transactions.get)))
    print ("median:\t" + str(np.median(npa)))
    print ("mean:\t" + str(np.mean(npa)))
    print ("std:\t" + str(np.std(npa)))

    # histogram plot of num_successful_transactions > 0 and < 100
    a = 0
    b = 100
    plt.hist(npa[(npa>a) & (npa<b)], bins = 100, rwidth=0.95)
    plt.show()
    
    # calculate some more statistics on user_to_age
    age_array = np.array(list(user_to_age.values()))
    age_array = age_array[~np.isnan(age_array)]
    print ("min:\t" + str(np.min(age_array)))
    print ("max:\t" + str(np.max(age_array)))
    print ("argmax:\t" + str(max(user_to_age, key=user_to_num_successful_transactions.get)))
    print ("median:\t" + str(np.median(age_array)))
    print ("mean:\t" + str(np.mean(age_array)))
    print ("std:\t" + str(np.std(age_array)))

    # histogram plot of user_to_age > 0 and < 100
    a = 0
    b = 100
    plt.hist(age_array[(age_array>a) & (age_array<b)], bins = 100, rwidth=0.95)
    plt.show()

    # create a subset of data with no date of birth   
    df3 = df[df['user_id'].isin(list_of_user_ids_no_dob)]
    df3.to_csv(r'list_of_user_ids_no_dob.csv', index=False)
    
    # create a subset of data with no date of birth and no successfull transactions   
    df4 = df[df['user_id'].isin(list_of_user_ids_no_dob_no_success_transactions)]
    df4.to_csv(r'list_of_user_ids_no_dob_no_success_transactions.csv', index=False)
        
    list_of_users_no_dob_at_least_one_success = [item for item in list_of_user_ids_no_dob if item not in list_of_user_ids_no_dob_no_success_transactions]
    df5 = df[df['user_id'].isin(list_of_users_no_dob_at_least_one_success)]
    df5.to_csv(r'list_of_users_no_dob_at_least_one_success.csv', index=False)

    