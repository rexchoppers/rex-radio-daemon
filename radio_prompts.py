class RadioPrompts:
    def __init__(
            self,
            station_name: str,
            personality: str = "friendly",
            tone: str = "upbeat"
    ):
        self.station_name = station_name
        self.personality = personality
        self.tone = tone

    def base_system_prompt(self):
        return (
            "<|system|>\n"
            "You are a professional radio script generator. "
            "Your job is to write natural, engaging, and context-aware radio dialogue. "
            f"Your personality is {self.personality} and your tone is {self.tone}. "
            f"You are the host of {self.station_name}.\n"
            "<|end|>\n"
        )

    def station_start_welcome_prompt(self, current_time: str):
        prompt = (
                self.base_system_prompt() +
                "<|user|>\n"
                f"Write a single-paragraph welcome message for the station '{self.station_name}' "
                f"for the current time: {current_time}. "
                "Make it friendly, upbeat, and like a professional radio DJ. "
                "Do not include instructions, lists, or multiple separate sentences — just one cohesive paragraph.\n"
                "<|assistant|>"
        )
        return prompt

    def transition_prompt(self, next_segment: str):
        return (
                self.base_system_prompt() +
                "<|user|>\n"
                f"Create a short transition line introducing the next segment: {next_segment}. "
                "Keep it conversational and natural.\n"
                "<|assistant|>"
        )
