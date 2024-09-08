import json
import os
import asyncio
from response_system import LlmClient
from pydantic import BaseModel
from dotenv import load_dotenv
from retell import AsyncRetell
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

app = FastAPI()
load_dotenv(dotenv_path='.env.local')
client = AsyncRetell(
    api_key=os.environ['RETELL_API_KEY'],
)

# Define a Pydantic model that represents the expected structure of your request body.
class Register_Params(BaseModel):
    agent_id: str
    description: str = None
    price: float
    tax: float = None


@app.websocket("/llm-websocket/{call_id}")
async def websocket_handler(websocket: WebSocket, call_id: str):
    await websocket.accept()
    # A unique call id is the identifier of each call
    print(f"Handle llm ws for: {call_id}")

    llm_client = LlmClient()

    # Send the first message, and then listen before generating future responses
    response_id = 0
    first_event = llm_client.draft_begin_message()
    await websocket.send_text(json.dumps(first_event))

    async def stream_response(request):
        nonlocal response_id
        for event in llm_client.draft_response(request):
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


@app.post("/register-call")
async def register_call(params: Register_Params):
    print("Registering call!")
    # Register the call with Retell AI
    call = await client.call.register(
        agent_id=params.agent_id,
        audio_encoding="s16le",
        audio_websocket_protocol="web",
        sample_rate=24000,
    )

    return JSONResponse(content={ 'call_id': call.call_id }, status_code=200)
