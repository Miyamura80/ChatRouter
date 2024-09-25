import unittest

from tests.test_class import TestCaseClass, ci_test
from utils import OpenAIStructuredChat
from langchain.schema import HumanMessage
from global_config.global_config import global_config
import json


class TestStructuredOutput(TestCaseClass):
    def setUp(self) -> None:
        super().setUp()

        self.output_schema = {
            "type": "object",
            "properties": {
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "explanation": {"type": "string"},
                            "output": {"type": "string"},
                        },
                        "required": ["explanation", "output"],
                        "additionalProperties": False,
                    },
                },
                "final_answer": {"type": "string"},
            },
            "required": ["steps", "final_answer"],
            "additionalProperties": False,
        }

        self.structured_chat = OpenAIStructuredChat(
            config_dict=self.config,
            session_path_postfix="/structured",
            output_schema=self.output_schema,
        )

    @ci_test
    def test_structured_invoke(self):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Summarize the benefits of exercise."},
        ]
        result = self.structured_chat.invoke(messages)

        response_json = json.loads(result.choices[0].message.content)

        # print("Structured Response:")
        # print(json.dumps(response_json, indent=2))

        # Validate the structure of the response
        self.assertIn("steps", response_json)
        self.assertIsInstance(response_json["steps"], list)
        self.assertIn("final_answer", response_json)
        self.assertIsInstance(response_json["final_answer"], str)

        for step in response_json["steps"]:
            self.assertIn("explanation", step)
            self.assertIn("output", step)
            self.assertIsInstance(step["explanation"], str)
            self.assertIsInstance(step["output"], str)


if __name__ == "__main__":
    unittest.main()
