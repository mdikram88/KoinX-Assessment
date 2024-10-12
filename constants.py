# MongoDB Atlas connection details
USERNAME = "user_007"
PASSWORD = "Password123"
CLUSTER_URL = "learn101.w7vfxhv.mongodb.net"

# Database and collection names
DB_NAME = "Koinx"
COLLECTION_NAME = "crypto_data"

# DB Connection URI
DB_URI = f"mongodb+srv://{USERNAME}:{PASSWORD}@{CLUSTER_URL}/?retryWrites=true&w=majority&ssl=true"

# CoinGecko API
API_URL = "https://api.coingecko.com/api/v3/coins/markets"
HEADERS = {"accept": "application/json"}

# Coins
COINS = ["bitcoin", "matic-network", "ethereum"]
