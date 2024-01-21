import requests
import subprocess
import os


def process_video(reddit_url):
    
    STATIC_FOLDER = "static\\videos"
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'}
    response = requests.get(reddit_url, headers=headers)
    processed_video_path = os.path.join(STATIC_FOLDER, 'processed_video.mp4')
    

    # Define the path to the static folder where processed files will be stored
    STATIC_FOLDER = 'static/videos'

    def download_and_process_audio(audio_source, output_filename, is_hls=False):
        try:
            if is_hls:
                # Directly use FFmpeg for HLS (.m3u8) URLs
                audio_input = audio_source
            else:
                # Check if the input file exists and is not empty for local files
                if not os.path.isfile(audio_source) or os.path.getsize(audio_source) == 0:
                    print(f"Input file {audio_source} does not exist or is empty.")
                    return
                audio_input = f"file:{audio_source}"

            # Process the audio using FFmpeg and save it in the static/videos folder
            processed_audio = os.path.join(STATIC_FOLDER, 'processed_video.mp4')
            ff_command = [
                'ffmpeg', '-nostdin',
                '-i', audio_input,
                '-c:a', 'aac',             # Use AAC audio codec
                '-strict', 'experimental',
                processed_audio
            ]

            result = subprocess.run(ff_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Print FFmpeg's output (stdout and stderr)
            print(result.stdout)
            print(result.stderr)

        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    if response.status_code == 200:
        data = response.json()
        try:
            video_data = data[0]['data']['children'][0]['data']['secure_media']['reddit_video']
            video_url = video_data['fallback_url']
            dash_url = video_data['dash_url']
            hls_url = video_data['hls_url']

            # Download Video
            video_filename = os.path.join(STATIC_FOLDER, 'video.mp4')
            r_video = requests.get(video_url, stream=True)
            if r_video.status_code == 200:
                with open(video_filename, 'wb') as f:
                    for chunk in r_video.iter_content(chunk_size=1024*1024):
                        if chunk:
                            f.write(chunk)
                print(f"Video downloaded successfully: {video_filename}")
            else:
                print(f"Failed to download video. Status code: {r_video.status_code}")

            # Try getting audio from DASH format
            dash_audio_url = dash_url.replace('DASHPlaylist.mpd', 'DASH_audio.mp4')
            audio_filename = os.path.join(STATIC_FOLDER, 'audio.mp4')
            r_audio = requests.get(dash_audio_url, headers=headers)
            if r_audio.status_code == 200:
                with open(audio_filename, 'wb') as f:
                    for chunk in r_audio.iter_content(chunk_size=1024*1024):
                        if chunk:
                            f.write(chunk)
                print(f"Audio downloaded successfully: {audio_filename}")
                download_and_process_audio(audio_filename, 'processed_video.mp4')
                return {'video_path': processed_video_path}
            else:
                print(f"Failed to download audio from DASH. Status code: {r_audio.status_code}")
                print(f"Trying HLS audio: {hls_url}")
                # If DASH audio download failed, try HLS
                download_and_process_audio(hls_url, 'processed_audio_hls.mp4', is_hls=True)
                return {'video_path': processed_video_path}

        except (KeyError, IndexError) as e:
            print("Couldn't find video/audio URL in the post.")
            print(e)
    else:
        print(f"Failed to fetch post data. Status code: {response.status_code}")
        

# Example usage:
# process_reddit_video("https://www.reddit.com/r/Asmongold/comments/16pa3wu/uber_eats_robots_deployed_in_us/.json")
