from __future__ import absolute_import,unicode_literals
from email import header
import queue
from symtable import Symbol
from wsgiref import headers
from celery import shared_task
from fileinput import close
from tkinter.filedialog import Open
from trade_replicator.tasks import trade_replication
from tda.auth import easy_client
from tda.client import Client
from tda.streaming import StreamClient
import ssl
import datetime
ssl._create_default_https_context = ssl._create_unverified_context
import asyncio
from .models import Stock, Strategy
from django.forms.models import model_to_dict
from asgiref.sync import sync_to_async
from djangoauthapi1.celery import app

stock_strategy_map = {}
@shared_task(bind=True,queue="streaming_queue")
def data_streaming(*args, **kwargs):
    stocks=Stock.objects.filter(stock_is_active=True)  
    strategies = Strategy.objects.filter(strategy_is_active=True).values('stock__symbol', 'name')
    global stock_strategy_map 
    for strategy in strategies:
        stock_symbol = strategy['stock__symbol']
        strategy_name = strategy['name']
        stock_strategy_map[stock_symbol] = strategy_name
 
    print(strategies,"QQQQQQQQQQQQQQQQ")
    stock_list=[]
    for stock in stocks:
        stock_list.append(stock.symbol)

    client = easy_client(
            api_key='EBJQOOZWSLMKMB4ALAXTEDX7AASBDES2@AMER.OAUTHAP',
            redirect_uri='https://localhost',
            token_path='/Users/dakshdagariya/Downloads/djangoreactjsauth1-master/djangoauthapi1/tradingstrategies/td_state.json')

    print(client,"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    stream_client = StreamClient(client)

   

    response=client.get_option_chain('SPY',contract_type=client.Options.ContractType.PUT,strike_count=1,strike=141.11,strike_range=client.Options.StrikeRange.NEAR_THE_MONEY)
    #print(json.dumps(response.json(),indent=4))

    def getOptionChain(*args):
        pass

    async def read_stream():
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


            """
            global open
            global open_price
            global high_price
            global low_price
            global close_price
            if open:                                                     # initialiazing variables when the code starts runnning only runs once
                print("YOOO")
                open_price=current_tick['content'][0]['OPEN_PRICE']
                high_price=current_tick['content'][0]['HIGH_PRICE']
                low_price=current_tick['content'][0]['LOW_PRICE']
                close_price=current_tick['content'][0]['CLOSE_PRICE']
                open=False
            
            high_price=max(high_price,current_tick['content'][0]['HIGH_PRICE'])
            low_price=min(low_price,current_tick['content'][0]['LOW_PRICE'])

            if(date_time.minute%5==0):
                close_price=current_tick['content'][0]['CLOSE_PRICE']
                print(date_time.minute,"a")

                print(open_price ,"    ",high_price,"   ",low_price,"   ",close_price,"    THIS IS 5 MINUTE CandleStick ")
                
                open_price=close_price
                high_price=open_price
                low_price=open_price
        """
        # Always add handlers before subscribing because many streams start sending
        # data immediately after success, and messages with no handlers are dropped.
        stream_client.add_chart_equity_handler(print_message)
        await stream_client.chart_equity_subs(stock_list)
        while True:
            await stream_client.handle_message()

    asyncio.run(read_stream())

count=0
minutes_processed={}
minute_candlesticks=[]
current_tick=None
open=True
open_price=None
high_price=-1
low_price=1000000
close_price=None
@shared_task(name="strategy_1",queue='strategy_1_queue')
def strategy_1(data):
    date_time = datetime.datetime.fromtimestamp(data[0]['CHART_TIME']/1000)
    global count
    global open_price
    global high_price
    global close_price
    global low_price
    if date_time.minute%5==4:
        if count==4:
            count=0
            high_price=max(high_price,data[0]['HIGH_PRICE'])
            low_price=min(low_price,data[0]['LOW_PRICE'])
            close_price=data[0]['CLOSE_PRICE']
            print(open_price ,"    ",high_price,"   ",low_price,"   ",close_price,"    THIS IS 5 MINUTE CandleStick ")
            open_price=data[0]['CLOSE_PRICE']
            low_price=open_price
            high_price=open_price
        else:
            count=0
            open_price=data[0]['OPEN_PRICE']
            low_price=data[0]['OPEN_PRICE']
            high_price=data[0]['OPEN_PRICE']
    else:
        high_price=max(high_price,data[0]['HIGH_PRICE'])
        low_price=min(low_price,data[0]['LOW_PRICE'])
        count=count+1

    print(data,"ASDFGFDSASSDFGFDDSSDASSS")
    trade_replication.apply_async(queue='replication_queue')

@shared_task(name="strategy_2",queue='strategy_2_queue')
def strategy_2(data):
    print(data,"ASDFGFDSASSDFGFDDSSDASSS")
    trade_replication.apply_async(queue='replication_queue')


