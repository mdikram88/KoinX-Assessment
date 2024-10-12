import pymongo
from pymongo import MongoClient
from constants import *
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, make_response, jsonify
import requests
import pandas as pd


client = MongoClient(DB_URI)   # Create a MongoDB client
db = client[DB_NAME]        # Access the database
collection = db[COLLECTION_NAME]    # Access the collection

app = Flask(__name__)


def fetch_and_upload_crypto_data():
    coins = ",".join(COINS)
    params = {"vs_currency": "usd", "ids": coins}
    response = requests.get(API_URL, headers=HEADERS, params=params)

    lt = []
    for coin in response.json():
        dt = {"coin_id": coin["id"],
              "name": coin["name"],
              "currentPrice": coin["current_price"],
              "marketCap": coin["market_cap"],
              "24h_Change": coin["price_change_24h"],
              "timestamp": datetime.now()}

        lt.append(dt)
    print("Data Collected")

    # Insert document (write operation)
    try:
        result = collection.insert_many(lt)
        print("Documents inserted successfully!")
    except pymongo.errors.BulkWriteError as e:
        print("Error inserting documents:", e.details)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_upload_crypto_data, 'interval', hours=2)
    scheduler.start()


# Route for your web app
@app.route('/')
def home():
    return "Web application is running, refer to /stats or /deviation for results"


@app.route("/stats")
def get_latest_data():
    coin = request.args.get("coin")
    print(coin)
    if coin is None:
        return "Please provide 'coin' query parameter"
    result = collection.find_one({"coin_id": coin}, sort=[("timestamp", -1)])

    if result is not None:
        dt = {"Price": result["currentPrice"],
              "marketCap": result["marketCap"],
              "24hChange": result["24h_Change"]}
        return make_response(jsonify(dt), 200)
    return make_response(jsonify({"message": "No data records for the given coin"}), 400)



@app.route("/deviation")
def get_deviation():
    coin = request.args.get("coin")
    if coin is None:
        return "Please provide 'coin' query parameter"

    results = collection.find({"coin_id": coin}, sort=[("timestamp", -1)]).limit(100)

    try:
        results[0]

        prices = []
        for result in results:
            prices.append(result["currentPrice"])

        std = pd.Series(prices).std()

        return make_response(jsonify({"deviation": round(std, 2)}), 200)

    except IndexError as e:
        print(e)
        return make_response(jsonify({"deviation": 0}))


if __name__ == "__main__":
    # Start the background scheduler before starting the web server
    start_scheduler()

    # Start the Flask web server (you can replace this with any other framework's method)
    app.run(debug=True, use_reloader=False)  # `use_reloader=False` to avoid double-start issues with APScheduler

    client.close()




