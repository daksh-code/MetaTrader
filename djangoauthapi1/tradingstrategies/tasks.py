from __future__ import absolute_import,unicode_literals
from importlib.resources import contents
import json
from pickle import PUT
import queue
from statistics import quantiles
from symtable import Symbol
from textwrap import indent
from tkinter import SINGLE
from urllib import request
from wsgiref import headers
from celery import shared_task
from fileinput import close
from tkinter.filedialog import Open
from trade_replicator.tasks import trade_replication
from tda.auth import easy_client
from tda.client import Client
from tda.streaming import StreamClient
from asgiref.sync import sync_to_async
import ssl
import datetime
ssl._create_default_https_context = ssl._create_unverified_context
import asyncio
from .models import Stock, Strategy
from django.forms.models import model_to_dict
from djangoauthapi1.celery import app
from django.core.cache import cache
from django_redis import get_redis_connection
import pandas as pd
import copy

stock_strategy_map = {}

@shared_task(bind=True,queue="streaming_queue")
def data_streaming(*args, **kwargs):
    """stocks=Stock.objects.filter(stock_is_active=True)  
    strategies = Strategy.objects.filter(strategy_is_active=True).values('stock__symbol', 'name')
    global stock_strategy_map 
    for strategy in strategies:
        stock_symbol = strategy['stock__symbol']
        strategy_name = strategy['name']
        stock_strategy_map[stock_symbol] = strategy_name
 
    print(strategies,"QQQQQQQQQQQQQQQQ")
    stock_list=[]
    for stock in stocks:
        stock_list.append(stock.symbol)"""

    client = easy_client(
            api_key='EBJQOOZWSLMKMB4ALAXTEDX7AASBDES2@AMER.OAUTHAP',
            redirect_uri='https://localhost',
            token_path='/Users/dakshdagariya/Downloads/djangoreactjsauth1-master/djangoauthapi1/tradingstrategies/td_state.json')

    print(client,"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    stream_client = StreamClient(client)

   

    #print(json.dumps(response.json(),indent=4))

  
"""
    async def read_stream():
        client = easy_client(
        api_key='EBJQOOZWSLMKMB4ALAXTEDX7AASBDES2@AMER.OAUTHAP',
        redirect_uri='https://localhost',
        token_path='/Users/dakshdagariya/Downloads/djangoreactjsauth1-master/djangoauthapi1/tradingstrategies/td_state.json')

        print(client,"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        stream_client = StreamClient(client)
        await stream_client.login()
        await stream_client.quality_of_service(StreamClient.QOSLevel.EXPRESS)
        def print_message(message):
            print(message)
            current_tick=message
            date_time = datetime.datetime.fromtimestamp(current_tick['content'][0]['CHART_TIME']/1000)  
            counter=1
            key_data = {}
            for item in current_tick['content']:
                key = item['key']
                if key not in key_data:
                    key_data[key] = []
                key_data[key].append(item)
                print(stock_strategy_map,"MMMMMMMMM")
                
                if key in stock_strategy_map:                                 #sending data to individual tasks
                    task = app.tasks[stock_strategy_map[key]]
                    task.apply_async(args=[key_data[key]],queue="{}_queue".format(stock_strategy_map[key]))


      
        # Always add handlers before subscribing because many streams start sending
        # data immediately after success, and messages with no handlers are dropped.
        stream_client.add_chart_equity_handler(print_message)
        await stream_client.chart_equity_subs(stock_list)
        while True:
            await stream_client.handle_message()

    asyncio.run(read_stream())
"""

cache.set('count', 0)
count=0
minutes_processed={}
minute_candlesticks=[]
current_tick=None
open=True
open_price=None
high_price=None
low_price=None
close_price=None
lock = get_redis_connection("default").lock("lock_count")


def getPlaceOrderJSON(*args, **kwargs):
    {
  "orderStrategyType": "TRIGGER",
  "session": "NORMAL",
  "duration": "DAY",
  "orderType": "Market_Order",
  "orderLegCollection": [
    {
      "instruction": "BUY",
      "quantity": 5,
      "instrument": {
        "assetType": "EQUITY",
        "symbol": "XYZ"
      }
    }
  ],
  "childOrderStrategies": [
    {
      "orderStrategyType": "OCO",
      "childOrderStrategies": [
        {
          "orderStrategyType": "SINGLE",
          "session": "NORMAL",
          "duration": "GOOD_TILL_DAY",
          "orderType": "LIMIT",
          "price": 15.27,
          "orderLegCollection": [
            {
              "instruction": "SELL",
              "quantity": 5,
              "instrument": {
                "assetType": "EQUITY",
                "symbol": "XYZ"
              }
            }
          ]
        },
        {
          "orderStrategyType": "SINGLE",
          "session": "NORMAL",
          "duration": "GOOD_TILL_CANCEL",
          "orderType": "STOP",
          "stopPrice": 11.27,
          "orderLegCollection": [
            {
              "instruction": "SELL",
              "quantity": 5,
              "instrument": {
                "assetType": "EQUITY",
                "symbol": "XYZ" 
               }
            }
          ]
        }
      ]
    }
  ]
}


cache.set('activate',False)


@shared_task(name="strategy_1",queue='strategy_1_queue')
def strategy_1(*args, **kwargs):
    strategy=Strategy.objects.filter(name="strategy_1").first()
    stock_symbol=strategy.stock.symbol
    print(stock_symbol,"STOCK_SYMBOl")
    client = easy_client(
            api_key='EBJQOOZWSLMKMB4ALAXTEDX7AASBDES2@AMER.OAUTHAP',
            redirect_uri='https://localhost',
            token_path='/Users/dakshdagariya/Downloads/djangoreactjsauth1-master/djangoauthapi1/tradingstrategies/td_state.json')
    stream_client = StreamClient(client)
    print(client,"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    if strategy.strategy_is_active:
        async def read_stream():
            await stream_client.login()
            await stream_client.quality_of_service(StreamClient.QOSLevel.FAST)
            def print_message(message):
                if message["service"]=="CHART_EQUITY" and cache.get('activate')==False:
                    data=message
                    date_time = datetime.datetime.fromtimestamp(data['content'][0]['CHART_TIME']/1000)

                    # below code for converting 1 minute data to 5 minute data.

                    print(date_time.minute,"MINUTE")
                    global count
                    global open_price
                    global high_price
                    global close_price
                    global low_price
                    if date_time.minute%5==4:    
                        if count==4: 
                            high_price=max(high_price,data['content'][0]['HIGH_PRICE'])
                            low_price=min(low_price,data['content'][0]['LOW_PRICE'])
                            close_price=data['content'][0]['CLOSE_PRICE']
                            print(open_price ,"    ",high_price,"   ",low_price,"   ",close_price,"    THIS IS 5 MINUTE CandleStick ")
                            # strategy logic
                            """if open_price>close_price:    
                                low_price_set=low_price
                                option_quote=getOptionChain(low_price,data['content'][0]['key'])         
                                placeOrderJSON=getPlaceOrderJSON(option_quote,strategy.quantity)
                                trade_replication.apply_async(args=[placeOrderJSON],queue='replication_queue')"""
                            if  open_price>close_price:
                                if lock.acquire(blocking=True):
                                    try:
                                        cache.set('activate',True)
                                    finally:
                                        lock.release()
                           
                                
                            #strategy_1_logic(open_price,high_price,low_price,close_price)
                            # ends

                        if lock.acquire(blocking=True):
                            try:
                                count=0
                            finally:
                                lock.release()
                    else:
                        if count==0:
                            open_price=data['content'][0]['OPEN_PRICE']
                            high_price=data['content'][0]['HIGH_PRICE']
                            low_price=data['content'][0]['LOW_PRICE']
                            if lock.acquire(blocking=True):
                                try:
                                    count=count+1
                                finally:
                                    lock.release()
                            print(count,"CCCCCCCCCCCCC")
                        else:
                            high_price=max(high_price,data['content'][0]['HIGH_PRICE'])
                            low_price=min(low_price,data['content'][0]['LOW_PRICE'])
                            if lock.acquire(blocking=True):
                                try:
                                    count=count+1
                                finally:
                                    lock.release()
                            print(count,"CCCCCCCCCCCCC")

                    print(data,"ASDFGFDSASSDFGFDDSSDASSS")
                elif message["service"]=="QUOTE" and cache.get('activate')==True:
                    print("STRRRRRAAAAATEEEEGY ACTIVVVVVVATTTTTEDDDD")
                    try:
                        if low_price>message["content"]["LAST_PRICE"]:
                            print(message["content"]["LAST_PRICE"])
                            symbol=getOptionSymbol(client,stock_symbol)
                            if lock.acquire(blocking=True):
                                try:
                                    cache.set('activate',False)
                                finally:
                                    lock.release()
                            
                        else:
                            pass      
                    except:
                        pass


            stream_client.add_chart_equity_handler(print_message)
            #stream_client.add_level_one_equity_handler(print_message)
            #await stream_client.level_one_equity_subs(['GOOG'])
            await stream_client.chart_equity_subs([stock_symbol])
            
            while True:
                await stream_client.handle_message()

        asyncio.run(read_stream())
    else:
        print("Strategy_1 is not active")
        pass
            # ends
      
           

@shared_task(name="strategy_2",queue='strategy_2_queue')
def strategy_2():
    client = easy_client(
            api_key='EBJQOOZWSLMKMB4ALAXTEDX7AASBDES2@AMER.OAUTHAP',
            redirect_uri='https://localhost',
            token_path='/Users/dakshdagariya/Downloads/djangoreactjsauth1-master/djangoauthapi1/tradingstrategies/td_state.json')
    stream_client = StreamClient(client)

    async def read_stream():
        await stream_client.login()
        await stream_client.quality_of_service(StreamClient.QOSLevel.FAST)
        
        def print_message(message):
            print(json.dumps(message, indent=4))

        # Always add handlers before subscribing because many streams start sending
        # data immediately after success, and messages with no handlers are dropped.
        stream_client.add_level_one_equity_handler(print_message)
        #stream_client.add_chart_equity_handler(print_message)
        await stream_client.level_one_equity_subs(['GOOG'])
        #await stream_client.chart_equity_subs(['GOOG'])
        while True:
            await stream_client.handle_message()

    asyncio.run(read_stream())
    #trade_replication.apply_async(queue='replication_queue')


async def getOptionSymbol(client,stock_symbol):
    response=client.get_option_chain(stock_symbol,contract_type=client.Options.ContractType.PUT,strike_count=1,strike=None,strike_range=client.Options.StrikeRange.NEAR_THE_MONEY,from_date=datetime.datetime.now().date() + datetime.timedelta(days=7),to_date=datetime.datetime.now().date() + datetime.timedelta(days=14),option_type=client.Options.Type.STANDARD)
    option_data=response.json()
    put_exp_date_map = option_data['putExpDateMap']
    first_date = list(put_exp_date_map.keys())[0]
    first_strike = list(put_exp_date_map[first_date].keys())[0]
    options = put_exp_date_map[first_date][first_strike]
    #symbol = options[0]['symbol']
    return options


@sync_to_async
def get_strategy():
    return Strategy.objects.filter(name="strategy_3").first()

async def placeOrderDataStrategy1(option,df_5min):
    strategy = await get_strategy()
    option_symbol=option[0]['symbol']
    delta=option[0]['delta']
    ltp=option[0]['last']
    candle_size=abs(df_5min.loc[df_5min.index[0],'high']-df_5min.loc[df_5min.index[0],'low'])
    quantity=strategy.quantity 
    if(strategy.max_stop_loss is not None and candle_size>strategy.max_stop_loss):
        option_candle_size=strategy.max_stop_loss*delta      # this is giving us the price change of option quote if price of equity changed 
        stop_price=ltp+option_candle_size
        limit_price=(-1*option_candle_size)*(1/strategy.risk_to_reward_ratio)+ltp
    else:
        option_candle_size=candle_size*delta     # this is giving us the price change of option quote for price change in equity quoute from low to high of the red candle
        stop_price=ltp+option_candle_size
        limit_price=(-1*option_candle_size)*(1/strategy.risk_to_reward_ratio)+ltp 
    limit_price=round(limit_price,2)
    stop_price=round(stop_price,2)
    global place_order_data
    place_order_data={
    "orderStrategyType": "TRIGGER",
    "session": "NORMAL",
    "duration": "DAY",
    "orderType": "MARKET",
    "orderLegCollection": [
        {
        "instruction": "BUY_TO_OPEN",
        "quantity": quantity,
        "instrument": {
            "assetType": "OPTION",
            "symbol": option_symbol
        }
        }
    ],
    "childOrderStrategies": [
        {
        "orderStrategyType": "OCO",
        "childOrderStrategies": [
            {
            "orderStrategyType": "SINGLE",
            "session": "NORMAL",
            "duration": "GOOD_TILL_CANCEL",
            "orderType": "LIMIT",
            "price": limit_price,
            "orderLegCollection": [
                {
                "instruction": "SELL_TO_CLOSE",
                "quantity": quantity,
                "instrument": {
                    "assetType": "OPTION",
                    "symbol": option_symbol
                }
                }
            ]
            },
            {
            "orderStrategyType": "SINGLE",
            "session": "NORMAL",
            "duration": "GOOD_TILL_CANCEL",
            "orderType": "STOP",
            "stopPrice": stop_price,
            "orderLegCollection": [
                {
                "instruction": "SELL_TO_CLOSE",
                "quantity": quantity,
                "instrument": {
                    "assetType": "OPTION",
                    "symbol": option_symbol 
                }
                }
            ]
            }
        ]
        }
    ]
    }
    place_order_data=json.dumps(place_order_data)
    return place_order_data




df = pd.DataFrame(columns=['time', 'open', 'high','low','close'])
df_5min=pd.DataFrame()
df.set_index('time', inplace=True)
max_strategy_run=2
@shared_task(name="strategy_1",queue='strategy_1_queue')
def strategy_1():
    client = easy_client(
            api_key='EBJQOOZWSLMKMB4ALAXTEDX7AASBDES2@AMER.OAUTHAP',
            redirect_uri='https://localhost',
            token_path='/Users/dakshdagariya/Downloads/djangoreactjsauth1-master/djangoauthapi1/tradingstrategies/td_state.json')
    stream_client = StreamClient(client)
    strategy=Strategy.objects.filter(name="strategy_1").first()
    stock_symbol=strategy.stock.symbol
    async def read_stream():
        await stream_client.login()
        await stream_client.quality_of_service(StreamClient.QOSLevel.FAST)
        async def print_message(message):
            global df
            global df_5min
            global max_strategy_run
            global place_order_data
            if message['service']=='CHART_EQUITY':
                if max_strategy_run==0:
                    await stream_client.chart_equity_unsubs([stock_symbol])
                    await stream_client.level_one_equity_unsubs([stock_symbol])
                if df.shape[0]==0 and datetime.datetime.fromtimestamp(message['content'][0]['CHART_TIME']/1000).minute%5!=0:
                    pass
                else:
                    df = df.append({
                    'time': datetime.datetime.fromtimestamp(message['content'][0]['CHART_TIME']/1000),
                    'open': message['content'][0]['OPEN_PRICE'],
                    'high': message['content'][0]['HIGH_PRICE'],
                    'low':  message['content'][0]['LOW_PRICE'],
                    'close': message['content'][0]['CLOSE_PRICE'],
                    },ignore_index=True)

                print(json.dumps(message, indent=4))
                if df.shape[0]==5:
                    df.set_index('time', inplace=True)
                    df = df.resample('5T').agg({'open': 'first', 
                                        'high': 'max', 
                                        'low': 'min', 
                                        'close': 'last'})
                    df_5min=copy.deepcopy(df)
                    print('New DataFrame (5 minute):\n', df_5min)
                    if df_5min.loc[df_5min.index[0],'open']>df_5min.loc[df_5min.index[0],'close']:
                        max_strategy_run=max_strategy_run-1
                        option=await getOptionSymbol(client,message['content'][0]['key'])
                        print(option)
                        place_order_data = await placeOrderDataStrategy1(option,df_5min)
                        print(place_order_data)
                        df.drop(index=df.index, inplace=True)
                        await stream_client.chart_equity_unsubs([stock_symbol])
                        await stream_client.level_one_equity_subs([stock_symbol])
                    else:
                        df.drop(index=df.index, inplace=True)
                
            elif message['service']=='QUOTE':
                print(message)
                if max_strategy_run==0:
                    message['content'][0]['LAST_PRICE']=12345678
                if ((datetime.datetime.now() - df_5min.index[0]).total_seconds() / 60)<20:
                    try:
                        if message['content'][0]['LAST_PRICE']<df_5min.loc[df_5min.index[0],'low']:
                            # here we'll place order
                            max_strategy_run=0
                            trade_replication.apply_async(args=place_order_data)
                            print("ORDER   PLACED  !!!!!!!!!!!>>>>><<<<<<<<")
                            await stream_client.level_one_equity_unsubs([stock_symbol])
                    except KeyError:
                        print('Error: Could not retrieve LAST_PRICE from message')
                else:
                    await stream_client.level_one_equity_unsubs([stock_symbol])
                    
            # Always add handlers before subscribing because many streams start sending
            # data immediately after success, and messages with no handlers are dropped.
        stream_client.add_chart_equity_handler(print_message)
        stream_client.add_level_one_equity_handler(print_message)
        await stream_client.chart_equity_subs([stock_symbol])
        while True:
            await stream_client.handle_message()
    asyncio.run(read_stream())


