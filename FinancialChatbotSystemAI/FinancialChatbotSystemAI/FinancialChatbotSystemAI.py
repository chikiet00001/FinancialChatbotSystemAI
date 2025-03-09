
from flask import Flask, request, jsonify
import requests
import random

app = Flask(__name__)

# API tài chính
EXCHANGE_RATE_API = "https://api.exchangerate-api.com/v4/latest/USD"
GOLD_PRICE_API = "https://www.metals-api.com/api/latest?access_key=YOUR_ACCESS_KEY&base=USD&symbols=XAU"
STOCK_API = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey=YOUR_STOCK_API_KEY"

# Lấy tỷ giá hối đoái
def get_exchange_rate(currency):
    try:
        response = requests.get(EXCHANGE_RATE_API).json()
        rate = response['rates'].get(currency.upper())
        if rate:
            return f"Tỷ giá {currency}/USD hiện tại: {rate}"
        return "Không tìm thấy thông tin tỷ giá."
    except Exception as e:
        return "Lỗi khi lấy dữ liệu tỷ giá."

# Lấy giá vàng hiện tại
def get_gold_price():
    try:
        response = requests.get(GOLD_PRICE_API).json()
        gold_price = response['rates'].get("XAU")
        if gold_price:
            return f"Giá vàng hiện tại: {gold_price} USD/ounce"
        return "Không tìm thấy thông tin giá vàng."
    except Exception as e:
        return "Lỗi khi lấy dữ liệu giá vàng."

# Lấy giá cổ phiếu
def get_stock_price(symbol):
    try:
        response = requests.get(STOCK_API.format(symbol=symbol)).json()
        latest_time = list(response["Time Series (5min)"].keys())[0]
        stock_price = response["Time Series (5min)"][latest_time]["1. open"]
        return f"Giá cổ phiếu {symbol} hiện tại: {stock_price} USD"
    except Exception as e:
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

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()
    
    if "tỷ giá" in user_message:
        words = user_message.split()
        for word in words:
            if len(word) == 3:  # Mã tiền tệ thường có 3 chữ cái (VD: VND, EUR, JPY)
                return jsonify({"reply": get_exchange_rate(word)})
    
    elif "giá vàng" in user_message:
        return jsonify({"reply": get_gold_price()})
    
    elif "cổ phiếu" in user_message:
        words = user_message.split()
        for word in words:
            if word.isalpha() and len(word) > 1:  # Mã chứng khoán thường có 2-5 chữ cái (VD: AAPL, TSLA)
                return jsonify({"reply": get_stock_price(word.upper())})
    
    elif "lời khuyên tài chính" in user_message:
        return jsonify({"reply": get_financial_advice()})
    
    return jsonify({"reply": "Xin lỗi, tôi chưa hiểu câu hỏi của bạn. Hãy thử hỏi về tỷ giá, giá vàng, giá cổ phiếu hoặc lời khuyên tài chính!"})

if __name__ == "__main__":
    app.run(debug=True)
