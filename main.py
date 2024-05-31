import config
import pyrogram
from pyrogram import Client, filters
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client(
    ":subscription:",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

# Health Check Server
PORT = 8000

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

def run_health_check_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, HealthCheckHandler)
    logger.info(f"Serving health check on port {PORT}")
    httpd.serve_forever()

# Start the health check server in a separate thread
health_check_thread = threading.Thread(target=run_health_check_server)
health_check_thread.daemon = True
health_check_thread.start()

@app.on_message(filters.private | filters.group)
async def redirecter_(_, msg):
    try:
        await msg.reply("‼ IMPORTANT MSG TO ADMIN ‼")
    except pyrogram.errors.exceptions.not_acceptable_406.ChannelPrivate as e:
        logger.error(f"ChannelPrivate error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

# ------------------------------------------------------------------------------- #
logger.info("🍓🍓 Successfully deployed subscription bot")
# ------------------------------------------------------------------------------- #

# Run the bot
app.run()
