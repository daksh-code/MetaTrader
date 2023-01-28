from __future__ import absolute_import,unicode_literals
from email import header
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



@shared_task(bind=True)
def trading_strategy1(*args, **kwargs):

    client = easy_client(
            api_key='EBJQOOZWSLMKMB4ALAXTEDX7AASBDES2@AMER.OAUTHAP',
            redirect_uri='https://localhost',
            token_path='/Users/dakshdagariya/Downloads/djangoreactjsauth1-master/djangoauthapi1/tradingstrategies/td_state.json')

    print(client,"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    stream_client = StreamClient(client)

    minutes_processed={}
    minute_candlesticks=[]
    current_tick=None
    open=True
    open_price=None
    high_price=None
    low_price=None
    close_price=None


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
            

            if current_tick['content'][0]['OPEN_PRICE']>current_tick['content'][0]['CLOSE_PRICE']:
                trade_replication.apply_async()
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

                if(open_price>close_price):
                    pass           #strategy logic in this function


                open_price=close_price
                high_price=open_price
                low_price=open_price

        # Always add handlers before subscribing because many streams start sending
        # data immediately after success, and messages with no handlers are dropped.
        stream_client.add_chart_equity_handler(print_message)
        await stream_client.chart_equity_subs(['AAPL'])
        while True:
            await stream_client.handle_message()

    asyncio.run(read_stream())