from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_video_stream():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
        'extractaudio': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict['url']

            return jsonify({'stream_url': video_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
