from __future__ import absolute_import,unicode_literals
from email import header
import json
import queue
from threading import Thread
from wsgiref import headers
from celery import shared_task
import requests
from authTokens.models import AuthToken
from django.core.cache import cache
import time


@shared_task
def trade_replication(*args, **kwargs):
    thread_list = []
    res={}
    que = queue.Queue()
    authtokens = cache.get('my_key')
    if authtokens is None:
        authtokens = AuthToken.objects.filter(id__range=(0,35))
        cache.set('my_key', authtokens)

    data = json.dumps({
    "orderStrategyType": "TRIGGER",
    "session": "NORMAL",
    "duration": "DAY",
    "orderType": "LIMIT",
    "price": 4,
    "orderLegCollection": [{
        "instruction": "BUY",
        "quantity": 5,
        "instrument": {
            "assetType": "EQUITY",
            "symbol": "AAPL"
        }
    }],
    "childOrderStrategies": [{
        "orderStrategyType": "OCO",
        "childOrderStrategies": [{
                "orderStrategyType": "SINGLE",
                "session": "NORMAL",
                "duration": "GOOD_TILL_CANCEL",
                "orderType": "LIMIT",
                "price": 2.00,
                "orderLegCollection": [{
                    "instruction": "SELL",
                    "quantity": 1,
                    "instrument": {
                        "assetType": "EQUITY",
                        "symbol": "AAPL"
                    }
                }]
            },
            {
                "orderStrategyType": "SINGLE",
                "session": "NORMAL",
                "duration": "GOOD_TILL_CANCEL",
                "orderType": "STOP",
                "stopPrice": 11.27,
                "orderLegCollection": [{
                    "instruction": "SELL",
                    "quantity": 5,
                    "instrument": {
                        "assetType": "EQUITY",
                        "symbol": "AAPL"
                    }
                }]
            }
           ]
        }]
    })
    print(authtokens.count(),"COUNT!!!!!!")

    start_time = time.time()
    for authtoken in authtokens:
        thread = Thread(target = lambda q, arg1: q.put({arg1.user:requests.post(url = "https://api.tdameritrade.com/v1/accounts/{}/orders".format(arg1.api_account_number),data=data,headers={'Content-type': 'application/json' , 'Authorization': "Bearer {}".format(arg1.api_access_token)}).elapsed.total_seconds()}), args = (que,authtoken))
        print(authtoken.api_account_number,"   API_ACCOUNT_NUMBER!!!!!!   ",  authtoken.api_access_token,"   API_ACCESS_TOKEN!!!!!")
        thread.start()
        thread_list.append(thread)
    
    print(len(thread_list),"  THREAD_COUNT!!!!!!")
    # sending post request and saving response as response object
    #r = requests.post(url = API_ENDPOINT,data=data,headers=headers)
    for thread in thread_list:
        thread.join()

    end_time = time.time()
    time_taken = end_time - start_time
    print('Time taken:', time_taken)
    total=0
    while not que.empty():
        result = que.get()
        res.update(result)
       
    #API_ENDPOINT = "https://api.tdameritrade.com/v1/accounts/{}/orders"
    print(total,"    SSSSSSSSSSSSSSSSS     ",res)
    # your API key here
    #ACCESS_TOKEN = "bdKAt4y0TJLl0BqGXzpHDA0W8/ObCz3Zy24EYhbBnBdvBUNM5SMOEegvc8TcCI6DNUNeaxsD54wvlWtuKcLXi65iRhKxfvWsHoIDgCxCxPeSHYUHCHznBKt21GJ0w4hSPJYb1cpLDBSgX5cLicPvkt+NZeZ8XUhwlW+WxD8gYYyu6df0Ex5RXnia4m5RgaFWGyEaBxvyN8Q/zxwBQI9U0g6u7bDkDKOrL+TkfVNvNtwFe+SWIdxT5za4s0httCm7fDqFpmBwHmyXORPR1b+lpYax52tf1Duyl90PQghbCtaZP8pNlIJBRdL2NX8MNsnyEM83TNftnKGykDhItPh+ProD1vq2m3LneJ/NP9EEAN02kSRALLVEgFVEYTySnqGBrvAtAOf4ILdJxBqL1SVJivGei9hksYxGRy2HG5O2EW0PLUtxUvyytoNMmPuIQVLErJOK2zf4D8w10mGEp9cEMktHRxw9qlQ0tPIOaDH6QvO+bM/1bG6E4kr6/Lgr09BJkfFnrizBxhMXWEo4nj6UIN97mQ2PnTTGsmFGNSXh76jrXtRwk100MQuG4LYrgoVi/JHHvl+Hv8vS3RJm30Dfp1WietgQdmKrI+7nh5eSb5vSi9iCx5NTOl57k7WPcrccibCsxvMCo9/og2jL5OZtEJGCt0TcUYXXL7YNiNYCghJArysDJ16vAAbBDFWrycR6AhVwRgJ/YctlqOqbQMR75wam5I/jnVUA6jlNiSlRxUZ6WdxrA3dBtIixl2vzM2Ssa4wOuIuXLuGtP8tZLM0xfv5dnE47KuSge97lAwTS1EL4ISbjnfI83eJSNnWL0JlwXIfsYej0s+DDwd6S8M8jwffLL/a/a6GI/QHd4U15PSOKJ1UeLYruczu2lONMr+g/Xd5Ub4SjnWubLObSUOElYMKsBsTBoFQHPMVQauIb7w++nN13rtFMuqHEh20WWut1WQIRwkJtXZCHhPR00FHCRUCoIFqMg/4apfji44QQqDqcdeX5H6rg/M3zzhl6I5pia2ztHQNghAyjzWYIEcWlmAQ6zUaiXabZYqGJMzflr6clrud9dIjCP9uU/Apigl9tIp8mdeeGC1CjCNGMDWowfO+Bj1Vpq9ewckXbxjs2jy/sdeaLzALi1w==212FD3x19z9sWBHDJACbC00B75E"
    
    #headers = {'Content-type': 'application/json' , 'Authorization': "Bearer {}".format(ACCESS_TOKEN)}
    # data to be sent to api


    # extracting response text 
    #print(r.status_code)
    
    


    