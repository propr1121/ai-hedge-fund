from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import sys
import io
import threading
import time
from main import run_hedge_fund
from utils.analysts import ANALYST_ORDER

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mobile')
def mobile():
    return render_template('mobile.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        
        # Extract parameters
        tickers = [ticker.strip() for ticker in data.get('tickers', '').split(',')]
        start_date = data.get('start_date', '')
        end_date = data.get('end_date', '')
        initial_cash = float(data.get('initial_cash', 100000.0))
        show_reasoning = data.get('show_reasoning', False)
        selected_analysts = data.get('selected_analysts', None)
        
        # Validate tickers
        if not tickers or tickers == ['']:
            return jsonify({'error': 'Please provide at least one ticker symbol'}), 400
        
        # Set default dates if not provided
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            start_date = (end_date_obj - relativedelta(months=3)).strftime("%Y-%m-%d")
        
        # Initialize portfolio
        portfolio = {
            "cash": initial_cash,
            "positions": {ticker: 0 for ticker in tickers}
        }
        
        # Run the hedge fund analysis
        result = run_hedge_fund(
            tickers=tickers,
            start_date=start_date,
            end_date=end_date,
            portfolio=portfolio,
            show_reasoning=show_reasoning,
            selected_analysts=selected_analysts
        )
        
        return jsonify({
            'success': True,
            'result': result,
            'parameters': {
                'tickers': tickers,
                'start_date': start_date,
                'end_date': end_date,
                'initial_cash': initial_cash,
                'show_reasoning': show_reasoning,
                'selected_analysts': selected_analysts
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysts')
def get_analysts():
    """Get available analysts"""
    return jsonify([{'display': display, 'value': value} for display, value in ANALYST_ORDER])

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)