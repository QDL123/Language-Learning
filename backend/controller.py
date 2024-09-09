import json
import os
import asyncio
from responder import Responder
from dotenv import load_dotenv
from retell import AsyncRetell
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware  # TODO: remove.

load_dotenv(dotenv_path='.env.local')

ORIGINS = [
    "http://localhost:3000",  # local client.
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = AsyncRetell(api_key=os.environ['RETELL_API_KEY'])

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


@app.post("/debug/start-call")
async def start_call():
    print("Starting call...")
    call = await client.call.create_web_call(
        agent_id="agent_45b928a513a87da3a0927ba694"
    )

    return JSONResponse(content={'access_token': call.access_token},
                        status_code=200)
