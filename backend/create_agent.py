import requests
from dotenv import load_dotenv
import os

def main():
    print('Creating agent')

    load_dotenv(dotenv_path='.env.local')
    url = "https://api.retellai.com/create-agent"

    body = {
        'llm_websocket_url': os.environ['LLM_WEBSOCKET_URL'],
        'agent_name': 'Alejandro',
        'voice_id': 'openai-Echo',
        'ambient_sound': 'coffee-shop',
        'language': 'es-ES',
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ['RETELL_API_KEY'],
    }

    response = requests.post(url, json=body, headers=headers)

    # Checking if the request was successful
    if response.status_code == 200 or response.status_code == 201:
        # Parsing the response JSON if the request was successful
        print('Successfully created agent!')
        data = response.json()
        print(data)
    else:
        print("Failed to create agent", response.status_code)



if __name__ == "__main__":
    main()