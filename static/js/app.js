// DOM Elements
const analyzeBtn = document.getElementById('analyze-btn');
const tickersInput = document.getElementById('tickers');
const startDateInput = document.getElementById('start-date');
const endDateInput = document.getElementById('end-date');
const initialCashInput = document.getElementById('initial-cash');
const cryptoGrid = document.getElementById('crypto-grid');
const analysisResults = document.getElementById('analysis-results');
const loading = document.getElementById('loading');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeDates();
    loadCryptoData();
    
    // Event listeners
    analyzeBtn.addEventListener('click', runAnalysis);
    
    // Auto-refresh crypto data every 30 seconds
    setInterval(loadCryptoData, 30000);
});

// Initialize default dates
function initializeDates() {
    const today = new Date();
    const threeMonthsAgo = new Date();
    threeMonthsAgo.setMonth(today.getMonth() - 3);
    
    startDateInput.value = threeMonthsAgo.toISOString().split('T')[0];
    endDateInput.value = today.toISOString().split('T')[0];
}

// Load cryptocurrency data
async function loadCryptoData() {
    try {
        const response = await fetch('/api/crypto');
        const cryptoData = await response.json();
        
        if (cryptoData && cryptoData.length > 0) {
            displayCryptoData(cryptoData);
        } else {
            showError('Failed to load cryptocurrency data');
        }
    } catch (error) {
        console.error('Error loading crypto data:', error);
        showError('Error loading cryptocurrency data');
    }
}

// Display cryptocurrency data
function displayCryptoData(cryptoData) {
    cryptoGrid.innerHTML = '';
    
    cryptoData.forEach(coin => {
        const card = createCryptoCard(coin);
        cryptoGrid.appendChild(card);
    });
}

// Create cryptocurrency card
function createCryptoCard(coin) {
    const card = document.createElement('div');
    card.className = 'crypto-card';
    
    const formatPrice = (price) => {
        return price < 1 ? `$${price.toFixed(6)}` : `$${price.toLocaleString()}`;
    };
    
    const formatChange = (change) => {
        const className = change >= 0 ? 'positive' : 'negative';
        const sign = change >= 0 ? '+' : '';
        return `<span class="change-item ${className}">${sign}${change.toFixed(2)}%</span>`;
    };
    
    const formatMarketCap = (marketCap) => {
        if (marketCap >= 1e12) return `$${(marketCap / 1e12).toFixed(2)}T`;
        if (marketCap >= 1e9) return `$${(marketCap / 1e9).toFixed(2)}B`;
        if (marketCap >= 1e6) return `$${(marketCap / 1e6).toFixed(2)}M`;
        return `$${marketCap.toLocaleString()}`;
    };
    
    card.innerHTML = `
        <div class="crypto-header">
            <img src="${coin.image}" alt="${coin.name}" class="crypto-icon">
            <div>
                <div class="crypto-name">${coin.name}</div>
                <div class="crypto-symbol">${coin.symbol}</div>
            </div>
        </div>
        <div class="crypto-price">${formatPrice(coin.current_price)}</div>
        <div class="crypto-market-cap">Market Cap: ${formatMarketCap(coin.market_cap)}</div>
        <div class="crypto-changes">
            ${formatChange(coin.price_change_1h)} 1H
            ${formatChange(coin.price_change_24h)} 24H
            ${formatChange(coin.price_change_7d)} 7D
        </div>
    `;
    
    return card;
}

// Run hedge fund analysis
async function runAnalysis() {
    const tickers = tickersInput.value.trim();
    const startDate = startDateInput.value;
    const endDate = endDateInput.value;
    const initialCash = parseFloat(initialCashInput.value);
    
    if (!tickers) {
        showError('Please enter at least one ticker symbol');
        return;
    }
    
    if (!startDate || !endDate) {
        showError('Please select both start and end dates');
        return;
    }
    
    if (new Date(startDate) >= new Date(endDate)) {
        showError('Start date must be before end date');
        return;
    }
    
    if (initialCash < 1000) {
        showError('Initial cash must be at least $1,000');
        return;
    }
    
    // Show loading spinner
    loading.classList.remove('hidden');
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                tickers,
                start_date: startDate,
                end_date: endDate,
                initial_cash: initialCash
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayAnalysisResults(result);
            showSuccess('Analysis completed successfully!');
        } else {
            showError(result.error || 'Analysis failed');
        }
    } catch (error) {
        console.error('Error running analysis:', error);
        showError('Error running analysis. Please try again.');
    } finally {
        // Hide loading spinner
        loading.classList.add('hidden');
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<i class="fas fa-play"></i> Run Analysis';
    }
}

