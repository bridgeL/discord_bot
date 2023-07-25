import re
import discord
from contextvars import ContextVar


CURRENT_MSG: ContextVar[discord.message.Message] = ContextVar("CURRENT_MSG")
'''discord msg object'''

CURRENT_PREFIX: ContextVar[str] = ContextVar("CURRENT_PREFIX")
'''prefix'''

CURRENT_CMD: ContextVar[str] = ContextVar("CURRENT_CMD")
'''cmd'''

CURRENT_TEXT: ContextVar[str] = ContextVar("CURRENT_TEXT")
'''the left of msg.content excluding prefix and cmd'''

CURRENT_REGEX: ContextVar[re.Match] = ContextVar("CURRENT_REGEX")
