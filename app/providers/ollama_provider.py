import ollama
import asyncio


class OllamaProvider:
    def __init__(self):
        pass

    async def query_qwen25(self, text):
        """Query Qwen2.5-VL model and return text response"""
        try:
            # Create the prompt with SCG context
            prompt_data = await self.update_prompt(text)

            # Query the model
            response = ollama.chat(
                model='qwen2.5vl:latest',
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
            return f"Error querying Qwen2.5-VL: {str(e)}"

    async def query_llama32(self, text):
        """Query Llama3.2 model and return text response"""
        try:
            # Create the prompt with SCG context
            prompt_data = await self.update_prompt(text)

            # Query the model
            response = ollama.chat(
                model='scb10x/llama3.1-typhoon2-8b-instruct:latest',
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
            return f"Error querying scb10x/llama3.1-typhoon2-8b-instruct:latest: {str(e)}"

    async def update_prompt(self, text):
        """Update prompt with SCG context"""
        content = f"User question: {text}"
        role = "You are an SCG chatbot that helps answer questions about SCG-related topics. SCG = Siam Cement Group Co., Ltd. Provide helpful and accurate information about the company, its products, services, and operations."
        return {"content": content, "role": role}
