import os
import shutil
from flask import Flask, render_template, request, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from utils import get_funny_message
import hashlib
from replit import db

# Setup logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"

# Setup rate limiting
limiter = Limiter(app=app,
                  key_func=get_remote_address,
                  default_limits=["200 per day", "50 per hour"])


def get_real_ip():
    """Get the real IP address even when behind a proxy"""
    if request.headers.get('CF-Connecting-IP'):  # Cloudflare
        return request.headers.get('CF-Connecting-IP')
    elif request.headers.get('X-Forwarded-For'):  # Standard proxy
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):  # Nginx proxy
        return request.headers.get('X-Real-IP')
    return request.remote_addr


def initialize_db():
    """Initialize the database if it doesn't exist"""
    if 'victims' not in db:
        db['victims'] = {}
    if 'counter' not in db:
        db['counter'] = 0


def get_victim_number(request_info):
    initialize_db()

    unique_id = f"{request_info.get('ip')}_{request_info.get('user_agent')}"
    identifier_hash = hashlib.sha256(unique_id.encode()).hexdigest()

    app.logger.debug(f"Unique ID (before hash): {unique_id}")
    app.logger.debug(f"Hash generated: {identifier_hash}")

    if identifier_hash in db['victims']:
        victim_number = db['victims'][identifier_hash]
        app.logger.debug(f"Returning existing victim number: {victim_number}")
        return victim_number, db['counter'], False

    db['counter'] += 1
    db['victims'][identifier_hash] = db['counter']

    app.logger.debug(f"Created new victim number: {db['counter']}")
    return db['counter'], db['counter'], True


def generate_script():
    funny_message = get_funny_message()
    protocol = 'https' if request.is_secure else 'http'

    request_info = {
        'ip': get_real_ip(),
        'user_agent': request.headers.get('User-Agent', 'unknown'),
    }

    app.logger.debug(f"Install request info: {request_info}")

    victim_number, total_victims, is_new = get_victim_number(request_info)

    with open('troll.sh', 'r') as f:
        script_content = f.read()

    script_content = script_content.replace('%FUNNY_MESSAGE%', funny_message)
    script_content = script_content.replace('%PROTOCOL%', protocol)
    script_content = script_content.replace('%HOST%', request.host)
    script_content = script_content.replace('%VICTIM_NUMBER%',
                                            str(victim_number))
    script_content = script_content.replace('%TOTAL_VICTIMS%',
                                            str(total_victims))
    script_content = script_content.replace('%IS_NEW_VICTIM%',
                                            'true' if is_new else 'false')

    return script_content


# Special routes for static files
@app.route('/static/<path:path>')
def send_static(path):
    return app.send_static_file(path)


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


# Wildcard route to handle all other paths
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@limiter.limit("30 per minute")
def catch_all(path):
    app.logger.debug(f"Request headers: {dict(request.headers)}")
    app.logger.debug(f"Real IP: {get_real_ip()}")
    app.logger.debug(f"Requested path: {path}")

    # Check if it's a curl request
    if 'curl' in request.headers.get('User-Agent', '').lower():
        response = Response(generate_script(), mimetype='text/plain')
        response.headers['Content-Type'] = 'text/plain; charset=utf-8'
        return response

    # Regular web browser request
    initialize_db()
    return render_template('index.html',
                           host=request.host,
                           victim_count=db['counter'])
