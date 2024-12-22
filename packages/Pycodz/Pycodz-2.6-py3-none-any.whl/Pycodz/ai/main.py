import requests
from api import API
class blackboxai:
    def __init__(
            self
    ):
        self.titel =  """Generate response from www.blackboxai.com"""
    def chat(
            self,
            message: str,
            module
        ):
        return API.generate(
            message=message,
            module=module
            )