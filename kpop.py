import requests
import json
import time
from urlconfig import *
# Set the Webhook Url as 'webhookUrl' in urlconfig.py 

redditUrl = "https://reddit.com/r/kpop/search.json?q=flair:mv&sort=new"

username = "Kpop News"

def main():
  r = requests.get(redditUrl,headers={'User-agent': 'Kpop-bot'})

  posts = r.json()["data"]["children"]

  lastHour = []
  for post in posts:
    if time.time() - post["data"]["created_utc"] < 600:
      lastHour.append(post)

  for post in lastHour:
    print(post["data"]["title"])
    sendWebhook(post["data"]["url_overridden_by_dest"])


def sendWebhook(msg):
  data = {}
  data["content"] = msg
  data["username"] = username

  result = requests.post(webhookUrl,data=json.dumps(data),headers={"Content-Type": "application/json"})

  try:
    result.raise_for_status()
  except requests.exceptions.HTTPError as err:
    print(err)
  else:
    print("Payload delivered successfully, code {}".format(result.status_code))

if __name__ == "__main__":
  main()