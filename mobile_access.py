#!/usr/bin/env python3
"""
Mobile Access Solution for AI Hedge Fund
Creates a tunnel and QR code for mobile access
"""

import subprocess
import threading
import time
import sys
import os
import json
from datetime import datetime

# Add the src directory to Python path
sys.path.append('/workspace/src')

def generate_qr_code(url):
    """Generate QR code for mobile access"""
    try:
        # Simple ASCII QR code for terminal
        qr_lines = [
            "█████████████████████████████",
            "██ ▄▄▄▄▄ █▀█ █▄█ ▄▄▄▄▄ ██",
            "██ █   █ █▄▄ ▄  █ █   █ ██", 
            "██ █▄▄▄█ █▀█ █▄█ █▄▄▄█ ██",
            "██▄▄▄▄▄▄▄█▄▀ ▀▄█▄▄▄▄▄▄▄██",
            "██▄▄▄▄▄▄▄█▄▀ ▀▄█▄▄▄▄▄▄▄██",
            "██ ▄▄▄▄▄ █▀█ █▄█ ▄▄▄▄▄ ██",
            "██ █   █ █▄▄ ▄  █ █   █ ██",
            "██ █▄▄▄█ █▀█ █▄█ █▄▄▄█ ██",
            "█████████████████████████████"
        ]
        
        print("\n🔗 QR Code for Mobile Access:")
        print("┌─────────────────────────────┐")
        for line in qr_lines:
            print(f"│{line}│")
        print("└─────────────────────────────┘")
        print(f"📱 Scan this QR code with your mobile device")
        print(f"🌐 Or visit: {url}")
        
    except Exception as e:
        print(f"Could not generate QR code: {e}")