// Display analysis results
function displayAnalysisResults(result) {
    analysisResults.innerHTML = '';
    
    if (!result.decisions) {
        showError('No analysis results available');
        return;
    }
    
    const resultsContainer = document.createElement('div');
    resultsContainer.className = 'analysis-results';
    
    // Display results for each ticker
    Object.entries(result.decisions).forEach(([ticker, decision]) => {
        const tickerDiv = createTickerAnalysis(ticker, decision, result.analyst_signals);
        resultsContainer.appendChild(tickerDiv);
    });
    
    analysisResults.appendChild(resultsContainer);
}

// Create ticker analysis display
function createTickerAnalysis(ticker, decision, analystSignals) {
    const div = document.createElement('div');
    div.className = 'ticker-analysis';
    
    // Get signals for this ticker
    const signals = [];
    Object.entries(analystSignals).forEach(([agent, agentSignals]) => {
        if (agentSignals[ticker]) {
            const signal = agentSignals[ticker];
            const agentName = agent.replace('_agent', '').replace('_', ' ').title();
            signals.push({
                agent: agentName,
                signal: signal.signal,
                confidence: signal.confidence
            });
        }
    });
    
    // Create signals table
    const signalsTable = createSignalsTable(signals);
    
    // Create decision table
    const decisionTable = createDecisionTable(decision);
    
    div.innerHTML = `
        <div class="ticker-header">${ticker}</div>
        <h4>Analyst Signals</h4>
        ${signalsTable}
        <h4>Trading Decision</h4>
        ${decisionTable}
        <div class="reasoning">
            <h4>Reasoning</h4>
            <p>${decision.reasoning}</p>
        </div>
    `;
    
    return div;
}

// Create signals table
function createSignalsTable(signals) {
    let table = '<table class="signals-table"><thead><tr><th>Analyst</th><th>Signal</th><th>Confidence</th></tr></thead><tbody>';
    
    signals.forEach(signal => {
        const signalClass = `signal-${signal.signal.toLowerCase()}`;
        table += `
            <tr>
                <td>${signal.agent}</td>
                <td class="${signalClass}">${signal.signal}</td>
                <td>${signal.confidence}%</td>
            </tr>
        `;
    });
    
    table += '</tbody></table>';
    return table;
}

// Create decision table
function createDecisionTable(decision) {
    const actionClass = `action-${decision.action.toLowerCase()}`;
    
    return `
        <table class="decision-table">
            <tbody>
                <tr>
                    <td><strong>Action</strong></td>
                    <td class="${actionClass}">${decision.action}</td>
                </tr>
                <tr>
                    <td><strong>Quantity</strong></td>
                    <td>${decision.quantity}</td>
                </tr>
                <tr>
                    <td><strong>Confidence</strong></td>
                    <td>${decision.confidence.toFixed(1)}%</td>
                </tr>
            </tbody>
        </table>
    `;
}

// Helper functions
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    // Remove existing error messages
    const existingErrors = document.querySelectorAll('.error-message');
    existingErrors.forEach(error => error.remove());
    
    // Add new error message
    analysisResults.appendChild(errorDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    
    // Remove existing success messages
    const existingSuccess = document.querySelectorAll('.success-message');
    existingSuccess.forEach(success => success.remove());
    
    // Add new success message
    analysisResults.appendChild(successDiv);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

// String helper
String.prototype.title = function() {
    return this.replace(/\w\S*/g, (txt) => {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
};