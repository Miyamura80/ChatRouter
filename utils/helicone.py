from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from global_config.global_config import global_config


class HeliconeChatObject:
    def __init__(
        self,
        session_name,
        session_path,
        session_id,
        model_name,
        temperature,
        request_timeout,
    ):
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timeout,
            model_kwargs={
                "extra_headers": {
                    "Helicone-Auth": f"Bearer {global_config.HELICONE_API_KEY}",
                    "Helicone-Session-Id": session_id,
                    "Helicone-Session-Name": session_name,
                    "Helicone-Session-Path": session_path,
                }
            },
            openai_api_base="https://oai.helicone.ai/v1",
        )

    def invoke(self, messages):
        return self.llm.invoke(messages)
