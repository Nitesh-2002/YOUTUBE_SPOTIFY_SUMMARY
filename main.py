from spotify_summarizer import summarize_audio_from_spotify
from youtube_summarizer import summarize_video_from_youtube

# Prompt user for input
link = input("Enter the YouTube video or Spotify track link: ")
language = print("This model takes only english language link: ")

# Check if it's a YouTube video link or Spotify track link
if "youtube.com/watch?v=" in link:
    summarize_video_from_youtube(link, language)
elif "open.spotify.com/track/" in link:
    summarize_audio_from_spotify(link, language)
else:
    print("Invalid link format.")
