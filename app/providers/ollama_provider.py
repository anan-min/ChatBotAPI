import subprocess

class OllamaProvider:
    def __init__(self):
        pass

    async def query_text_file(self, text):
        """Query Ollama via subprocess and print input, output, and errors."""
        try:
            # Start the subprocess and send the input text
            process = subprocess.Popen(
                ["ollama", "run", "llama3.2"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,  # Treat input/output as text
                encoding="utf-8",  # Ensure UTF-8 encoding
                errors="replace"  # Replace decoding errors with '?'
            )

            # Communicate with the subprocess
            stdout, stderr = process.communicate(input=text)

            # Check for process return code
            if process.returncode != 0:
                raise subprocess.CalledProcessError(
                    process.returncode, process.args, output=stdout, stderr=stderr
                )
            cleaned_output = " ".join(stdout.strip().split())
            return cleaned_output

        except subprocess.CalledProcessError as e:
            print(f"Command failed with error:\n{e.stderr}")
            return ""

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return ""
