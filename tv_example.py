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

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields

query = 'kubernetes'
query_params = {'query', 'max_results':100, 'tweet.fields':'created_at'}



##########################################

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    search = st.text_input('query', 'kubernetes')
    st.write(search)
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    #st.write(response)
    return response.json()


def main():
    json_response = connect_to_endpoint(search_url, query_params)
    data_only = json_response["data"]
    df = pd.DataFrame(data_only)

    # df["created_at"] = pd.to_datetime(df["created_at"])
    # df["created_at"] = df["created_at"].dt.strftime("%Y-%m-%d %H:%M:%S")

    df_show = df.set_index("created_at", inplace=False)
    st.table(df_show["text"])


if  __name__ == "__main__":
    main()
