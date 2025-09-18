import asyncio
import json
import os
import uuid

import httpx
import reflex as rx


class SettingsState(rx.State):
    # The accent color for the app
    color: str = "violet"

    # The font family for the app
    font_family: str = "Poppins"

    @rx.event
    def set_color(self, color: str):
        self.color = color

    @rx.event
    def set_font_family(self, font_family: str):
        self.font_family = font_family


class State(rx.State):
    # The current question being asked.
    question: str

    # Whether the app is processing a question.
    processing: bool = False

    # Keep track of the chat history as a list of (question, answer) tuples.
    chat_history: list[tuple[str, str]] = []

    user_id: str = str(uuid.uuid4())

    @rx.event
    def set_question(self, question: str):
        self.question = question

    async def answer(self):
        # Set the processing state to True.
        self.processing = True
        yield

        # convert chat history to a list of dictionaries
        chat_history_dicts = []
        for chat_history_tuple in self.chat_history:
            chat_history_dicts.append(
                {"role": "user", "content": chat_history_tuple[0]}
            )
            chat_history_dicts.append(
                {"role": "assistant", "content": chat_history_tuple[1]}
            )

        self.chat_history.append((self.question, ""))

        # Clear the question input.
        question = self.question
        self.question = ""

        # Yield here to clear the frontend input before continuing.
        yield

        client = httpx.AsyncClient()

        # call the agentic workflow
        input_payload = {
            "chat_history_dicts": chat_history_dicts,
            "user_input": question,
        }
        deployment_name = os.environ.get("DEPLOYMENT_NAME", "MyDeployment")
        apiserver_url = os.environ.get("APISERVER_URL", "http://localhost:4501")
        response = await client.post(
            f"{apiserver_url}/deployments/{deployment_name}/tasks/create",
            json={"input": json.dumps(input_payload)},
            timeout=60,
        )
        answer = response.text

        for i in range(len(answer)):
            # Pause to show the streaming effect.
            await asyncio.sleep(0.01)
            # Add one letter at a time to the output.
            self.chat_history[-1] = (
                self.chat_history[-1][0],
                answer[: i + 1],
            )
            yield

        # Add to the answer as the chatbot responds.
        answer = ""
        yield

        async for item in session:
            if hasattr(item.choices[0].delta, "content"):
                if item.choices[0].delta.content is None:
                    break
                answer += item.choices[0].delta.content
                self.chat_history[-1] = (self.chat_history[-1][0], answer)
                yield

        # Ensure the final answer is added to chat history
        if answer:
            self.chat_history[-1] = (self.chat_history[-1][0], answer)
            yield

        # Set the processing state to False.
        self.processing = False

    async def handle_key_down(self, key: str):
        if key == "Enter":
            async for t in self.answer():
                yield t

    def clear_chat(self):
        # Reset the chat history and processing state
        self.chat_history = []
        self.processing = False
