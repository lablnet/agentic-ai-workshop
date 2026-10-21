"""Import the shared tools here; agent examples choose the functions they need."""

from .crypto import get_crypto_price
from .knowledge_base import search_in_knowledge_base
from .maths import calculate
from .weather import get_weather

ALL_TOOLS = [get_weather, get_crypto_price, calculate, search_in_knowledge_base]
