from flask import Flask, request, jsonify, render_template
import os
import requests
import random

app = Flask(__name__)

# Sử dụng biến môi trường cho API Keys
EXCHANGE_RATE_API = "https://api.exchangerate-api.com/v4/latest/USD"
GOLD_PRICE_API = f"https://www.metals-api.com/api/latest?access_key={os.getenv('METALS_API_KEY')}&base=USD&symbols=XAU"
STOCK_API_KEY = os.getenv("STOCK_API_KEY", "DEFAULT_KEY")
STOCK_API = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={{symbol}}&interval=5min&apikey={STOCK_API_KEY}"

# Lấy tỷ giá hối đoái
def get_exchange_rate(currency):
    try:
        response = requests.get(EXCHANGE_RATE_API).json()
        rate = response.get('rates', {}).get(currency.upper())
        if rate:
            return f"Tỷ giá {currency}/USD hiện tại: {rate}"
        return "Không tìm thấy thông tin tỷ giá."
    except Exception as e:
        return "Lỗi khi lấy dữ liệu tỷ giá."

# Lấy giá vàng hiện tại
def get_gold_price():
    try:
        response = requests.get(GOLD_PRICE_API).json()
        if 'rates' in response and 'XAU' in response['rates']:
            gold_price = response['rates']['XAU']
            return f"Giá vàng hiện tại: {gold_price:.2f} USD/ounce"
        return "Không tìm thấy thông tin giá vàng."
    except Exception:
        return "Lỗi khi lấy dữ liệu giá vàng."

# Lấy giá cổ phiếu
def get_stock_price(symbol):
    try:
        response = requests.get(STOCK_API.format(symbol=symbol)).json()
        if "Time Series (5min)" in response:
            latest_time = list(response["Time Series (5min)"].keys())[0]
            stock_price = response["Time Series (5min)"][latest_time]["1. open"]
            return f"Giá cổ phiếu {symbol} hiện tại: {stock_price} USD"
        return f"Không tìm thấy thông tin về mã cổ phiếu {symbol}."
    except Exception:
        return "Lỗi khi lấy dữ liệu cổ phiếu."

# Lời khuyên tài chính
def get_financial_advice():
    advices = [
        "Hãy tiết kiệm ít nhất 20% thu nhập mỗi tháng và đa dạng hóa danh mục đầu tư.",
        "Đầu tư vào bản thân bằng cách học tập và phát triển kỹ năng.",
        "Tránh vay nợ không cần thiết và luôn có một quỹ khẩn cấp.",
        "Tận dụng lãi suất kép bằng cách đầu tư sớm và đều đặn.",
        "Xây dựng ngân sách hợp lý và theo dõi chi tiêu hàng tháng."
    ]
    return random.choice(advices)

@app.route("/", methods=["GET", "POST"])
def home():
    exchange_rate = ""
    stock_price = ""
    gold_price = ""
    financial_advice = get_financial_advice()

    if request.method == "POST":
        if "currency" in request.form:
            currency = request.form["currency"]
            exchange_rate = get_exchange_rate(currency)
        elif "stock_symbol" in request.form:
            stock_symbol = request.form["stock_symbol"]
            stock_price = get_stock_price(stock_symbol)
        elif "gold" in request.form:
            gold_price = get_gold_price()

    return render_template("index.html", exchange_rate=exchange_rate, stock_price=stock_price, gold_price=gold_price, financial_advice=financial_advice)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
