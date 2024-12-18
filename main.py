from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

def get_video_id(url):
    """
    Extracts the video ID from the YouTube URL.
    """
    import re
    youtube_url_pattern = r"(?:https?://)?(?:www\.)?(?:youtube\.com(?:/[^/]+)*/(?:watch\?v=|(?:v|e(?:mbed)?)\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(youtube_url_pattern, url)
    return match.group(1) if match else None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_transcript', methods=['POST'])
def get_transcript():
    data = request.json
    youtube_url = data.get('youtube_url')
    language_code = data.get('language_code', 'en')

    video_id = get_video_id(youtube_url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
        text_output = "\n".join([f"{entry['text']}" for entry in transcript])
        return jsonify({"transcript": text_output})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
