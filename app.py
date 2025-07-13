from flask import Flask, render_template, request, jsonify
import requests
import asyncio
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import threading
import time
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the hedge fund components
from main import run_hedge_fund, create_workflow
from utils.display import print_trading_output

app = Flask(__name__)

class HedgeFundWebApp:
    def __init__(self):
        self.analysis_results = {}
        self.crypto_data = {}
        
    def get_crypto_data(self):
        """Fetch top 8 cryptocurrencies from CoinGecko API (free)"""
        try:
            # CoinGecko API - free tier
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 8,
                'page': 1,
                'sparkline': True,
                'price_change_percentage': '1h,24h,7d'
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                processed_data = []
                
                for coin in data:
                    processed_data.append({
                        'name': coin['name'],
                        'symbol': coin['symbol'].upper(),
                        'current_price': coin['current_price'],
                        'market_cap': coin['market_cap'],
                        'price_change_1h': coin.get('price_change_percentage_1h_in_currency', 0),
                        'price_change_24h': coin['price_change_percentage_24h'],
                        'price_change_7d': coin.get('price_change_percentage_7d_in_currency', 0),
                        'image': coin['image'],
                        'market_cap_rank': coin['market_cap_rank']
                    })
                
                self.crypto_data = processed_data
                return processed_data
            else:
                return []
        except Exception as e:
            print(f"Error fetching crypto data: {e}")
            return []
    
    def run_hedge_fund_analysis(self, tickers, start_date, end_date, initial_cash=100000):
        """Run the hedge fund analysis"""
        try:
            # Parse tickers
            ticker_list = [ticker.strip() for ticker in tickers.split(",")]
            
            # Initialize portfolio
            portfolio = {
                "cash": float(initial_cash),
                "positions": {ticker: 0 for ticker in ticker_list}
            }
            
            # Run analysis with default analysts
            result = run_hedge_fund(
                tickers=ticker_list,
                start_date=start_date,
                end_date=end_date,
                portfolio=portfolio,
                show_reasoning=True,
                selected_analysts=["technical_analyst", "fundamentals_analyst", "sentiment_analyst", "valuation_analyst"]
            )
            
            self.analysis_results = result
            return result
            
        except Exception as e:
            print(f"Error running hedge fund analysis: {e}")
            return {"error": str(e)}

# Initialize the web app
hedge_app = HedgeFundWebApp()

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/api/crypto')
def get_crypto():
    """API endpoint for cryptocurrency data"""
    crypto_data = hedge_app.get_crypto_data()
    return jsonify(crypto_data)

@app.route('/api/analyze', methods=['POST'])
def analyze_stocks():
    """API endpoint for hedge fund analysis"""
    data = request.json
    
    tickers = data.get('tickers', 'AAPL,MSFT,NVDA')
    start_date = data.get('start_date', (datetime.now() - relativedelta(months=3)).strftime('%Y-%m-%d'))
    end_date = data.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    initial_cash = data.get('initial_cash', 100000)
    
    # Run analysis in background
    def run_analysis():
        result = hedge_app.run_hedge_fund_analysis(tickers, start_date, end_date, initial_cash)
        return result
    
    try:
        result = run_analysis()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/status')
def get_status():
    """Get current analysis status"""
    return jsonify({
        "crypto_data": len(hedge_app.crypto_data),
        "analysis_results": bool(hedge_app.analysis_results),
        "last_updated": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting AI Hedge Fund Dashboard...")
    print("🌐 Server will be accessible at:")
    print("   - Local: http://localhost:5000")
    print("   - Network: http://0.0.0.0:5000")
    print("   - External: http://[your-server-ip]:5000")
    print("📊 Cryptocurrency data loading...")
    print("🤖 AI analysis ready!")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)