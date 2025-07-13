from flask import Flask, render_template, request, jsonify, session
import subprocess
import os
import sys
import json
from datetime import datetime, timedelta
import threading
import time
import uuid

app = Flask(__name__)
app.secret_key = 'ai-hedge-fund-secret-key'

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Store running jobs
running_jobs = {}

def run_hedge_fund_analysis(job_id, tickers, start_date, end_date, show_reasoning, initial_cash):
    """Run hedge fund analysis in a separate thread"""
    try:
        cmd = [
            'poetry', 'run', 'python', 'src/main.py',
            '--tickers', tickers,
            '--initial-cash', str(initial_cash)
        ]
        
        if start_date:
            cmd.extend(['--start-date', start_date])
        if end_date:
            cmd.extend(['--end-date', end_date])
        if show_reasoning:
            cmd.append('--show-reasoning')
        
        # Set PATH to include poetry
        env = os.environ.copy()
        env['PATH'] = '/home/ubuntu/.local/bin:' + env.get('PATH', '')
        
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd='/workspace',
            env=env,
            timeout=300  # 5 minute timeout
        )
        
        running_jobs[job_id] = {
            'status': 'completed',
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr,
            'timestamp': datetime.now().isoformat()
        }
        
    except subprocess.TimeoutExpired:
        running_jobs[job_id] = {
            'status': 'timeout',
            'success': False,
            'output': '',
            'error': 'Analysis timed out after 5 minutes',
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        running_jobs[job_id] = {
            'status': 'error',
            'success': False,
            'output': '',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def run_backtester(job_id, tickers, start_date, end_date):
    """Run backtester in a separate thread"""
    try:
        cmd = [
            'poetry', 'run', 'python', 'src/backtester.py',
            '--ticker', tickers
        ]
        
        if start_date:
            cmd.extend(['--start-date', start_date])
        if end_date:
            cmd.extend(['--end-date', end_date])
        
        # Set PATH to include poetry
        env = os.environ.copy()
        env['PATH'] = '/home/ubuntu/.local/bin:' + env.get('PATH', '')
        
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd='/workspace',
            env=env,
            timeout=300  # 5 minute timeout
        )
        
        running_jobs[job_id] = {
            'status': 'completed',
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr,
            'timestamp': datetime.now().isoformat()
        }
        
    except subprocess.TimeoutExpired:
        running_jobs[job_id] = {
            'status': 'timeout',
            'success': False,
            'output': '',
            'error': 'Backtesting timed out after 5 minutes',
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        running_jobs[job_id] = {
            'status': 'error',
            'success': False,
            'output': '',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    tickers = data.get('tickers', 'AAPL,MSFT,NVDA')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    show_reasoning = data.get('show_reasoning', False)
    initial_cash = float(data.get('initial_cash', 100000))
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # Start analysis in background thread
    running_jobs[job_id] = {'status': 'running'}
    thread = threading.Thread(
        target=run_hedge_fund_analysis,
        args=(job_id, tickers, start_date, end_date, show_reasoning, initial_cash)
    )
    thread.start()
    
    return jsonify({'job_id': job_id})

@app.route('/backtest', methods=['POST'])
def backtest():
    data = request.json
    tickers = data.get('tickers', 'AAPL,MSFT,NVDA')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # Start backtesting in background thread
    running_jobs[job_id] = {'status': 'running'}
    thread = threading.Thread(
        target=run_backtester,
        args=(job_id, tickers, start_date, end_date)
    )
    thread.start()
    
    return jsonify({'job_id': job_id})

@app.route('/job/<job_id>')
def get_job_status(job_id):
    if job_id in running_jobs:
        return jsonify(running_jobs[job_id])
    else:
        return jsonify({'status': 'not_found'}), 404

@app.route('/test')
def test():
    return jsonify({
        'status': 'success',
        'message': 'AI Hedge Fund Web Interface is running!',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/testpage')
def test_page():
    """Serve a simple test page to verify browser functionality"""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Hedge Fund - Test Page</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            color: white;
            text-align: center;
        }
        .container {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 3rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        h1 { font-size: 3rem; margin-bottom: 1rem; }
        p { font-size: 1.2rem; margin-bottom: 2rem; }
        .status {
            background: #10b981;
            color: white;
            padding: 1rem 2rem;
            border-radius: 50px;
            font-weight: bold;
            font-size: 1.1rem;
        }
        .links { margin-top: 2rem; }
        a {
            color: #fbbf24;
            text-decoration: none;
            font-weight: bold;
            font-size: 1.1rem;
            margin: 0 1rem;
        }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Hedge Fund</h1>
        <p>Web Interface Test Page</p>
        <div class="status">✅ Server is Working!</div>
        <div class="links">
            <a href="/">Main Interface</a>
            <a href="/test">API Test</a>
        </div>
        <p style="margin-top: 2rem; font-size: 0.9rem; opacity: 0.8;">
            If you can see this page, your browser and server are working correctly.<br>
            Try the Main Interface link above to access the full application.
        </p>
    </div>
</body>
</html>'''

if __name__ == '__main__':
    print("🚀 Starting AI Hedge Fund Web Interface...")
    print(f"🌐 Server will be available at:")
    print(f"   - http://0.0.0.0:5000/")
    print(f"   - http://127.0.0.1:5000/")
    print(f"   - http://172.30.0.2:5000/")
    print(f"🔗 Test endpoint: http://172.30.0.2:5000/test")
    print("")
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)