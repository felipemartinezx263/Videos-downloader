import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url') if data else None
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    ydl_opts = {'format': 'best', 'quiet': True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'status': 'success',
                'title': info.get('title'),
                'download_url': info.get('url')
            })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    # Render assigns dynamic ports via environment variables
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
