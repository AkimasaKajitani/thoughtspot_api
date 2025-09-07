import requests
from thoughtspot_rest_api_v1 import *

#-------------------------★使い方★-------------------------------------#
# このサンプルコードは、ThoughtSpotのREST APIをPythonで利用するためのサンプルコードです。
# 以下、事前に設定が必要です
# 1. thoughtspot_rest_api_v1 ライブラリを使用するため、PIPでインストールしてください。
# 2. 使用する場合は、ユーザー設定情報を更新してください
# 3. 「以下は必要に応じて追加」より下の部分は、実際に叩きたいAPIに応じて変更してください。
#-------------------------★使い方終わり★--------------------------------#


#-----------ユーザー情報設定(Start)----------#
#ThoughtSpotのURLとユーザー情報を設定
username = '<YOUR USERNAME>' #ログインするユーザー名
password = '<YOUR PASSWORD>' #ログインパスワード
org_id = 0 #Playgroundで「Get Current User Info」を叩くとすぐわかる
server = 'https://<YOUR TS NAME>.thoughtspot.cloud' #ログインするThoughtSpotインスタンスURL
#-----------ユーザー情報設定(End)----------#

#-----------FullToken取得(Start)----------#
ts: TSRestApiV2 = TSRestApiV2(server_url=server)
try:
    auth_token_response = ts.auth_token_full(username=username, password=password, org_id=org_id, validity_time_in_sec=36000)

    # Endpoints with JSON responses return the Python Dict form of the JSON response automatically
    ts.bearer_token = auth_token_response['token']

except requests.exceptions.HTTPError as e:
    print(e)
    print(e.response.content)
    exit()
#-----------FullToken取得(End)----------#


#-----------以下は必要に応じて追加----------#
# Get all Users with a particular privilege
search_request = {
  "record_offset": 0,
  "record_size": 10,
  "include_favorite_metadata": False,  # make sure to upper-case booleans
  "privileges": [
    "DATADOWNLOADING"
  ]
}
try:
    users = ts.users_search(request=search_request)
except requests.exceptions.HTTPError as e:
    print(e)
    print(e.response.content)
    exit()
for u in users:
    # get details of each table and do further actions
    user_guid = u['id']

print(f"Found {len(users)} users with DATADOWNLOADING privilege")

