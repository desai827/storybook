import os
from typing import List, Dict

import openai
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")


class Storybook:
    prompt: str
    current_story: str
    variations: List[str]
    pages: Dict[str, str]

    def __init__(self):
        self.prompt = ""
        self.current_story = ""
        self.variations = []
        self.pages = {}

    def generate_story(
        self,
        prompt: str = "tell me a story about Kaiya, a baby that goes on an adventure",
        variant_count: int = 1,
    ) -> requests.Response:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=4096 - len(prompt),
            top_p=1,
            n=variant_count,
        )

        self.variations = [choice["text"] for choice in response.choices]
        self.current_story = self.variations[0][2:].replace("\n\n", "\n")

        return response

    def get_current_story(self) -> str:
        return self.current_story

    def _generate_images(self) -> None:
        pages = {}
        for prompt in self.current_story.splitlines():
            pages[prompt] = openai.Image.create(prompt=f"illustration: {prompt}")[
                "data"
            ][0]["url"]

        self.pages = pages

    def generate_storybook(self):
        if not self.current_story:
            self.generate_story()

        if not self.pages:
            self._generate_images()

        html_page = "<body>"
        for text, image in self.pages.items():
            html_page += f"<p>{text}</p><img src='{image}' />"

        html_page += "</body>"

        return html_page
