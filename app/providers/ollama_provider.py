import asyncio
class OllamaProvider:
    def __init__(self):
        pass

    async def query_text_file(self, text):
        # Create the subprocess to run Ollama
        process = await asyncio.create_subprocess_exec(
            "ollama", "run", "llama3.2",
            stdin=asyncio.subprocess.PIPE,  # Send the prompt as input
            stdout=asyncio.subprocess.PIPE,  # Capture the output
            stderr=asyncio.subprocess.PIPE   # Capture any errors
        )
        stdout, stderr = await process.communicate(input=text.encode())
        if stderr:
            raise Exception(f"Ollama error: {stderr.decode()}")
        output_text = stdout.decode().strip()
        return output_text