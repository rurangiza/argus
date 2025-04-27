from datetime import datetime

from src.argus.tools.tool import Tool


class GetDatetime(Tool):
    """Get the current date and time"""

    def resolve(self) -> str:
        return datetime.today().strftime('%d/%m/%Y, %H:%M:%S')
