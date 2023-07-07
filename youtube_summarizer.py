from youtube_transcript_api import YouTubeTranscriptApi
import subprocess
from transformers import pipeline
import time

def summarize_video_from_youtube(video_link, language):
    if "youtube.com/watch?v=" not in video_link:
        print("Invalid YouTube video link!")
        return

    # Extract video ID from the YouTube link
    video_id = video_link.split("=")[1]

    # Get the transcript of the YouTube video
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Combine the transcript into a single string
    result = ""
    for i in transcript:
        result += ' ' + i['text']

    # Initialize the summary pipeline
    summarizer = pipeline('summarization')

    # Measure the inference time
    start_time = time.time()

    # Summarize the text
    num_iters = int(len(result) / 1000)
    summarized_text = []
    for i in range(num_iters + 1):
        start = i * 1000
        end = (i + 1) * 1000
        input_text = result[start:end]
        out = summarizer(input_text)
        out = out[0]
        out = out['summary_text']
        summarized_text.append(out)

    end_time = time.time()

    # Calculate the inference time
    inference_time = end_time - start_time

    # Save the summarized text in a TXT file
    txt_filename = "transcript.txt"
    with open(txt_filename, 'w') as txt_file:
        for text in summarized_text:
            txt_file.write(text + '\n')

    # Print the summarized text, transcript, and inference time
    print("Transcript:")
    for i in transcript:
        print(i['text'])

    print("Summarized text:")
    for text in summarized_text:
        print(text)
