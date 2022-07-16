#Dataset History
#Online Retail II dataset contains all the transactions occurring in a UK-based, online retail between 01/12/2009 and 09/12/2011.

#Variable Information
#InvoiceNo: Invoice number. A 6-digit number uniquely assigned to each transaction. If this code starts with the letter 'C', it indicates a cancellation.
#StockCode: Product (item) code. A 5-digit number uniquely assigned to each distinct product.
#Description: Product (item) name.
#Quantity: The quantities of each product (item) per transaction.
#InvoiceDate: The day and time when a transaction was generated.
#UnitPrice: Product price per unit in sterlin.
#CustomerID: A 5-digit number uniquely assigned to each customer.
#Country: The name of the country where a customer resides.

#Business Problem
#UK based retail company wants to segment its customers and wants to determine its marketing strategies according to these segments to increase the company's revenue.
# For this purpose, they want to do behavioural segmentation with respect to customers' purchase behaviours and preferences.

import datetime as dt
import pandas as pd
pd.set_option("display.max_columns",None)
# pd.set_option("display.max_rows",None)
from matplotlib import pyplot as plt
pd.set_option("display.float_format",lambda x: "%.3f" % x)


############################### TASK 1 ###############################

# Step 1: read excel file
df_ = pd.read_excel("WEEK_3/Bonus_ödevler/Online Retail RFM/online_retail_II.xlsx", sheet_name = "Year 2010-2011")
df = df_.copy()
df.head()

# Step 2: examine the dataset

def check_df(dataframe, head=5):
    print("############### shape #############")
    print(dataframe.shape)
    print("############### types #############")
    print(dataframe.dtypes)
    print("############### head #############")
    print(dataframe.head())
    print("############### tail #############")
    print(dataframe.tail())
    print("############### NA #############")
    print(dataframe.isnull().sum())
    print("############### Quantiles #############")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)

# Step 3: eliminate null values
df.dropna(inplace=True)
df.isnull().sum()

#Step 4: find the number of unique product
df["Description"].nunique()

#Step 5: find the number of each product
df["Description"].value_counts()

# Step 6: Sort the 5 most ordered products
df.groupby("Description").agg({"Quantity":"sum"}).sort_values(by = "Quantity", ascending=False).head(5)

# Step 7: if "C" is inside of the invoice, the order was canceled. This, we need to delete them.
df = df.loc[~df["Invoice"].str.contains("C", na=False)]

# Step 8: find the total income for each invoice
df["TotalPrice"] = df["Price"] * df["Quantity"]

############################### TASK 2 ###############################

# Step 1: Describe Recency, frequency and monetary

# Recency (Yenilik) : when the customer buy a product. One point is better than 10 points since one point is meaning that the customer bought a product one day ago. (Müşterinin yeniliği)

# Frequency (Sıklık) : a total number of buying product of the customer or total number of operation of the customer.

# Monetary (Parasal Değer) : a total number of price which customer sell.

# Step 2: estimate recency, frequency and monetary for each customer

df["InvoiceDate"].max()

today_date = dt.datetime(2011, 12, 11)

rfm = df.groupby("Customer ID").agg({"InvoiceDate": lambda x: (today_date - x.max()).days,
                                     "Invoice": lambda x: x.nunique(),
                                     "TotalPrice": lambda x: x.sum()})

rfm.columns = ["Recency", "Frequency", "Monetary"]

rfm = rfm.loc[rfm["Monetary"]>0,:]

print(rfm.head())

############################### TASK 3 ###############################

# Step 1: give point between 1-5 for recency, frequency and monetary
rfm["Recency_score"] = pd.qcut(rfm["Recency"],5, labels= [5, 4, 3, 2, 1])

rfm["Frequency_score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels = [1, 2, 3, 4, 5])

rfm["Monetary_score"] = pd.qcut(rfm["Monetary"],5, labels= [1, 2, 3, 4, 5])

rfm["RFM_SCORE"] = (rfm["Recency_score"].astype(str) + rfm["Frequency_score"].astype(str)) # in order to create score

rfm.head()

############################### TASK 4 ###############################

# Describe segment according to RFM_Score
seg_map = {
    r"[1-2][1-2]" : "hibernating",
    r"[1-2][3-4]" : "at_Risk",
    r"[1-2]5" : "cant_loose",
    r"3[1-2]" : "about_to_sleep",
    r"33" : "need_attention",
    r"[3-4][4-5]" :"loyal_customers",
    r"41" : "promising",
    r"51" : "new_customers",
    r"[4-5][2-3]" : "potential_loyalists",
    r"5[4-5]" : "champions"
}

rfm["segment"] = rfm["RFM_SCORE"].replace(seg_map, regex= True)

rfm.head()

############################### TASK 5 ###############################

# Analyze segments

colors  = ("darkorange", "darkseagreen", "orange", "cyan", "cadetblue", "hotpink", "lightsteelblue", "coral",  "mediumaquamarine","palegoldenrod")
explodes = [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]

rfm["segment"].value_counts(sort=False).plot.pie(colors=colors,
                                                 textprops={'fontsize': 12},
                                                 autopct = '%4.1f',
                                                 startangle= 90,
                                                 radius =2,
                                                 rotatelabels=True,
                                                 shadow = True,
                                                 explode = explodes)
plt.ylabel("");
