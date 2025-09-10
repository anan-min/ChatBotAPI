import ollama
import asyncio
import os 


class OllamaProvider:
    def __init__(self):
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

    async def query_qwen25(self, text):
        """Query Qwen2.5-VL model and return text response"""
        try:
            # Create the prompt with SCG context
            prompt_data = await self.update_prompt(text)

            # Query the model
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': prompt_data['role']
                    },
                    {
                        'role': 'user',
                        'content': text
                    }
                ]
            )

            return response['message']['content']

        except Exception as e:
            return f"Error querying {self.model}: {str(e)}"

    async def query_llama32(self, text):
        """Query Llama3.2 model and return text response"""
        try:
            # Create the prompt with SCG context
            prompt_data = await self.update_prompt(text)

            # Query the model
            response = ollama.chat(
                model='llama3.2:latest',
                messages=[
                    {
                        'role': 'system',
                        'content': prompt_data['role']
                    },
                    {
                        'role': 'user',
                        'content': text
                    }
                ]
            )

            return response['message']['content']

        except Exception as e:
            return f"Error querying llama3.2:latest: {str(e)}"

    async def update_prompt(self, text):
        """Update prompt with SCG context"""
        content = f"User question: {text}"
        role = "You are an SCG chatbot that helps answer questions about SCG-related topics. SCG = Siam Cement Group Co., Ltd. Provide helpful and accurate information about the company, its products, services, and operations."
        return {"content": content, "role": role}
