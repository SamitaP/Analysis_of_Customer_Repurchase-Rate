# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 14:01:35 2017

@author: Samita
"""
import numpy as np
import pandas as pd
import os
import glob
import re
import string
from datetime import datetime

def reformatNumber(x):
    phone = re.sub(r'\D', '', x)
    # since area codes never start with 1
    phone = phone.lstrip('1')
    return '{}-{}-{}'.format(phone[0:3], phone[3:6], phone[6:])

def cleanZip(n):
    if re.search('[a-zA-Z]', n):
        return ""
    else:
        n = n.replace('\'','')[:5]
        if len(n)==4:
            return '0' + n
        else:
            return n

def cleanAddress(n):
    address = string.capwords(n)
    address = re.sub(r'\b(Avenue|Ave.)\b','Ave', address)
    address = re.sub(r'\b(Street|St.)\b','St', address)
    address = re.sub(r'\b(Road|Rd.)\b','Rd', address)
    address = re.sub(r'\b(Apartment|Apt.)\b','Apt', address)
    address = re.sub(r'\b(Drive|Dr.)\b','Dr', address)

def getPurchaseCounts(data):
    data['Email_previous'] = data['Email'].shift(1)  
    
    count = 1
    for index, row in data.iterrows():        
        if row['Email_previous'] == row['Email']:
            count += 1
            row['Purchase Count'] = count
        else:
            count = 1
            row['Purchase Count'] = count
    return data       
       # print(row['Email'],data.loc[index-1]['Email'])
def getCohortDates(data):
    for index, row in data.iterrows():
        if row['Purchase Count'] == 1:
            dateList = list()
            dateList.append(row['Paid at'])
            row['Cohort Date'] = row['Paid at']
        else:
            row['Cohort Date'] = dateList[0]
    return data

def getRepurchaseDate(data):
    date_format = "%Y-%m-%d %H:%M:%S %z"
    for index, row in data.iterrows():
        a = datetime.strptime(row['Paid at'], date_format)
        b = datetime.strptime(row['Cohort Date'], date_format)
        delta  = b - a
        delta = abs(delta.days)
        #if row['Paid at'] == row['Cohort Date']:
           # row['Repurchase Date'] = 'No Repurchase'
        if delta < 20:
            row['Repurchase Date'] = '<20'
        elif 20 < delta < 40 :
            row['Repurchase Date'] = '<40'
        elif 40 < delta < 60:
            row['Repurchase Date'] = '<60'
        elif 60 < delta < 80:
            row['Repurchase Date'] = '<80'
        elif 80 < delta < 100:
            row['Repurchase Date'] = '<100'
        elif 100 < delta < 120:
            row['Repurchase Date'] = '<120'
        elif 120 < delta < 140:
            row['Repurchase Date'] = '<140'
        elif 140 < delta < 160:
            row['Repurchase Date'] = '<160'
        elif 160 < delta < 180:
            row['Repurchase Date'] = '<180'
        elif 180 < delta < 200:
            row['Repurchase Date'] = '<200'
        elif 200 < delta < 220:
             row['Repurchase Date'] = '<220'
        elif 220 < delta < 240:
             row['Repurchase Date'] = '<240'
        elif 240 < delta < 260:
             row['Repurchase Date'] = '<260'
        elif 260 < delta < 280:
             row['Repurchase Date'] = '<280'
        elif 280 < delta < 300:
             row['Repurchase Date'] = '<300'
        elif 300 < delta < 320:
             row['Repurchase Date'] = '<320'
        elif 320 < delta < 340:
             row['Repurchase Date'] = '<340'
        elif 340 < delta < 360:
             row['Repurchase Date'] = '<360'
    return data
        
def main():
    path = r'C:\Users\Samita\Desktop\data'
    all_files = glob.glob(os.path.join(path, "*.csv"))   
    df_from_each_file = (pd.read_csv(f) for f in all_files)
    df = pd.concat(df_from_each_file, ignore_index=True)
    
    # cleaning phone number
    df['Billing Phone'] = df['Billing Phone'].dropna().map(lambda n: reformatNumber(n))
    df['Shipping Phone'] = df['Shipping Phone'].dropna().map(lambda n: reformatNumber(n))
    
    # cleaning zipcodes
    df['Billing Zip'] = df['Billing Zip'].dropna().map(lambda n: cleanZip(n))
    df['Shipping Zip'] = df['Shipping Zip'].dropna().map(lambda n: cleanZip(n))
    
    # cleaning address
    df['Billing Street'] = df['Billing Street'].dropna().map(lambda n: cleanAddress(n))
    df['Billing Address1'] = df['Billing Address1'].dropna().map(lambda n: cleanAddress(n))
    df['Billing Address2'] = df['Billing Address2'].dropna().map(lambda n: cleanAddress(n))
    df['Shipping Street'] = df['Shipping Street'].dropna().map(lambda n: cleanAddress(n))
    df['Shipping Address1'] = df['Shipping Address1'].dropna().map(lambda n: cleanAddress(n))
    df['Shipping Address2'] = df['Shipping Address2'].dropna().map(lambda n: cleanAddress(n))


    sort_on_email = df.sort_values(['Email','Paid at'])
    
    # copy columns needed for further analysis
    sort_on_email = sort_on_email.filter(['Name','Email','Paid at'], axis=1)
    
    # remove rows with similar email but no date of purchase(indicating entry is part of first order)
    #also remove any entry with no email as email is considered as unique id it cannot be derived from any other value
    task1 = sort_on_email.dropna()  
   
    # get purchase count
    task1['Purchase Count'] = ''
    task1 = getPurchaseCounts(task1)
    
    
    # get cohort dates
    task1['Cohort Date'] = ''
    task1 = getCohortDates(task1)
    
    # get repurchase date difference
    task1['Repurchase Date'] = ''
    task1 = getRepurchaseDate(task1)
    task1.to_csv('Output.csv', sep=',', encoding='utf-8')
    
    # select data we need
    task2 = pd.read_csv('Output.csv')
    task2 = task2[['Paid at','Purchase Count','Repurchase Date']]
    
    # convert Paid at to a datetime format
    task2['Paid at'] = pd.to_datetime(task2['Paid at'], coerce=True)
    
    # group by week and plot
    table = task2.set_index('Paid at').groupby('Repurchase Date').resample('w', how=sum).reset_index().pivot(index='Paid at', columns='Repurchase Date', values='Purchase Count')
    table2 = table.div(table.iloc[:,-1],axis=0).plot(kind="bar", stacked = True).legend()
    print(table)
    print(table2)
    
if __name__== "__main__":
    main()
