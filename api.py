import requests
import json
token =  'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyIiwianRpIjoiYzViNTM2ZjYwYmJkNmUzODE5OTY1NDU5Y2NhMDdkYWZkZWZmOGNhYzFmMWFlM2M4ZjM0NDNlNTliNmRkNjNhOWY5M2RlYjZlOWE3M2RkOWYiLCJpYXQiOjE1ODI4Nzc5NzIsIm5iZiI6MTU4Mjg3Nzk3MiwiZXhwIjoxNjE0NTAwMzcyLCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.LO3h9dmRO3avdr0Xie6qju2SBYoN8Js283pRW2ajm1NGZeMRGB9mVBP0w6v7H4pkrvx1eAF0CFyFpEwWf5WF9FbEGbvBFMuVsYYfEQluAMYykPmR7RynXhBi_TVj7o2h7ZKK4RKCMqUdMD9R2S6K_ebtE0sfPn-Dh08pxwjYgx4ecpYImt0P6gfvhPON9tGzWrxd_GLeZ0Oqs5012v13gL1BKk45_op1_rovDG3o18eLk5ASYh38dkgT1My8zxN9Ommuz1EhDlwD0FcI_w6d1OYV0qprsxpvUUUT33tWeOhkC5Y1mViGGyPdQW3y08VGrUIaVGsPu6BpFx1whhDeDryTFY9FBv7dX3yhiz0mX51Tc5iOeIjXmy127PRBAzeYysHMG1I3WrE6It_LJ4r2BdVrLFfQc1zdNxC-KAy3CdwhHYsIYL9aGlSv2VPrXDRnNujF5nprZSTMbbgEbXW6ahAte2AyC6kFmfcl-Q-E2a7tCk_jMmo6lqiNR1RGhQjs-7j1SuNxvcVVm9mXO8z-L_k6Fh34SxkPD4_UR_EtGWV4XPpIEhxHJGzVfKR72LAgayfc5dnTZowKs2xMTsfAQLDLljuDmeDzgE1MIj1zgt9cQVQ9z5UUzfUiVQDMUW33uxQ07fasjFsGiGg9uQA6v_zO0epZ8c_Xl0bWbDGcNF0'
headers = {
            'Content-Type': "application/json",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Host': 'crawler-dev.digi-zaay.com.mm',
            'Accept-Encoding': "gzip, deflate",
            # 'Content-Length': "45",
            'Connection': "keep-alive",
            'cache-control': "no-cache",
            'Authorization':token
        }
url = "http://crawler-dev.digi-zaay.com.mm/api/current-crawling-pages"
result = requests.get(url,headers = headers)
datas = result.json()
json_data = json.dumps(datas,indent=4)
print(json_data)
# if datas:    
#     # for data in datas:
#         # p.collect_from_schedule(data["id"],data['url'])
#     print(f"Total {len(datas)} page to crawl")
# else:
#     print("There is no page to crawl")
