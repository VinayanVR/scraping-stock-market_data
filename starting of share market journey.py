#!/usr/bin/env python
# coding: utf-8

# # Scraping Financial Data of the Stocks from Screener.com
# 
# TODO(Intro):
# 
# - Importing the library for scraping data with python
# - The libraries we are going to use are BeautifulSoup, Pandas, Requests
# 
# 

# Here are the Steps we will follow:
# - We are going to scape https://www.screener.in/explore/
# - We will get stock data  from all the sector (eg Chemical, Bank, Energy, Infrastructure etc...)
# - From each sector we will get the financial data of the list company(P/E ration, Book Value, 1year return etc..)
# - For each sector we will create a csv file to store the data
# 

# In[ ]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# ## Scraping the list of sector from Screener in
# 
# - use request to download the page
# - use Bs4 to prase and extract information
# - using pandas to convert it into a dataframe

# In[ ]:


# Getting the request from the website to fetch the data

url = "https://www.screener.in/explore/"
response = requests.get(url)
response.status_code


# In[ ]:


len(response.text)


# In[ ]:


# using beautifulsoup to parse the data from the website

soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())


# ![](https://imgur.com/aYqu5jb.png)

# In[ ]:


# Getting a tags that contains the name and link to the financial data of the company

selection_class = 'bordered radius-6 padding-4-12 font-size-14 ink-700'
topic_title  = soup.find_all('a', {'class': selection_class})
topic_title


# In[ ]:


# Creating a loop for  getting all the name of the sector

topic_tag = []
for tag in topic_title:
    topic_tag.append(tag.text.replace('/',"").strip())
topic_tag 


# In[ ]:


# Creating a loop for  getting all the link to the sectors financial data

base = "https://www.screener.in"
topic_url = []
for tag in topic_title:
    topic_url.append(base + tag['href'])
    
print(topic_url[0])


# In[35]:


# creating a dataframe from the scraped data

market_data = {'title' : topic_tag, 'url': topic_url}
market_df = pd.DataFrame(market_data)
market_df


# In[ ]:


# Craeting a csv file to store the data

market_df.to_csv(r"C:\Users\g\Pictures\Begining story of stock market\market_analysis.csv", index = None)


# ##  Now we have name of the each sector and link to the financial data
# 
# - Now we are going scarpe data from the chemical sector and all the listed company financial data
# - Then we are going to make  a Dataframe out of it and going to save it to a csv file
# - After that we are going to create a function that will automatically get data from all the sector
#   and we are going to save all of them in a csv format.

# In[ ]:


# Getting the request from the website and parsing the data

topic_urls =  topic_url[23]
topic_urls


# In[ ]:


response = requests.get(topic_urls)
response.status_code


# In[ ]:


soup = BeautifulSoup(response.text, "html.parser")
soup.prettify()


# ![](https://imgur.com/MI9QD6O.png)

# In[ ]:


# Getting the heading of the table that content all the financial aspect of the company 

table = 'data-table text-nowrap striped mark-visited'
table_tag = soup.find_all('table', {'class': table})
table_tag[0].text


# In[ ]:


tr_tag =table_tag[0].find_all('tr')[0]
tr_tag


# In[ ]:


a_tag = tr_tag.find_all('a')
n =a_tag[10]
n.text[:30].strip()


# In[ ]:


heading = []
for x in tr_tag.find_all('a'):
    heading.append(x.text[:28].strip())
    
heading


# In[ ]:


# Getting the  table that content all the financial ratio of the company 

table_value = []
for x in table_tag[0].find_all('tr')[1:]:
    td_tags = x.find_all('td')
    td_val = [y.text.strip() for y in td_tags]
    table_value.append(td_val)
    
table_value    


# In[36]:


# Converting that into csv file and storing it

df = pd.DataFrame(table_value, columns = heading, index = None)
market_df = df[df.astype(str)['Name']!='None']
market_df


# In[37]:


# Then form that link we are going to scrape financial data from each sector

def get_topic_page(url):           
    response = requests.get(url)    ## Pulling the request
    if response.status_code!= 200:
        raise Exception('Failed to load page{}'.format(url))
    topic_doc = BeautifulSoup(response.text, 'html.parser')   ##parsing the data
    return topic_doc

def get_topic_title(topic_doc):
    table = 'data-table text-nowrap striped mark-visited'       ## Getting the table tag 
    table_tag = topic_doc.find_all('table', {'class': table})   ##that contains the title
    tr_tag =table_tag[0].find_all('tr')[0]
    heading = []
    for x in tr_tag.find_all('a'):
        heading.append(x.text[:28].strip())
    return heading

def data(topic_doc):
    table = 'data-table text-nowrap striped mark-visited'          ## Getting the table  tag
    table_tag = topic_doc.find_all('table', {'class': table})      ## that cntains  financial ratio 
    table_value = []                                               ## of the company
    for x in table_tag[0].find_all('tr')[1:]:
        td_tags = x.find_all('td')
        td_val = [y.text.strip() for y in td_tags]
        table_value.append(td_val)
    return pd.DataFrame(table_value, columns = heading, index = None)

def scrap_topic(topic_url, topic_name):
    topic_df = data(get_topic_page(topic_url))                      #3 saving the file as csv
    market_df = topic_df[topic_df.astype(str)['Name']!='None']      
    path = r'C:\Users\g\Pictures\Begining story of stock market\ '
    
    market_df.to_csv(path+ topic_name +'.csv',index = None)
    
    


# In[38]:


# Instead of repeating the process for each sector we are going to create a
# function that pull data from csv file we are going to create

# First we are going get the name of sector and link to the sector

doc = BeautifulSoup(response.text, 'html.parser')


def get_topic_title(doc):
    selection_class = 'bordered radius-6 padding-4-12 font-size-14 ink-700'
    topic_title  = doc.find_all('a', {'class': selection_class})
    topic_tag = []        
    for tag in topic_title:
        topic_tag.append(tag.text.replace('/',"").strip())
    return topic_tag 

def topic_url(doc):
    selection_class = 'bordered radius-6 padding-4-12 font-size-14 ink-700'
    topic_title  = doc.find_all('a', {'class': selection_class})
    base = "https://www.screener.in"
    topic_url = []
    for tag in topic_title:
        topic_url.append(base + tag['href'])
    return topic_url
        
def scrape_topic():
    url = "https://www.screener.in/explore/"
    response = requests.get(url)
    if response.status_code!= 200:
        raise Exception('Failed to load page{}'.format(url))
    soup = BeautifulSoup(response.text, 'html.parser')
    market_data = {'title' : get_topic_title(soup), 'url': topic_url(soup)}
    market_df = pd.DataFrame(market_data)
    return market_df



# In[39]:


# Now  we are going to  scrape the data and going to save it
def scrape_stock_data():                     
    print('scraping data from screener.com')       ## creating a loop to get data of all the company
    topic_df = scrape_topic()
    for index, row in topic_df.iterrows():
        print('scraping top respositories for "{}"'.format(row['title']))
        scrap_topic(row['url'], row['title'])


# In[40]:


scrape_stock_data()


# ![](https://imgur.com/A8ZeUan.png)

# In[ ]:




