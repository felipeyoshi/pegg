import openai

class LLM:

    def __init__(self, api_key):
        self.api_key  = api_key
        
    def get_prompt(self, agent, context):
        messages = [{"role": "system",
                      "content": f'''{agent}'''},
                      {"role": "user", "content": f'''{context}'''}]

        return messages

    def get_completion(self, messages):
        openai.api_key = self.api_key
        print("Asking OpenAI...")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=3200,
            n=1,
            stop="###",
            temperature=0.7)
        print("OpenAI answered!")
        return response['choices'][0]['message']['content']