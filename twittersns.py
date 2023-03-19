import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime
from datetime import date
import pymongo
import json


def twitter(username,number):
    tweet_data=[]
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('{}'.format(username)).get_items()):
     if i > number :
       break
     else:
       tweet_data.append([tweet.date,tweet.id,tweet.url,tweet.content,tweet.user,tweet.replyCount, tweet.retweetCount,tweet.lang, tweet.source, tweet.likeCount])
    df=pd.DataFrame(tweet_data,columns=['date','id','url','content','user','replyCount','retweetCount','language','source','likeCounts'])
    df['date'] = df['date'].dt.date
    df1=df.loc[(df['date'] >= d1) & (df['date'] <= d2)]
    return df1


st.title('Twitter Scraping')

a=st.text_input('Enter the Keyword or Hashtag')
b=st.slider("Number of Tweets",0,1000)

d1=st.date_input('Scraped Data From')
d2=st.date_input('To')

c=st.button("Display Data")

if c:
    st.dataframe(twitter(a,b))

upload = st.button("Upload Data")
if upload:
   client=pymongo.MongoClient('mongodb+srv://vaidyanti:1234@cluster0.ee0zjto.mongodb.net/?retryWrites=true&w=majority')
   db=client.scraping
   coll=db.tweet
   tweet_dict=twitter(a,b).to_json()
   x={'Scraped Word' : a,'Scraped Date':datetime.datetime.now(),'Scraped Data':tweet_dict}
   coll.insert_one(x)
   st.write("Uploaded Successfully")
