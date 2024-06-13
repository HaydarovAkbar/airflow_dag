# # import requests
# # from requests.auth import HTTPBasicAuth
# #
# # url = "https://iskm.egov.uz:9444/oauth2/token"
# #
# # data = {
# #     "grant_type": "password",
# #     "username": "your_username",
# #     "password": "your_password"
# # }
# # consumer_key = "your_consumer_key"
# # consumer_secret = "your_consumer_secret"
# #
# # response = requests.post(url, data=data, auth=HTTPBasicAuth(consumer_key, consumer_secret))
# #
# # if response.status_code == 200:
# #     access_token = response.json().get("access_token")
# #     print("Access Token:", access_token)
# # else:
# #     print("Failed to get access token:", response.status_code, response.text)
#
#
# import requests
# import re
#
# login_url = 'https://dev.ttbooking.ru/login'
# username = '12345Rr+'
# password = 'd094h5ghs'
# login_payload = {
#     'username': username,
#     'password': password
# }
# session = requests.Session()
# login_response = session.post(login_url, data=login_payload)
# ttbooking_dev_session_value = None
#
# if login_response.status_code == 200:
#     set_cookie_header = login_response.headers.get('Set-Cookie')
#     pattern = r'ttbooking_dev_session=([^;]+)'
#
#     match = re.search(pattern, set_cookie_header)
#
#     if match:
#         ttbooking_dev_session_value = match.group(1)
#     else:
#         print("ttbooking_dev_session not found")
#
#     print('Login successful')
# else:
#     print('Login failed')
#     print(login_response.text)
#     exit(1)
# request_url = 'https://dev.ttbooking.ru/module/qsearch?term=пет'
#
# __ddg1_ = 'mpm4zZ49pXxnFY7sI925'
# _gid = 'GA1.2.1254322515.1718118818'
# _ga = 'GA1.1.1710589421.1718118818'
# _ga_EZYBVPZ6BD = 'GS1.1.1718118817.1.1.1718118926.0.0.0'
#
# Cookie = (f'__ddg1_={__ddg1_}; _gid={_gid}; _ga={_ga}; _ga_EZYBVPZ6BD={_ga_EZYBVPZ6BD};'
#           f'ttbooking_dev_session={ttbooking_dev_session_value}')
# print(Cookie)
# headers = {
#     'accept': 'application/json, text/plain, */*',
#     'accept-language': 'en-US,en;q=0.9,uz;q=0.8,ru;q=0.7',
#     'cookie': Cookie,
#     'priority': 'u=1, i',
#     'referer': 'https://dev.ttbooking.ru/module/avia-api',
#     'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
#     'x-requested-with': 'XMLHttpRequest',
#     'x-socket-id': '3802167153.3503833440',
# }
# print(headers)
# response = session.get(request_url, headers=headers)
# print(response.json())
#
#
# import requests
#
# url = 'https://dev.ttbooking.ru/module/qsearch?term=%D0%BF%D0%B5%D1%82'
#
# headers = {
#     'accept': 'application/json, text/plain, */*',
#     'accept-language': 'en-US,en;q=0.9,uz;q=0.8,ru;q=0.7',
#     'cookie': '__ddg1_=mpm4zZ49pXxnFY7sI925; _gid=GA1.2.1254322515.1718118818; _ga=GA1.1.1710589421.1718118818; _ga_EZYBVPZ6BD=GS1.1.1718118817.1.1.1718118926.0.0.0; ttbooking_dev_session=eyJpdiI6ImhXUlVOQ1JPWmpXS2lNelMvOTR1Z3c9PSIsInZhbHVlIjoiZEVlVWhOeWxtU1RCZGVxZ3RnWGJNSHNKZUx1STZ4c2ZtMm9kc0NhdTJyTXd3MjVHbnVhZ2pTTVlZMmFzTnNJcVlzRkhQSndSS3pYUDRHSmxaSW16RHRBTklpQ3E4L0pzdm9OSlRHSFdIUWgxa3NpdEV6Y0k5aE1EZk13Tm85SmYiLCJtYWMiOiIzN2I0NmQwZWYyYjYzODNjNTliZmE1M2U5OWE3YTUwN2Y4N2MzYWEzZjgwZDFhMjE5NTRhM2MzMjQ3NTYzMzdiIiwidGFnIjoiIn0%3D',
#     'priority': 'u=1, i',
#     'referer': 'https://dev.ttbooking.ru/module/avia-api',
#     'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
#     'x-requested-with': 'XMLHttpRequest',
#     'x-socket-id': '5498065436.2553535608'
# }
#
# response = requests.get(url, headers=headers)
#
# print(response.json())