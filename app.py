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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)