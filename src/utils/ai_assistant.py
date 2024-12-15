import requests

from .logger import logger


class AiAssistant:
    def __init__(self, endpoint_url: str, api_key: str, model: str):
        """
        Initialize the AI assistant with the endpoint URL, API key, and model name.
        Note: This class is a wrapper around the OpenAI API, any AI assistant compatible with the OpenAI API can be used.

        :param endpoint_url:
        :param api_key:
        :param model:
        """
        self.endpoint_url = endpoint_url
        self.api_key = api_key
        self.model = model

    def send_prompt(self, prompt: str, system_prompt: str = None) -> tuple[int, str]:
        """
        Send a prompt to the AI assistant and return the response.

        :param prompt:
        :param system_prompt:
        :return:
        """
        if not system_prompt:
            system_prompt = ("You are a helpful assistant. "
                             "You only provide information about music, artists, and songs. "
                             "Please be extremely concise, answer with no more then 4 sentences (prefer 2).")

        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        data = {"model": self.model,
                "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
                "stream": False}

        try:
            response = requests.post(self.endpoint_url, headers=headers, json=data)
            response.raise_for_status()

            # Note: this may need to be adjusted based on the API response structure:
            result = response.json().get('choices', [{}])[0].get('message', '')['content']
            tokens = response.json().get('usage', {}).get('total_tokens', 0)
            logger.info(f"This request used {tokens} tokens.")

            return response.status_code, result
        except requests.RequestException as e:
            logger.warning(f"Error sending prompt: {e}")
            return (None, str(e))
