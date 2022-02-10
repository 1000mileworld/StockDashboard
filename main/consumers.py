from channels.generic.websocket import AsyncWebsocketConsumer
from asyncio import sleep
import json
from random import randint
from stocks import alpaca, func, tweet

class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'stock_data'
        
        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket (JS frontend)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data_mode = text_data_json['data_mode']
        stock_select = text_data_json['stock_select']

        #market_open = alpaca.isOpen()

        # Send message to group
        if data_mode=='realTime':
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'realTime',
                    'data_mode': data_mode,
                    'stock_select': stock_select,
                }
            )
        else:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'historical',
                    'data_mode': data_mode,
                    'stock_select': stock_select,
                }
            )
    
    # Receive message from group
    async def historical(self, event):
        data_mode = event['data_mode']
        stock_select = event['stock_select']
        x_val, y_val = func.getHistorical(stock_select,data_mode)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'data_mode': data_mode,
            'stock_select': stock_select,
            'x_val': x_val,
            'y_val': y_val,
        }))
    
    async def realTime(self, event):
        data_mode = event['data_mode']
        stock_select = event['stock_select']
        # for i in range(15):
        #     await self.send(json.dumps({
        #         'data_mode': data_mode,
        #         'stock_select': stock_select,
        #         'bid': randint(150,160),
        #         'ask': randint(160,170),
        #         }))
        #     await sleep(1)

        while alpaca.isOpen():
            quote = alpaca.getQuote(stock_select)
            await self.send(json.dumps({
                'data_mode': data_mode,
                'stock_select': stock_select,
                'bid': round(quote.bidprice,2),
                'ask': round(quote.askprice,2),
                }))
            await sleep(1)

        while not alpaca.isOpen():
            close = alpaca.getLastClose(stock_select)
            await self.send(json.dumps({
                'data_mode': data_mode,
                'stock_select': stock_select,
                'close': round(close,2),
                }))
            await sleep(1)

class TweetConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'tweet_data'
        
        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket (JS frontend)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        stock_select = text_data_json['stock_select']
        tweet_count = text_data_json['tweet_count']

        # Send message to group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'tweet',
                'stock_select': stock_select,
                'tweet_count': tweet_count,
            }
        )
    
    # Receive message from group
    async def tweet(self, event):
        stock_select = event['stock_select']
        tweet_count  = event['tweet_count']
        ids = tweet.getTweetID(stock_select,int(tweet_count))
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'ids': ids,
        }))