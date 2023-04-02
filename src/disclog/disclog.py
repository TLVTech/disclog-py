import requests
from typing import Optional

class LogLevel:
    Info = 0
    Warning = 1
    Error = 2

class Disclog:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.queue = []
        self.processing = False

    def log(self, level: int, message: str, webhook_url: Optional[str] = None):
        if webhook_url:
            self.webhook_url = webhook_url

        if not self.webhook_url:
            raise ValueError("Webhook URL is required")

        self.queue.append({"level": level, "message": message, "webhook_url": webhook_url})
        if not self.processing:
            self.process_queue()

    def process_queue(self):
        self.processing = True
        while len(self.queue) > 0:
            level = self.queue[0]["level"]
            message = self.queue[0]["message"]
            webhook_url = self.queue[0]["webhook_url"]
            color = None
            title = None
            if level == LogLevel.Info:
                color = 0x3498db # Blue
                title = "Info"
            elif level == LogLevel.Warning:
                color = 0xf1c40f # Yellow
                title = "Warning"
            elif level == LogLevel.Error:
                color = 0xe74c3c # Red
                title = "Error"
            else:
                raise ValueError("Invalid log level")

            try:
                response = requests.post(
                    self.webhook_url,
                    json={
                        "embeds": [
                            {
                                "type": "rich",
                                "title": title,
                                "description": message,
                                "color": color
                            }
                        ]
                    }
                )
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(f"Error sending message to Discord webhook: {e}")
                raise e

            self.queue.pop(0)
        self.processing = False

    def info(self, message: str, webhook_url: Optional[str] = None):
        self.log(LogLevel.Info, message, webhook_url)

    def warning(self, message: str, webhook_url: Optional[str] = None):
        self.log(LogLevel.Warning, message, webhook_url)

    def error(self, message: str, webhook_url: Optional[str] = None):
        self.log(LogLevel.Error, message, webhook_url)
