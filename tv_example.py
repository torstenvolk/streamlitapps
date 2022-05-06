import streamlit
from requests.api import request
import streamlit as st
import streamlit.components.v1 as components
import requests
import requests
import os
import json
import numpy as np
import pandas as pd
import time

################# Variables ###########
bearer_token = st.secrets["bearer_token"]
#bearer_token = os.environ.get("BEARER_TOKEN")
search_url = "https://api.twitter.com/2/tweets/search/recent"
metrics_url = "https://api.twitter.com/2/tweets/counts/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields


query_params = {'query':st.text_input('query', 'ema_research'), 'max_results':100,  'tweet.fields':'created_at,public_metrics'}
metrics_query_params = {'query':query)}


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
    st.table(df_show['text'])

	#json_response1 = connect_to_endpoint(metrics_url, metrics_query_params)
    #df1 = pd.DataFrame(json_response1)
    #st.write(df1)

if  __name__ == "__main__":
    main()
