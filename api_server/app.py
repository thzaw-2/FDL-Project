import os
import secrets
import asyncio
from flask import Flask, request, redirect, Response
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FileIdInvalid
import mimetypes
from urllib.parse import quote, unquote

# Environment Variables
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID"))

# Initialize Pyrogram client
try:
    SmartPyro = Client(
        "SmartUtilBot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )
except Exception as e:
    print(f"Error initializing Pyrogram client: {e}")
    exit(1)

# Initialize Flask app
app = Flask(__name__)

# Function to get file details
async def get_file_details(message_id: int):
    try:
        msg = await SmartPyro.get_messages(LOG_CHANNEL_ID, message_id)
        if not msg or not msg.media:
            return None, None, None
        
        file_name = getattr(msg, 'file_name', f"file-{message_id}.mp4")
        file_size = msg.file_size
        mime_type = msg.mime_type
        
        return file_name, file_size, mime_type
    except Exception as e:
        print(f"Error getting file details: {e}")
        return None, None, None

@app.route("/dl/<int:message_id>")
async def download_file(message_id):
    try:
        # Check code
        code = request.args.get('code')
        if not code:
            return "Unauthorized", 401
        
        msg = await SmartPyro.get_messages(LOG_CHANNEL_ID, message_id)
        if not msg or not msg.caption:
            return "File not found or code missing", 404
        
        if msg.caption.strip() != code.strip():
            return "Invalid code", 403
            
        file_size = msg.media.file_size
        file_name = getattr(msg.media, 'file_name', f"file_{message_id}.mp4")
        mime_type = getattr(msg.media, 'mime_type', 'application/octet-stream')

        # Get file stream
        def generate():
            stream = SmartPyro.stream_media(msg)
            while True:
                try:
                    chunk = next(stream)
                    yield chunk
                except StopIteration:
                    break
        
        headers = {
            'Content-Type': mime_type,
            'Content-Disposition': f'attachment; filename="{quote(file_name)}"',
            'Content-Length': str(file_size)
        }
        
        return Response(generate(), headers=headers)

    except Exception as e:
        print(f"Error in download_file: {e}")
        return "Internal Server Error", 500

@app.route("/stream/<int:message_id>")
async def stream_file(message_id):
    try:
        # Check code
        code = request.args.get('code')
        if not code:
            return "Unauthorized", 401

        msg = await SmartPyro.get_messages(LOG_CHANNEL_ID, message_id)
        if not msg or not msg.caption:
            return "File not found or code missing", 404
            
        if msg.caption.strip() != code.strip():
            return "Invalid code", 403

        file_size = msg.media.file_size
        mime_type = getattr(msg.media, 'mime_type', 'video/mp4')
        
        range_header = request.headers.get('Range', None)
        
        if range_header:
            range_parts = range_header.replace('bytes=', '').split('-')
            start = int(range_parts[0])
            end = int(range_parts[1]) if len(range_parts) > 1 and range_parts[1] else file_size - 1
            
            def generate_partial():
                stream = SmartPyro.stream_media(msg, offset=start, limit=end - start + 1)
                while True:
                    try:
                        chunk = next(stream)
                        yield chunk
                    except StopIteration:
                        break

            headers = {
                'Content-Type': mime_type,
                'Content-Range': f'bytes {start}-{end}/{file_size}',
                'Content-Length': str(end - start + 1),
                'Accept-Ranges': 'bytes'
            }
            return Response(generate_partial(), status=206, headers=headers)
        else:
            def generate_full():
                stream = SmartPyro.stream_media(msg)
                while True:
                    try:
                        chunk = next(stream)
                        yield chunk
                    except StopIteration:
                        break
            
            headers = {
                'Content-Type': mime_type,
                'Content-Length': str(file_size),
                'Accept-Ranges': 'bytes'
            }
            return Response(generate_full(), headers=headers)

    except FileIdInvalid:
        return "File Not Found", 404
    except Exception as e:
        print(f"Error in stream_file: {e}")
        return "Internal Server Error", 500

async def run_pyrogram():
    async with SmartPyro:
        # app.run(host='0.0.0.0', port=os.environ.get("PORT", 5000))
        # This part is for local testing. We'll use gunicorn for production.
        pass

if __name__ == "__main__":
    asyncio.run(run_pyrogram())
