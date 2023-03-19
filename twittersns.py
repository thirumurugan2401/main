Python 3.11.1 (tags/v3.11.1:a7a450f, Dec  6 2022, 19:58:39) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import streamlit as st
... from pymongo import MongoClient
... import snscrape.modules.twitter as sntwitter
... import pandas as pd
... import datetime
... import json
... 
... # creating page configuration
... st.set_page_config(
...         page_title="Twitter Scrapping",
... )
... st.header = "Twitter Scraping"
... 
... # Adding title to the app
... st.title('Twitter Scrapping')
... 
... # Initialize connection with mongoDB
... # Uses st.experimental_singleton to only run once.
... @st.experimental_singleton
... def init_connection():
...     return MongoClient('localhost', 27017)
... 
... 
... client = init_connection()
... 
... # Passing the arguments for scraping i.e. name of key ,staring date ,ending date and number of records
... def collect_twitter_data(search_keys,start_date_str,end_date_str,search_count):
...     try:
...         # Creating list to appendtweet data
...         tweets_list = []
...         for i, tweet in enumerate(sntwitter.TwitterSearchScraper("{keyword} since:{end_date} until:{start_date}".format       (keyword=search_keys,start_date=start_date_str,end_date=end_date_str)).get_items()):
...             if i > search_count:
...                 break
...             tweets_list.append(
                [tweet.date, tweet.id, tweet.url, tweet.content, tweet.replyCount, tweet.retweetCount, tweet.lang,
                 tweet.source, tweet.likeCount])

        # To see the tweets_list
        # print(tweets_list)

        # Creating dataframe from tweets list above
        tweets_df = pd.DataFrame(tweets_list,
                                 columns=['DateTime', 'User_ID', 'URL', 'Tweet_content', 'Reply_count', 'Retweet_count',
                                          'language', 'source', 'like_count'])
        data = tweets_df.to_dict(orient='record')
        return data,tweets_df
    except Exception as e:
        raise Exception(str(e))

def download_records(st):
    data = json.dumps(st,default=str)
    return data

def upload_data(data):
    try:
        if data:
            db = client['DW35']

            # Creating 'Scrapefromtwitter' collection in 'DW35' database
            collection = db['UploadsOfScrapefromtwitter']
            # Inserting documents into collection
            collection.insert_one(data)
    except Exception as e:
        raise Exception(str(e))

def get_csv_data(df):
    return df.to_csv(index=False).encode("utf-8")

# Creating search button
search_keywords = st.text_input("Search")
try:
    search_count = st.text_input("Count") or 10
    if search_count:
        search_count = int(search_count)
except Exception as e:
    search_count = 10
start_date = datetime.date.today()
endd_date_str = start_date.strftime("%Y-%m-%d")
end_date = start_date - datetime.timedelta(days=100)
start_date_str = end_date.strftime("%Y-%m-%d")

# Creating buttons for to take starting date,ending date
start_date_inp = st.date_input("Start Date").strftime("%Y-%m-%d") or start_date_str
endd_date_inp = st.date_input("End Date").strftime("%Y-%m-%d") or endd_date_str


# scrapping  data from twitter
if search_keywords:
    items,tweets_df = collect_twitter_data(search_keywords, endd_date_inp, start_date_inp,search_count)
    for item in items:
        st.write(item)
    start_date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    data = {search_keywords + start_date :items}
    # Creating button to download the data in json format
    st.download_button(label="Download Json",data=download_records(items),file_name="sample.json")
    # Creating button to download the data in csv format
    st.download_button("Download CSV",get_csv_data(tweets_df),"sample.csv","text/csv",key="download0-csv")
    # Creating button to upload the data retrieved from twitter to mongodb database
