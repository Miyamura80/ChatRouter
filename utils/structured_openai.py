from openai import OpenAI
from typing import List, Dict, Any
from global_config.global_config import global_config

# NOTE: There is another way to get structured output from OpenAI with function calling
# https://openai.com/index/introducing-structured-outputs-in-the-api/


class OpenAIStructuredChat:
    def __init__(
        self,
        config_dict: Dict[str, Any],
        session_path_postfix: str = "",
        output_schema: Dict[str, Any] = {},
    ):
        self.client = OpenAI(
            api_key=global_config.OPENAI_API_KEY,
            base_url="https://oai.helicone.ai/v1",
            default_headers={
                "Helicone-Auth": f"Bearer {global_config.HELICONE_API_KEY}",
            },
        )

        # We use cheaper models for testing
        self.model_name = (
            global_config.cheap_model_name
            if "test" in config_dict and config_dict["test"]
            else config_dict["model_name"] or global_config.model_name
        )

        self.config = config_dict
        self.output_schema = output_schema
        self.full_session_path = config_dict["session_path"] + session_path_postfix

    def invoke(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        print(self.config)

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=self.config["temperature"] or global_config.temperature,
            timeout=self.config["request_timeout"] or global_config.request_timeout,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "get_structured_output",
                    "strict": True,
                    "schema": self.output_schema,
                },
            },
            extra_headers={
                "Helicone-Auth": f"Bearer {global_config.HELICONE_API_KEY}",
                "Helicone-Session-Id": self.config["session_id"],
                "Helicone-Session-Name": self.config["session_name"],
                "Helicone-Session-Path": self.full_session_path,
            },
        )

        return response
