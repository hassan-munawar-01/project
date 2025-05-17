from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

class SmartChatBot:
    def __init__(self):
        # ✅ Correct GitHub AI inference endpoint
        self.client = ChatCompletionsClient(
            endpoint="https://models.github.ai/inference",
            credential=AzureKeyCredential("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")  # ✅ GitHub token(abubakar)
            # credential=AzureKeyCredential("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")  # ✅ GitHub token(hassan)
        )
        self.model = "openai/gpt-4.1"  # ✅ Fully qualified model name required

    def get_response(self, user_input, lang):
        # Initial assistant prompt  
        base_prompt = [
            SystemMessage("You are a smart multilingual assistant."),
            UserMessage(user_input)
        ]

        try:
            # Step 1: Get response
            completion = self.client.complete(
                messages=base_prompt,
                temperature=0.7,
                top_p=1.0,
                model=self.model
            )
            original_response = completion.choices[0].message.content

            # Step 2: Translate if needed
            if lang == 'ur':
                translate_prompt = f"Translate this into Urdu: {original_response}"
            elif lang == 'rp':
                translate_prompt = f"Translate this into Roman Punjabi: {original_response}"
            else:
                return original_response

            translation = self.client.complete(
                messages=[
                    SystemMessage("You are a helpful translator."),
                    UserMessage(translate_prompt)
                ],
                temperature=0.7,
                top_p=1.0,
                model=self.model
            )

            return translation.choices[0].message.content

        except Exception as e:
            return f"👳‍♂️ sardaar: Error occurred: {str(e)}"
