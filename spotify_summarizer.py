import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_transcript_api import YouTubeTranscriptApi
import urllib.request
import speech_recognition as sr
from transformers import pipeline
import time
from translate import Translator
import soundfile as sf

spotify_client_id = '67d84df62a7b44d1bbacfe8274c4792a'
spotify_client_secret = 'a8543c6dfaed457ebb7300be03bae439'

spotify_client_credentials_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
spotify_sp = spotipy.Spotify(client_credentials_manager=spotify_client_credentials_manager)

def summarize_audio_from_spotify(track_url, language):
    # Get track information
    track_info = spotify_sp.track(track_url)
    track_name = track_info['name']
    track_artist = track_info['artists'][0]['name']

    # Get preview URL
    preview_url = track_info['preview_url']
    print(f"Preview URL: {preview_url}")

    # Download audio from Spotify if preview URL is available
    if preview_url is not None:
        urllib.request.urlretrieve(preview_url, "audio.m4a")
    else:
        print("No preview URL available for the track.")
        return

    # Convert audio to WAV format using soundfile
    data, samplerate = sf.read("audio.m4a")
    sf.write("audio.wav", data, samplerate)

    # Initialize SpeechRecognition recognizer with PocketSphinx engine
    r = sr.Recognizer()
    r.energy_threshold = 4000

    # Load audio file
    audio_file = sr.AudioFile("audio.wav")

    # Transcribe audio using PocketSphinx
    with audio_file as source:
        audio = r.record(source)

    # Generate transcript
    transcript = r.recognize_sphinx(audio)

    # Print track information and transcript
    print(f"Track: {track_name} by {track_artist}")
    print("Transcript:")
    print(transcript)

    # Initialize the summary pipeline
    summarizer = pipeline('summarization')

    # Summarize the text
    summarized_text = summarizer(transcript, max_length=200, min_length=50, do_sample=False)

    # Print the summary
    print("Summary:")
    print(summarized_text[0]['summary_text'])

