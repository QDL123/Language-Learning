import json
import os
import asyncio
from responder import Responder
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()
load_dotenv(dotenv_path='.env.local')

# Old way of handling websocket connections
@app.websocket("/llm-websocket/{call_id}")
async def websocket_handler(websocket: WebSocket, call_id: str):
    await websocket.accept()
    print(f"Handle llm ws for: {call_id}")

    # llm_client = LlmClient()
    responder = Responder()

    # Send the first message, and then listen before generating future responses
    response_id = 0
    first_event = responder.draft_begin_message()
    await websocket.send_text(json.dumps(first_event))

    async def stream_response(request):
        nonlocal response_id
        for event in responder.respond(request):
        # for event in llm_client.draft_response(request):
            await websocket.send_text(json.dumps(event))
            if request['response_id'] < response_id:
                return # new response needed, abondon this one
            
    # listen for new updates
    try:
        while True:
            message = await websocket.receive_text()
            request = json.loads(message)

            # print out transcript
            os.system('cls' if os.name == 'nt' else 'clear')
            for utterance in request['transcript']:
                print(utterance['content'])

            if 'response_id' not in request:
                continue # no response needed
            response_id = request['response_id']
            asyncio.create_task(stream_response(request))
    except WebSocketDisconnect:
        print('Websocket exception')
        print(f"LLM WebSocket disconnected for {call_id}")
    except Exception as e:
        print(f'LLM WebSocket error for {call_id}: {e}')
    finally:
        print(f"LLM WebSocket connection closed for {call_id}")