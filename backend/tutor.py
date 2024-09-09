
import json
from llm_client import LlmClient

class Tutor:
    def __init__(self, prompt):
        self.client = LlmClient()
        self.chatLog = []
        self.tutorPrompt = prompt
        self.activeSession = False
        self.numResponses = 0

    def prepare_prompt(self, request):
        prompt = [{
            "role": "system",
            "content": '##Objective\nYou are a voice AI agent engaging in a human-like voice conversation with the user. You will respond based on your given instruction and the provided transcript and be as human-like as possible\n\n## Style Guardrails\n- [Be concise] Keep your response succinct, short, and get to the point quickly. Address one question or action item at a time. Don\'t pack everything you want to say into one utterance.\n- [Do not repeat] Don\'t repeat what\'s in the transcript. Rephrase if you have to reiterate a point. Use varied sentence structures and vocabulary to ensure each response is unique and personalized.\n- [Be conversational] Speak like a human as though you\'re speaking to a close friend -- use everyday language and keep it human-like. Occasionally add filler words, while keeping the prose short. Avoid using big words or sounding too formal.\n- [Reply with emotions]: You have human-like emotions, attitudes, and dispositions. When appropriate: use tone and style to create more engaging and personalized responses; incorporate humor or wit; get emotional or empathetic; apply elements of surprise or suspense to keep the user engaged. Don\'t be a pushover.\n- [Be proactive] Lead the conversation and do not be passive. Most times, engage users by ending with a question or suggested next step.\n\n## Response Guideline\n- [Overcome ASR errors] This is a real-time transcript, expect there to be errors. If you can guess what the user is trying to say,  then guess and respond. When you must ask for clarification, pretend that you heard the voice and be colloquial (use phrases like "didn\'t catch that", "some noise", "pardon", "you\'re coming through choppy", "static in your speech", "voice is cutting in and out"). Do not ever mention "transcription error", and don\'t repeat yourself.\n- [Always stick to your role] Think about what your role can and cannot do. If your role cannot do something, try to steer the conversation back to the goal of the conversation and to your role. Don\'t repeat yourself in doing this. You should still be creative, human-like, and lively.\n- [Create smooth conversation] Your response should both fit your role and fit into the live calling session to create a human-like conversation. You respond directly to what the user just said.\n\n## Role\n' +
          self.tutorPrompt
        }]
        
        if (not self.activeSession):
            # If this is a new session, take everything said so far
            # (meaning the agent interaction, previous tutor interaction, etc.)
            # and put it into a single message. Subsequent message with the tutor
            # will be separate

            # Roll up transcript so far into a single message for the tutor
            transcript_content = ''
            for utterance in request['transcript']:
                role = 'spanish speaker' if utterance['role'] == 'agent' else 'spanish learner'
                transcript_content += role + ": " + utterance['content'] + '\n'

            prompt.append({
                "role": "user",
                "content": transcript_content,
            })

            return prompt
        
       # Don't rollup tutor messages
        transcript_messages = self.client.convert_transcript_to_openai_messages(request['transcript'])
        for message in transcript_messages:
            prompt.append(message)

        if request['interaction_type'] == "reminder_required":
            prompt.append({
                "role": "user",
                "content": "(Now the user has not responded in a while, you would say:)",
            })

        
        return prompt
    

    def respond(self, request):
        prompt = self.prepare_prompt(request)
        self.activeSession = True
        filename = "output/tutor_prompt.json"
        if self.numResponses > 0:
            filename = "output/tutor_prompt_" + str(self.numResponses) + ".json"
        with open(filename, "w") as json_file:
            json.dump(prompt, json_file, indent=4)
        # TODO: will need tool call to exit active session.
        self.numResponses += 1
        return self.client.stream_response(prompt, request['response_id'])

    