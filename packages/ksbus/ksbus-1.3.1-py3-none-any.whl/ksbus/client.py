"""
This module implements a ksbus client https://github.com/kamalshkeir/ksbus

Author: Kamal Shkeir
Email: kamalshkeir@gmail.com
Link: https://kamalshkeir.dev
"""

import asyncio
import json
import random
import string

import websockets


class Bus:
    def __init__(self, options, block=False):
        self.Address = options.get('Address', 'localhost')
        self.Path = options.get('Path', '/ws/bus')
        self.scheme = 'ws://'
        if options.get('Secure', False):
            self.scheme = 'wss://'
        self.full_address = self.scheme + self.Address + self.Path
        self.conn = None
        self.topic_handlers = {}
        self.AutoRestart = options.get('AutoRestart', False)
        self.RestartEvery = options.get('RestartEvery', 5)
        self.OnOpen = options.get('OnOpen', lambda bus: None)
        self.OnClose = options.get('OnClose', lambda: None)
        self.OnDataWs = options.get('OnDataWs', None)
        self.OnId = options.get('OnId', lambda data: None)
        self.Id = options.get('Id') or self.makeId(12)
        try:
            if block :
                asyncio.get_event_loop().run_until_complete(self.connect(self.full_address))
            else:
                asyncio.create_task(self.connect(self.full_address))
        except Exception as e:
            print(e)
    
    async def connect(self, path):
        try:
            self.conn = await websockets.connect(path)
            await self.sendMessage({"action": "ping", "from": self.Id})
            async for message in self.conn:
                obj = json.loads(message)
                if self.OnDataWs is not None:
                    self.OnDataWs(obj,self.conn)
                if "event_id" in obj:
                    self.Publish(obj["event_id"], {"ok": "done", "from": self.Id, "event_id":obj["event_id"]})
                if "to_id" in obj and obj["to_id"] == self.Id:
                    if self.OnId is not None:
                        self.OnId(obj)
                elif "topic" in obj:
                    if obj["topic"] in self.topic_handlers:
                        subs = BusSubscription(self, obj["topic"])
                        self.topic_handlers[obj["topic"]](obj, subs)
                elif "data" in obj and obj["data"] == "pong":
                    if self.OnOpen is not None:
                        self.OnOpen(self)
        except Exception as e:
            print(f"Server closed the connection: {e}")
            if self.OnClose:
                self.OnClose()
            if self.AutoRestart:
                while True:
                    print(f"Reconnecting in {self.RestartEvery} seconds...")
                    await asyncio.sleep(self.RestartEvery)
                    await self.connect(self.full_address)

    def Subscribe(self, topic, handler):
        payload = {"action": "sub", "topic": topic, "from": self.Id}
        subs = BusSubscription(self, topic)
        self.topic_handlers[topic] = handler
            
        if self.conn is not None:
            asyncio.create_task(self.sendMessage(payload))
        return subs

    def Unsubscribe(self, topic):
        payload = {"action": "unsub", "topic": topic, "from": self.Id}
        del self.topic_handlers[topic]
            
        if topic and self.conn is not None:
            asyncio.create_task(self.sendMessage(payload))

    async def sendMessage(self, obj):
        try:
            await self.conn.send(json.dumps(obj))
        except Exception as e:
            print("error sending message:", e)

    def Publish(self, topic, data):
        if self.conn is not None:
            asyncio.create_task(self.sendMessage({"action": "pub", "topic": topic, "data": data, "from": self.Id}))
        else:
            print("Publish: Not connected to server. Please check the connection.")

    def PublishToID(self, id, data):
        if self.conn is not None:
            asyncio.create_task(self.sendMessage({"action": "pub_id", "id": id, "data": data, "from": self.Id}))
        else:
            print("PublishToID: Not connected to server. Please check the connection.")

    def RemoveTopic(self, topic):
        if self.conn is not None:
            asyncio.create_task(self.sendMessage({"action": "remove", "topic": topic, "from": self.Id}))
            del self.topic_handlers[topic]

    def makeId(self, length):
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    def PublishWaitRecv(self, topic, data, onRecv, onExpire):
        data["from"] = self.Id
        data["topic"] = topic
        eventId = self.makeId(8)
        data["event_id"] = eventId
        done = False

        def _onRecv(data, ch):
            nonlocal done
            if not done:
                done = True
                if onRecv:
                    onRecv(data)
                ch.Unsubscribe()

        sub = self.Subscribe(eventId, lambda data, ch: _onRecv(data, ch))
        
        async def expireTimer(eventId):
            await asyncio.sleep(0.5)  # Adjust the timeout as needed
            if not done:
                if onExpire:
                    onExpire(eventId, topic)
                sub.Unsubscribe()
        
        self.Publish(topic, data)
        asyncio.create_task(expireTimer(eventId))


    def PublishToIDWaitRecv(self, id, data, onRecv, onExpire):
        data["from"] = self.Id
        data["id"] = id
        eventId = self.makeId(8)
        data["event_id"] = eventId
        done = False

        def _onRecv(data, ch):
            nonlocal done
            if not done:
                done = True
                if onRecv:
                    onRecv(data)
                ch.Unsubscribe()

        sub = self.Subscribe(eventId, lambda data, ch: _onRecv(data, ch))

        async def expireTimer(eventId):
            await asyncio.sleep(0.5)  # Adjust the timeout as needed
            if not done:
                if onExpire:
                    onExpire(eventId,id)
                sub.Unsubscribe()

        
        self.PublishToID(id, data)
        asyncio.create_task(expireTimer(eventId))

    def PublishToServer(self, addr, data, secure):
        self.conn.send(json.dumps({
            "action": "pub_server",
            "addr": addr,
            "data": data,
            "secure": secure,
            "from": self.Id
        }))


class BusSubscription:
    def __init__(self, bus, topic):
        self.bus = bus
        self.topic = topic

    async def sendMessage(self, obj):
        try:
            await self.bus.conn.send(json.dumps(obj))
        except Exception as e:
            print("error sending message:", e)

    def Unsubscribe(self):
        asyncio.create_task(self.sendMessage({"action": "unsub", "topic": self.topic, "from": self.bus.Id}))
        del self.bus.topic_handlers[self.topic]

