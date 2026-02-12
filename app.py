from flask import Flask, render_template, request, jsonify
from compliance_engine import calculate_trust_score
from blockchain import store_hash_on_algorand
import json
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify_product():
    data = request.json
    
    # 1. Run Compliance Engine
    result = calculate_trust_score(data)
    
    # 2. Prepare Data for Blockchain (Immutable Record)
    record = {
        "product_name": data.get("product_name"),
        "timestamp": str(datetime.datetime.now()),
        "score": result["final_score"],
        "status": result["status"]
    }
    
    # 3. Store on Algorand
    # We store the result summary to save space/fees
    tx_id = store_hash_on_algorand(json.dumps(record))
    
    # 4. Return result to Frontend
    response = {
        "compliance": result,
        "blockchain_tx_id": tx_id,
        "timestamp": record["timestamp"]
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
