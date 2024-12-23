class Message:
    def __init__(self, client: any, data: dict):
        self.client = client
        self.data = data
        self.channel_id = data.get("channel_id")
        self.content = data.get("content")
        self.author = data.get("author", {}).get("username")

    async def send_message(self, content: str):
        """Відправка повідомлення в поточний канал."""
        url = f"{self.client.gateway_url}/channels/{self.channel_id}/messages"
        payload = {"content": content}
        headers = self.client.headers
        async with self.client.session.post(url, json=payload, headers=headers) as response:
            return await response.json()