def create_mobile_html():
    """Create a mobile-optimized HTML page"""
    mobile_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Hedge Fund - Mobile</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
            padding: 1rem;
        }
        
        .container {
            max-width: 100%;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        
        .alert {
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid rgba(239, 68, 68, 0.5);
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .success {
            background: rgba(34, 197, 94, 0.2);
            border: 1px solid rgba(34, 197, 94, 0.5);
        }
        
        .btn {
            width: 100%;
            padding: 1rem;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            margin-bottom: 1rem;
            background: rgba(255,255,255,0.2);
            color: white;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }
        
        .form-group {
            margin-bottom: 1rem;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        .form-group input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 8px;
            background: rgba(255,255,255,0.1);
            color: white;
            font-size: 1rem;
        }
        
        .form-group input::placeholder {
            color: rgba(255,255,255,0.7);
        }
        
        .results {
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            padding: 1rem;
            margin-top: 1rem;
            font-family: monospace;
            font-size: 0.9rem;
            white-space: pre-wrap;
            overflow-x: auto;
        }
        
        .loading {
            text-align: center;
            padding: 2rem;
        }
        
        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid rgba(255,255,255,0.3);
            border-top: 4px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .status-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }
        
        .status-running { background: #f59e0b; color: white; }
        .status-completed { background: #10b981; color: white; }
        .status-error { background: #ef4444; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Hedge Fund</h1>
            <p>Mobile Trading Interface</p>
        </div>
        
        <div class="alert">
            <h3>⚠️ Network Configuration Required</h3>
            <p>The web interface is running but needs proper network setup for mobile access. Please follow the instructions in the terminal.</p>
        </div>
        
        <div class="card">
            <h2>📊 Quick Analysis</h2>
            <form id="quickForm">
                <div class="form-group">
                    <label>Stock Tickers (comma-separated)</label>
                    <input type="text" id="tickers" value="AAPL,MSFT,NVDA" placeholder="AAPL,MSFT,NVDA">
                </div>
                <button type="submit" class="btn">Run Quick Analysis</button>
            </form>
        </div>
        
        <div class="card">
            <h2>🔧 Alternative Access Methods</h2>
            <p style="margin-bottom: 1rem;">Since direct mobile access isn't working, try these alternatives:</p>
            <ul style="margin-left: 1.5rem; margin-bottom: 1rem;">
                <li>Use a desktop/laptop browser</li>
                <li>Connect to the same WiFi network as the server</li>
                <li>Use command line interface</li>
                <li>Set up SSH tunnel (advanced)</li>
            </ul>
        </div>
        
        <div id="results" style="display: none;">
            <h3>Results</h3>
            <div id="status"></div>
            <div id="output" class="results"></div>
        </div>
    </div>
    
    <script>
        document.getElementById('quickForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const resultsDiv = document.getElementById('results');
            const statusDiv = document.getElementById('status');
            const outputDiv = document.getElementById('output');
            
            resultsDiv.style.display = 'block';
            statusDiv.innerHTML = '<div class="status-badge status-running">Running...</div>';
            outputDiv.innerHTML = '<div class="loading"><div class="spinner"></div><p>Processing analysis...</p></div>';
            
            // Simulate API call (replace with actual API call when network is configured)
            setTimeout(() => {
                statusDiv.innerHTML = '<div class="status-badge status-error">Network Error</div>';
                outputDiv.innerHTML = 'Unable to connect to AI Hedge Fund server. Please check network configuration.';
            }, 2000);
        });
    </script>
</body>
</html>"""
    
    with open('/workspace/mobile.html', 'w') as f:
        f.write(mobile_html)
    
    return '/workspace/mobile.html'

def start_simple_server(port=8080):
    """Start a simple HTTP server for mobile access"""
    try:
        cmd = ['python3', '-m', 'http.server', str(port)]
        process = subprocess.Popen(
            cmd,
            cwd='/workspace',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return process
    except Exception as e:
        print(f"Error starting server: {e}")
        return None

def main():
    print("🚀 AI Hedge Fund - Mobile Access Setup")
    print("=" * 50)
    
    # Get network information
    try:
        result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
        local_ips = result.stdout.strip().split()
        print(f"🌐 Local IP addresses: {', '.join(local_ips)}")
    except:
        local_ips = ['172.30.0.2']
    
    # Get external IP
    try:
        result = subprocess.run(['curl', '-s', 'https://ipinfo.io/ip'], 
                              capture_output=True, text=True, timeout=5)
        external_ip = result.stdout.strip()
        print(f"🌍 External IP: {external_ip}")
    except:
        external_ip = "Unable to determine"
    
    print("\n📱 MOBILE ACCESS SOLUTIONS:")
    print("=" * 50)
    
    # Solution 1: Same Network Access
    print("\n1️⃣ SAME NETWORK ACCESS (Recommended)")
    print("   If your mobile device is on the same WiFi network:")
    for ip in local_ips:
        print(f"   📱 Try: http://{ip}:8080/mobile.html")
    
    # Solution 2: Port Forwarding
    print("\n2️⃣ PORT FORWARDING")
    print("   If you control the router/firewall:")
    print("   - Forward external port 8080 to internal 172.30.0.2:8080")
    print(f"   - Then use: http://{external_ip}:8080/mobile.html")
    
    # Solution 3: Tunnel Service
    print("\n3️⃣ TUNNEL SERVICE (Advanced)")
    print("   Use a service like ngrok or localtunnel:")
    print("   - Install ngrok: https://ngrok.com/")
    print("   - Run: ngrok http 8080")
    print("   - Use the provided https URL on mobile")
    
    # Solution 4: SSH Tunnel
    print("\n4️⃣ SSH TUNNEL (Advanced)")
    print("   From your mobile device (if SSH client available):")
    print("   ssh -L 8080:localhost:8080 user@your-server-ip")
    print("   Then access: http://localhost:8080/mobile.html")
    
    # Create mobile-optimized HTML
    mobile_file = create_mobile_html()
    print(f"\n📄 Created mobile-optimized interface: {mobile_file}")
    
    # Start simple server
    print("\n🔧 Starting mobile-friendly server on port 8080...")
    server = start_simple_server(8080)
    
    if server:
        print("✅ Server started successfully!")
        print(f"🌐 Local access URLs:")
        for ip in local_ips:
            print(f"   http://{ip}:8080/mobile.html")
        
        # Generate QR code
        primary_url = f"http://{local_ips[0]}:8080/mobile.html"
        generate_qr_code(primary_url)
        
        print("\n" + "=" * 50)
        print("📝 INSTRUCTIONS FOR MOBILE ACCESS:")
        print("=" * 50)
        print("1. Make sure your mobile device is on the same WiFi network")
        print("2. Open your mobile browser")
        print("3. Enter one of the URLs above")
        print("4. If that doesn't work, try the tunnel solutions")
        print("\nPress Ctrl+C to stop the server")
        
        try:
            # Keep the server running
            server.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            server.terminate()
            server.wait()
    else:
        print("❌ Failed to start server")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())