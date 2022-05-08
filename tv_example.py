from requests.api import request
import streamlit as st
import streamlit.components.v1 as components
import requests
import os
import json
import numpy as np
import pandas as pd
import time
import streamlit.components.v1 as components


################# Variables ###########
bearer_token = st.secrets["bearer_token"]
#bearer_token = os.environ.get("BEARER_TOKEN")
search_url = "https://api.twitter.com/2/tweets/search/recent"
#metrics_url = "https://api.twitter.com/2/tweets/counts/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields


query_params = {'query':st.text_input('query', 'ema_research'), 'max_results':100,  'tweet.fields':'created_at,public_metrics'}



##########################################

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
	

def main():
    json_response = connect_to_endpoint(search_url, query_params)
    data_only = json_response["data"]
    df = pd.DataFrame(data_only)
	
    
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["created_at"] = df["created_at"].dt.strftime("%Y-%m-%d %H:%M:%S")

    df_show = df.set_index("created_at", inplace=False)
    st.table(df_show[['text','id']])



class Tweet(object):
    def __init__(self, s, embed_str=False):
        if not embed_str:
            # Use Twitter's oEmbed API
            # https://dev.twitter.com/web/embedded-tweets
            api = "https://publish.twitter.com/oembed?url={}".format(s)
            response = requests.get(api)
            self.text = response.json()["html"]
        else:
            self.text = s

    def _repr_html_(self):
        return self.text

    def component(self):
        return components.html(self.text, height=600)


#t = Tweet("https://twitter.com/OReillyMedia/status/901048172738482176").component()

t = Tweet("https://twitter.com/search?q=kubernetes").component()

	
if  __name__ == "__main__":
    main()
