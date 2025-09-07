import requests
import json

#-------------------------★使い方★-------------------------------------#
# このサンプルコードは、ThoughtSpotのREST APIをPythonで利用するためのサンプルコードです。
# ライブラリを使用しないため冗長なコードになっています。
# 以下、事前に設定が必要です
# 1. 使用する場合は、ユーザー設定情報を更新してください
# 2. 「以下は必要に応じて追加」より下の部分は、実際に叩きたいAPIに応じて変更してください。
#-------------------------★使い方終わり★--------------------------------#



#-----------ユーザー情報設定(Start)----------#
#ThoughtSpotのURLとユーザー情報を設定
thoughtspot_url = "https://<YOUR TS URL>.thoughtspot.cloud" #★変更必要★
org_id = 0 #Playgroundで「Get Current User Info」を叩くとすぐわかる
post_data = {
  "username": "<YOUR USERNAME>", #★変更必要★
  "password": "<YOUR PASSWORD>", #★変更必要★
  "validity_time_in_sec": 300, # 変更不要ですが必要に応じて変更可能です
  "org_id" : org_id,   # 変更不要(指定しなくても動くと思います)
  "auto_create": False # 変更不要
}
#-----------ユーザー情報設定(End)----------#

#-----------基本設定(Start)----------#
api_version = '2.0'
base_url = '{thoughtspot_url}/api/rest/{version}/'.format(thoughtspot_url=thoughtspot_url, version=api_version)
api_headers = {
    'X-Requested-By': 'ThoughtSpot',
    'Accept': 'application/json'
}
#-----------基本設定(End)----------#

#-----------FullToken取得(Start)----------#
#Get Full Access Token
api_endpoint_ending = "auth/token/full"

# Create a new Session object
requests_session = requests.Session()
# Set the headers for all uses of the requests_session object
requests_session.headers.update(api_headers)
# Define the JSON message, in Python object syntax (close but not exactly JSON)
json_post_data = post_data
# Set the URL of the endpoint
url = base_url + f"{api_endpoint_ending}" #チュートリアル通りだと動かないので「f」を追加

try:
    # Issue the HTTP request and store the response to a variable
    resp = requests_session.post(url=url, json=json_post_data)

    # This method causes Python Exception to throw if status not 2XX
    resp.raise_for_status()

    # Retrieve the JSON body of response and convert into Dict
    # Some endpoints returns 204 not 200 for success, with no body, will error if you call .json() method
    resp_json = resp.json()
    #print(json.dumps(resp_json, indent=2)) #レスポンスの中身を全部見たいときはコメントアウトを外す
    token = resp_json["token"]
    print("Here's the token:")
    print(token)

except Exception as e:
    print("Something went wrong when trying to get a token:")
    print(e)
    print(e.request)
    print(e.request.url)
    print(e.request.headers)
    print(e.request.body)
    print(e.response.content)
    exit(1)

# Update api_headers from before with header for Bearer token
api_headers['Authorization'] = 'Bearer {}'.format(token)
requests_session.headers.update(api_headers)
#-----------FullToken取得(End)----------#

#-----------以下は必要に応じて追加----------#
# Example: Search for users
user_search_url = base_url + "users/search"
json_post_data = {
  "record_offset": 0,
  "record_size": 10,
  "include_favorite_metadata": False
}
# Every request must be wrapped in try...except
try:
    search_resp = requests_session.post(url=user_search_url, json=json_post_data)
    search_resp.raise_for_status()
except Exception as e:
    print("Something went wrong when trying to get a token:")
    print(e)
    print(e.request)
    print(e.request.url)
    print(e.request.headers)
    print(e.request.body)
    print(e.response.content)
    exit(1)


print("Here's the user search response:")
print(search_resp.json())