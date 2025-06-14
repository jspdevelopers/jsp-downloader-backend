from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # ⭐ Allow cross-origin requests

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'forcejson': True,
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            video = next((f for f in formats if f.get('ext') == 'mp4' and f.get('url')), None)

            return jsonify({
                'title': info.get('title'),
                'video_url': video['url'] if video else None
            })
    except Exception as e:
        print("ERROR:", e)
        return jsonify({'error': str(e)}), 500
