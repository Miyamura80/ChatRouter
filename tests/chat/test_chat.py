import unittest

from tests.test_class import TestCaseClass, ci_test
from utils import ChatRouter
from langchain.schema import HumanMessage
import uuid
from global_config.global_config import global_config
from human_id import generate_id


class TestChatRouter(TestCaseClass):
    def setUp(self) -> None:
        super().setUp()

        # Usually, just pass self.config in tests for ChatRouter
        self.chat = ChatRouter(
            config_dict={
                "session_name": "Unit Tests: test_chat",
                "session_path": "/test_chat",
                "session_id": generate_id(),
                "model_name": global_config.model_name,
                "temperature": 0,
                "request_timeout": 120,
            },
            session_path_postfix="/test_chat_postfix",
        )

    @ci_test
    def test_invoke(self):
        result = self.chat.invoke("Hello")
        print(result)
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
