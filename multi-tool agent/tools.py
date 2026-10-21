import requests
from geopy.geocoders import Nominatim
from rag import OllamaEmbeddingGenerator, SimpleVectorSearch

# Initialize geolocator
geolocator = Nominatim(user_agent="multi_agent")

# Load the embeddings from the file
embeddings = OllamaEmbeddingGenerator().load_embeddings("hec_outline_embeddings.json")

# Initialize the vector search
vector_search = SimpleVectorSearch(embeddings['embeddings'], embeddings['texts'])

print("🔍 Vector search initialized!")

# ============================================================================
# TOOL 1: WEATHER TOOL
# ============================================================================
def get_weather(location: str):
    """
    Get the current weather for a location
    """
    try:
        # Get the location coordinates
        location_obj = geolocator.geocode(location)
        if not location_obj:
            return f"Location '{location}' not found"
        
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={location_obj.latitude}&longitude={location_obj.longitude}&current_weather=true")
        data = response.json()
        weather = data["current_weather"]
        return weather
    except Exception as e:
        return f"Error getting weather: {e}"

# ============================================================================
# TOOL 6: CRYPTOCURRENCY TOOL
# ============================================================================
def get_crypto_price(symbol: str = "bitcoin"):
    """
    Get current cryptocurrency price
    Common symbols: bitcoin, ethereum, litecoin, dogecoin, etc.
    """
    try:
        # Using CoinGecko API (free)
        symbol = symbol.lower()
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd")
        if response.status_code == 200:
            data = response.json()
            if symbol in data:
                return {
                    "cryptocurrency": symbol.title(),
                    "price_usd": data[symbol]["usd"],
                    "timestamp": "current"
                }
            else:
                return f"Cryptocurrency '{symbol}' not found"
        else:
            return f"Failed to get crypto price: HTTP {response.status_code}"
    except Exception as e:
        return f"Error getting crypto price: {e}"

# ============================================================================
# TOOL 3: KNOWLEDGE BASE TOOL
# ============================================================================
def search_in_knowledge_base(query: str):
    """
    Search the knowledge base for the query
    """
    embedding_generator = OllamaEmbeddingGenerator()
    return vector_search.search_by_text(query, embedding_generator, top_k=5)
