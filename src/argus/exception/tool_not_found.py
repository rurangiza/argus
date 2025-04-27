class ToolNotFound(Exception):
    def __init__(self, tool_name: str) -> None:
        self.message = f'Tool Not Found: {tool_name}'
        super().__init__(self.message)
