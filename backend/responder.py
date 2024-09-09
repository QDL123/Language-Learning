import json
from llm_client import LlmClient
from agent import Agent
from tutor import Tutor

class Responder:
    def __init__(self):
        self.client = LlmClient()
        self.tutorMode = False
        self.agent = Agent()
        with open('prompts.json') as f:
            prompts = json.load(f)
            self.checkModePrompt = prompts['checkMode']
            self.tutor = Tutor(prompts['tutor'])

    def draft_begin_message(self):
        # Maybe we want to start message introducing the tutor as well?
        return self.agent.draft_begin_message()
    
    def respond(self, request):
        # Determine if the tutor or agent should respond and return the corresponding generator to
        # to stream back the output

        if self.tutorMode:
            # Check if we should exit tutor mode
            return self.tutor.respond(request)
        
        # Start getting the agent response
        agentResponse = self.agent.respond(request)

        # Check if we should enter tutor mode
        prompt = [{
            "role": "system",
            "content": self.checkModePrompt,
        }]

        # Roll up transcript into a single message
        transcript_content = ''
        for utterance in request['transcript']:
            if utterance['role'] == 'system':
                continue
            role = 'spanish speaker' if utterance['role'] == 'agent' else 'spanish learner'
            transcript_content += role + ": " + utterance['content'] + '\n'

        prompt.append({
            "role": "user",
            "content": transcript_content,
        })
        
        # TODO: Need to have a callback read this and issue an interrupt to Retell if the tutor is activated
        res = self.client.get_response(prompt)
        res_json = json.loads(res)
        if res_json["activate_tutor"]:
            print("Activating tutor mode")
            self.tutorMode = True
            return self.tutor.respond(request)
        
        # tutor mode is not needed, return the agent response generator
        return agentResponse

        