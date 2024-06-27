import os
import json
import gradio as gr


class Frontend:

    def __init__(self, levels_json, starting_level=1):
        self.theme = gr.themes.Soft(
            primary_hue="red",
            secondary_hue="teal",
            font=[
                gr.themes.GoogleFont("Space Grotesk"),
                "ui-sans-serif",
                "system-ui",
                "sans-serif",
            ],
        )
        self.unlocked_levels = list(range(1, starting_level+1))
        self.current_level = starting_level
        self.levels_json = levels_json
        self.max_level = len(self.levels_json)
        if starting_level > self.max_level:
            raise Exception("Starting level is greater than max level")

    def check_word(self, word):
        if word.upper() == self.secret_word.upper():
            if (
                self.current_level == self.unlocked_levels[-1]
                and self.current_level < self.max_level
            ):
                self.unlocked_levels.append(self.unlocked_levels[-1] + 1)
            return "Correct!", gr.Dropdown(
                choices=self.unlocked_levels,
                value=self.current_level,
                label="Level",
                info="Find the secret word to unlock more levels!",
                interactive=True,
            )

        else:
            print(self.unlocked_levels)
            return "Incorrect!", gr.Dropdown(
                choices=self.unlocked_levels,
                value=self.current_level,
                label="Level",
                info="Find the secret word to unlock more levels!",
                interactive=True,
            )

    def update_current_level(self, selected_level, levels_json):
        levels_data = json.loads(levels_json)
        self.current_level = selected_level
        print(f"Current level: {self.current_level}")
        self.secret_word = next(
            (item for item in levels_data if item.get("level") == self.current_level),
            None,
        )["secret_word"]

    def launch(self, reply_function, levels_data):
        self.secret_word = next(
            (item for item in levels_data if item.get("level") == self.current_level), None
        )["secret_word"]
        self.reply_function = reply_function

        with gr.Blocks(theme=self.theme) as frontend:
            levels_json_state = gr.State(json.dumps(levels_data))

            self.level_dropdown = gr.Dropdown(
                choices=self.unlocked_levels,
                value=self.current_level,
                label="Level",
                info="Find the secret word to unlock more levels!",
                interactive=True,
            )

            self.level_dropdown.change(
                fn=self.update_current_level,
                inputs=[self.level_dropdown, levels_json_state],
                outputs=[],
            )

            with gr.Row():
                word_input = gr.Textbox(label="Ask a question...")
                result_output = gr.Textbox(label="Bot Response")
                word_input.submit(
                    fn=reply_function,
                    inputs=[word_input, self.level_dropdown],
                    outputs=result_output,
                )
            send_button = gr.Button("Send")
            send_button.click(
                fn=reply_function,
                inputs=[word_input, self.level_dropdown],
                outputs=result_output,
            )

            with gr.Row():
                word_input = gr.Textbox(label="Enter the secret word")
                result_output = gr.Textbox(label="Result")
                word_input.submit(
                    fn=self.check_word,
                    inputs=word_input,
                    outputs=[result_output, self.level_dropdown],
                )
            check_button = gr.Button("Check")
            check_button.click(
                fn=self.check_word,
                inputs=word_input,
                outputs=[result_output, self.level_dropdown],
            )

        frontend.launch()
