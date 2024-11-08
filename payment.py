import os
import stripe
from flask import Flask, request, jsonify, url_for, render_template

app = Flask(__name__)

# 配置 Stripe API 私鑰
stripe.api_key = "sk_test_51QBrlCByxTEIQfBXCEuz9gYnoZD53sOZR80clSPblmSW3MbtmEsM5C7AvFK4nEPyuKpRFiwCFXwhlQEwnvwwVlpV00dLCqWczC"

@app.route("/")
def front():
    return render_template("front.html")


@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        # 從請求中獲取支付金額和支付方法 ID
        data = request.json
        amount = int(data['amount']) * 100  # Stripe 接受的金額單位為分

        # 創建支付 (Payment Intent)
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,   # 支付金額，單位為分（例如 TWD 100 = 10000 分
            currency='twd',
            payment_method=data['payment_method_id'],  # 客户端傳入的支付方法 ID
            confirmation_method='manual',  # 手動確認支付
            confirm=True,   # 自動確認支付
            return_url="http://localhost:4242/success"  # 客户完成支付後的跳轉連接
        )

        # 返回支付意圖的 JSON 格式
        return jsonify(payment_intent)

    except Exception as e:
        # 如果創建支付時發生錯誤，返回錯誤訊息
        return jsonify(error=str(e)), 403

# 成功頁面
@app.route('/success', methods=['GET'])
def success():
    return "<h1>付款成功！謝謝您的購買。</h1>"

if __name__ == '__main__':
    app.run(port=4242)
