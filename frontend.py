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
        self.logo_path = "images/agreat_logo_white.png"
        self.unlocked_levels = list(range(1, starting_level + 1))
        self.current_level = starting_level
        self.levels_json = levels_json
        self.max_level = len(self.levels_json)
        if starting_level > self.max_level:
            raise Exception("Starting level is greater than max level")

    def check_word(self, guess):
        print(f"User guessed: {guess}")
        print(f"Secret word: {self.secret_word}")
        if guess.upper() == self.secret_word.upper():
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
            return "Incorrect!", gr.Dropdown(
                choices=self.unlocked_levels,
                value=self.current_level,
                label="Level",
                info="Find the secret word to unlock more levels!",
                interactive=True,
            )
    def change_image(self, levels_json):
        levels_data = json.loads(levels_json)
        avatar_image_file_name = next(
            (item for item in levels_data if item.get("level") == self.current_level),
            None,
        )["avatar_image_file_name"]
        return gr.Image(value=f"images/level_avatars/{avatar_image_file_name}", label="Sophon")

    def update_current_level(self, selected_level, levels_json):
        levels_data = json.loads(levels_json)
        self.current_level = selected_level
        print(f"Current level: {self.current_level}")
        self.secret_word = next(
            (item for item in levels_data if item.get("level") == self.current_level),
            None,
        )["secret_word"]
        print(f"Secret word: {self.secret_word}")

    def launch(self, reply_function, levels_data):
        self.secret_word = next(
            (item for item in levels_data if item.get("level") == self.current_level),
            None,
        )["secret_word"]
        self.reply_function = reply_function

        with gr.Blocks(theme=self.theme, 
                       css="footer {visibility: hidden}"
                       ) as frontend:
            levels_json_state = gr.State(json.dumps(levels_data))

            with gr.Row():
                with gr.Column():
                    # Level dropdown
                    level_dropdown = gr.Dropdown(
                        choices=self.unlocked_levels,
                        value=self.current_level,
                        label="Level",
                        info="Find the secret word to unlock more levels!",
                        interactive=True,
                    )
                    level_dropdown.change(
                        fn=self.update_current_level,
                        inputs=[level_dropdown, levels_json_state],
                        outputs=[],
                    )

                    query_input = gr.Textbox(label="Ask a question...")
                    send_button = gr.Button("Send")
                    bot_response = gr.Textbox(label="Bot Response")
                    send_button.click(
                        fn=reply_function,
                        inputs=[query_input, level_dropdown],
                        outputs=bot_response,
                    )
                    query_input.submit(
                        fn=reply_function,
                        inputs=[query_input, level_dropdown],
                        outputs=bot_response,
                    )
                    with gr.Row():
                        secret_word_input = gr.Textbox(label="Enter the secret word")
                        secret_word_output = gr.Textbox(label="Result")
                        
                        check_button = gr.Button("Check secret word")
                        check_button.click(
                            fn=self.check_word,
                            inputs=secret_word_input,
                            outputs=[secret_word_output, level_dropdown],
                        )
                        secret_word_input.submit(
                                fn=self.check_word,
                                inputs=secret_word_input,
                                outputs=[secret_word_output, level_dropdown],
                            )
                avatar_image_file_name = next(
                        (item for item in levels_data if item.get("level") == self.current_level),
                        None,
                    )["avatar_image_file_name"]
                avatar_image = gr.Image(value=f"images/level_avatars/{avatar_image_file_name}", label="Sophon")
                level_dropdown.change(
                        fn=self.change_image,
                        inputs=[levels_json_state],
                        outputs=[avatar_image],
                    ),
            
            gr.Markdown("""
                        <div style='display: grid; place-items: end center; height: 10vh;'>
                            <div style='text-align: center;'>Made by</div>
                            <img src='/file=images/agreat_logo_white.png' alt='Agreat Logo' style='width: 30%;'>
                        </div>
                        """)

        frontend.launch(allowed_paths=["images"])
