#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

Netflix_csv = pd.read_csv("Netflix.csv")


# In[2]:


Netflix_csv.shape


# In[3]:


Netflix_csv.head()


# In[4]:


Netflix_csv.info()


# In[5]:


Netflix_csv.isnull().sum()


# In[6]:


Netflix_csv.describe()


# In[7]:


Netflix_csv.duplicated()


# In[9]:


Netflix_csv.drop_duplicates()


# In[16]:


# get_ipython().system('pip install matplotlib')


# In[12]:


Netflix_csv.columns


# In[13]:


Netflix_csv.dtypes


# In[22]:


import matplotlib.pyplot as plt


# In[29]:


Netflix_csv.groupby("Region")["Monthly_Revenue"].sum().plot(kind="bar", ylabel="Monthly_Revenue", title="Region Wise Revenue")


# In[30]:


Netflix_csv.groupby("Subscription_Plan")["Rating"].mean().plot(
    kind="bar",
    ylabel="Rating",
    title="Subscription Wise Rating"
)

plt.show()


# In[31]:


Netflix_csv.groupby("Subscription_Plan")["Rating"].mean().plot(
    kind="pie",
    ylabel="Rating",
    title="Subscription Wise Rating"
)

plt.show()


# In[33]:


Netflix_csv.groupby("Category")["Rating"].mean().plot(
    kind="pie",
    ylabel="Rating",
    title="Category Wise Rating"
)

plt.show()


# In[36]:


Netflix_csv["Watch_Date"] = pd.to_datetime(Netflix_csv["Watch_Date"])

Netflix_csv.groupby(
    Netflix_csv["Watch_Date"].dt.to_period("M")
)["Monthly_Revenue"].sum().plot(
    kind="area",
    ylabel="Monthly Revenue",
    xlabel="Month",
    title="Month Wise Revenue"
)

plt.show()


# In[ ]:




