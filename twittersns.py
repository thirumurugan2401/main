import streamlit as st
import datetime
import time
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo

# Empty list to store the data
tweets_list = []
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['Scraper']

# Create sidebar with required fields
with st.sidebar:
    option = st.radio("Search type", ("Keyword", "Hashtag"))
    key_or_hash = st.text_input('Type the '+option, value='Delhi')
    date_from = st.date_input('select the start date', value=datetime.date(2021, 6, 6))
    date_till = st.date_input('select the end date', value=datetime.date(2021, 8, 6))
    maxTweets = st.number_input('Set the limit of tweet to be extracted', 5, step=5)
    if key_or_hash:
        with st.spinner('Loading the data'):
            time.sleep(15)
    else:
        st.warning("Don't leave any field empty", icon="⚠")

# Scrape the required data
if option == "Keyword":
    for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper(f'{key_or_hash} since:{date_from} until:{date_till}').get_items()):
        if i > maxTweets:
            break
        tweets_list.append([tweet.date, tweet.id, tweet.rawContent, tweet.user.username, tweet.replyCount,
                            tweet.retweetCount, tweet.likeCount, tweet.lang, tweet.source])
else:
    for i, tweet in enumerate(
            sntwitter.TwitterHashtagScraper(f'{key_or_hash} since:{date_from} until:{date_till}').get_items()):
        if i > maxTweets:
            break
        tweets_list.append([tweet.date, tweet.id, tweet.rawContent, tweet.user.username, tweet.replyCount,
                            tweet.retweetCount, tweet.likeCount, tweet.lang, tweet.source])

# Convert data into dataframe
tweets = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Content', 'Username', 'Reply count',
                                            'Retweet count', 'Like count', 'Language', 'Source'])

# Show the data in table form
st.title("Twitter data scraper")
st.dataframe(tweets)

# Caching the data


@st.cache_data
def convert_csv(df):
    return df.to_csv()


c1, c2 = st.columns([4, 1])
if not tweets.empty:
    with c1:
        # Download as csv
        csv = tweets.to_csv()
        st.download_button(label='Download CSV', data=csv, file_name="Tweets.csv", mime='text/csv')

        # Download as json
        json_file = tweets.to_json(orient='records')
        st.download_button(label='Download JSON', data=json_file, file_name="Tweets.json", mime='application/json')

    with c2:
        # Upload data to mongodb
        if st.button('Upload'):
            col = key_or_hash
            col = col.replace(' ', '_')+'_Tweets'
            collection = db[col]
            data_dict = tweets.to_dict("records")
            if data_dict:
                collection.create_index('Tweet Id', unique=True)
                collection.insert_many(data_dict)
                st.success('Successfully uploaded into database', icon="✅")
            else:
                st.warning('No data to upload', icon="⚠")

else:
    st.warning("No data to download", icon="⚠")



if a and b:
  data1=twitter(a,b).to_json().encode()
  data2=twitter(a,b).to_csv().encode('utf-8')
  download1= st.download_button(
    label="Download data as json",
    data=data1,
    file_name='file.json')
  download2=st.download_button(
    label="Download data as csv",
    data=data2,
    file_name='myfile.csv')
