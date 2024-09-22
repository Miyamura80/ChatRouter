from .helicone import HeliconeChatObject
from openai import APIConnectionError
from typing import Dict, Any

from global_config.global_config import global_config


class ChatRouter:
    def __init__(
        self,
        config_dict: Dict[str, Any],
        session_path_postfix: str = "",
        type="helicone",
    ) -> None:

        # We use cheaper models for testing
        model_name = (
            global_config.cheap_model_name
            if "test" in config_dict and config_dict["test"]
            else config_dict["model_name"] or global_config.model_name
        )

        if type == "helicone":
            self.llm = HeliconeChatObject(
                session_name=config_dict["session_name"],
                model_name=model_name,
                temperature=config_dict["temperature"] or global_config.temperature,
                request_timeout=config_dict["request_timeout"]
                or global_config.request_timeout,
                session_path=config_dict["session_path"] + session_path_postfix,
                session_id=config_dict["session_id"],
            )
        else:
            self.llm = HeliconeChatObject(
                session_name=config_dict["session_name"],
                model_name=model_name,
                temperature=config_dict["temperature"] or global_config.temperature,
                request_timeout=config_dict["request_timeout"]
                or global_config.request_timeout,
                session_path=config_dict["session_path"] + session_path_postfix,
                session_id=config_dict["session_id"],
            )

    def invoke(self, messages):
        try:
            result = self.llm.invoke(messages)
        except APIConnectionError as e:
            print(f"OpenAI API Connection Error: {e}")
            return "Sorry, there was a network error. Please try again later."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "An unexpected error occurred. Please try again."
        return result
