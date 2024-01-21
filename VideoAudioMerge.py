import subprocess

subprocess.run([
    'ffmpeg',
    '-i', 'video.mp4',
    '-i', 'audio.mp4',
    '-c:v', 'copy',
    '-c:a', 'aac',
    '-strict', 'experimental',
    'output.mp4'
])