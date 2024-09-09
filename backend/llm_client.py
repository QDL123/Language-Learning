from openai import OpenAI
import os

class LlmClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ['OPENAI_API_KEY'],
        )

    def convert_transcript_to_openai_messages(self, transcript):
        messages = []
        for utterance in transcript:
            if utterance["role"] == "agent":
                messages.append({
                    "role": "assistant",
                    "content": utterance['content']
                })
            else:
                messages.append({
                    "role": "user",
                    "content": utterance['content']
                })
        return messages

    def get_response(self, prompt):
        stream = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=prompt,
            stream=False,
            response_format={"type": "json_object"}
        )

        return stream.choices[0].message.content
    

    def stream_response(self, prompt, response_id):
        for utterance in prompt:
            if utterance['role'] == 'system':
                continue
            print(utterance)
        print('\n')

        stream = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=prompt,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield {
                    "response_id": response_id,
                    "content": chunk.choices[0].delta.content,
                    "content_complete": False,
                    "end_call": False,
                }
        
        yield {
            "response_id": response_id,
            "content": "",
            "content_complete": True,
            "end_call": False,
        }