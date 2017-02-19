# coding:utf-8
"""
Created on Thu Feb 16 12:09:59 2017
@author: kishiyama
"""

import time
from datetime import datetime
from slackclient import SlackClient

from bot_auth import get_auth

#auth情報の読み取り
id_token = get_auth()
BOT_ID = id_token['BOT_ID']
SLACK_BOT_TOKEN = id_token['SLACK_BOT_TOKEN']

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "こんにちは"

# instantiate Slack & Twilio clients
slack_client = SlackClient(SLACK_BOT_TOKEN)

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = greeting()
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

def greeting():
  h = int(datetime.now().strftime("%H"))
  s1 = ""
  date = datetime.now().strftime("%Y/%m/%d")
  time = datetime.now().strftime("%H:%M:%S")
  if h > 17 or h < 2:
    s1 = "こんばんは \n"
  elif h < 11:
    s1 = "おはようございます \n"
  else:
    s1 = "こんにちは \n"
  tmp = "{0}今日は{1}\n時刻は{2}ですね :)".format(s1, date, time)
  return tmp

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
