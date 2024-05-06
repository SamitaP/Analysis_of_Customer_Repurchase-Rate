# Analysis-of-Customer-Repurchase-Rate

The main.py file contains python code that performs task 1 and task 2.

Task 1: In the first step, code combines data from all the three files to one file. On combining Billing phone, Shipping phone, Billing zip, Shipping zip, Billing Street, Billing Address1, Billing Address2, ShippingStreet, Shipping Address1 & Shipping Address2 are cleansed and standardized by writing functions for each category of attribute and then calling those functions from main method.

Task 2: Using pandas I have created pivot table to calculate repurchase rate and plot a graph of rolling 20-day repurchase rate by week. The steps I took for this were starting from sorting the data by Email and Paid at attribute. Then I removed the data which was not needed for this analysis. Next step was to drop all the null attributes from the Email attribute since it cannot contribute to any stats (Considering they are unique). The following steps were to get the Purchase count for each customer, the cohort dates to calculate the difference between the repurchase and first purchase and finally a variable to track if the repurchase was made in a rolling window of 20 weeks. Since, this is the first time I have experienced such a problem I am assuming some of the details here. Lastly, I plot the table and the graph using the pandas pivot table function.
