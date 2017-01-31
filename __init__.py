import logging
import aiohttp
import asyncio

from opsdroid.connector import Connector
from opsdroid.message import Message


class ConnectorTelegram(Connector):

    def __init__(self, config):
        """Setup the connector."""
        logging.debug("Loaded telegram connector")
        super().__init__(config)
        self.name = "telegram"
        self.token = config["token"]
        self.latest_update = None

    def build_url(self, method):
        return "https://api.telegram.org/bot{}/{}".format(self.token, method)

    async def connect(self, opsdroid):
        """Connect to telegram."""
        logging.debug("Connecting to telegram")
        async with aiohttp.ClientSession() as session:
            async with session.get(self.build_url("getMe")) as resp:
                json = await resp.json()
                logging.debug("Connected to telegram as %s",
                              json["result"]["username"])

    async def listen(self, opsdroid):
        """Listen for new message."""
        while True:
            async with aiohttp.ClientSession() as session:
                data = {}
                if self.latest_update is not None:
                    data["offset"] = self.latest_update
                async with session.post(self.build_url("getUpdates"),
                                        data=data) as resp:
                    if resp.status != 200:
                        logging.error("Telegram error %s, %s",
                                      resp.status, resp.text())
                    else:
                        json = await resp.json()
                        if len(json["result"]) > 0:
                            logging.debug("Received %i messages from telegram",
                                          len(json["result"]))
                        for response in json["result"]:
                            logging.debug(response)
                            if self.latest_update is None or \
                                    self.latest_update <= response["update_id"]:
                                self.latest_update = response["update_id"] + 1
                            if "text" in response["message"]:
                                message = Message(response["message"]["text"],
                                                  response["message"]["from"]["username"],
                                                  response["message"]["chat"],
                                                  self)
                                await opsdroid.parse(message)

                    await asyncio.sleep(0.5)


    async def respond(self, message):
        """Respond with a message."""
        logging.debug("Responding with: " + message.text)
        async with aiohttp.ClientSession() as session:
            data = {}
            data["chat_id"] = message.room["id"]
            data["text"] = message.text
            async with session.post(self.build_url("sendMessage"),
                                    data=data) as resp:
                if resp.status == 200:
                    logging.debug("Successfully responded")
