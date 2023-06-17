import requests
from dotenv import load_dotenv
import os
import requests

load_dotenv()
wip_url = os.getenv('WIP_URL')

def wip_api_post(display_name, user_id, conversatio_id, thread_id, message_id, timestamp, message):
    try:
      msg = {"display_name": display_name, "user_id": user_id, "conversation_id": conversatio_id, "thread_id": thread_id, "message_id": message_id, "timestamp": timestamp, "message": message}
      resp = requests.post(wip_url, json=msg)
        
    except requests.exceptions.RequestException as e:
       print("WIP_API_POST=ERROR: ", e)
    else:
       print("WIP_API_POST=OK")
    finally:
       print("WIP_API_POST=END")
