from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from RedditVideoScraper import process_video  # Import the process_video function

app = Flask(__name__)
CORS(app)

@app.route('/process_video', methods=['POST'])
def process_video_route():
    content = request.json
    reddit_url = content['url']
    result = process_video(reddit_url)  # Call your process_video function
    video_path = result.get('video_path', '')  # Adjust this based on your response structure
    if video_path:
        return send_file(video_path, as_attachment=True)
    return jsonify(result)

if __name__ == '__main__':
      app.run(debug=True)