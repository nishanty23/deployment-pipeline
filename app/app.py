from flask import Flask, jsonify, request
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': os.getenv('APP_VERSION', '1.0.0')
    })

@app.route('/')
def home():
    return jsonify({
        'message': 'Flask Deployment Pipeline Demo',
        'environment': os.getenv('FLASK_ENV', 'production'),
        'version': os.getenv('APP_VERSION', '1.0.0')
    })

@app.route('/api/data')
def get_data():
    return jsonify({
        'data': [1, 2, 3, 4, 5],
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
