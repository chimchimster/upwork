import requests

response = requests.post('https://www.fsca.co.za/Fais/Search_FSP.htm', data={'Search_FSP_No': 2409})
print(response.text)