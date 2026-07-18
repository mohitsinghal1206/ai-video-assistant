# import yt_dlp
# from pydub import AudioSegment
# import os


# DOWNLOAD_DIR='downloads'
# os.makedirs(DOWNLOAD_DIR,exist_ok=True)

# def download_youtube_audio(url:str)->str:
#     output_path=os.path.join(DOWNLOAD_DIR,"%(title)s.%(ext)s")
#     ydl_opts={
#         "format":"bestaudio/best",
#         "outtmpl":output_path,
#         "postprocessors":[
#             {
#                 "key":"FFmpegExtractAudio",
#                 "preferredcodec":"wav",
#                 "preferredquality":"192",
#             }
#         ],
#         "quiet":True,
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info=ydl.extract_info(url,download=True)
#         filename=ydl.prepare_filename(info).replace(".webm",".wav").replace(".m4a",".wav")
#     return filename

# # print(download_youtube_audio("https://www.youtube.com/watch?v=7HSSR1n8dgc"))
# # data=download_youtube_audio("https://www.youtube.com/watch?v=tplWXd_T7YQ")



# def convert_to_wav(input_path:str)->str:
#     """Convert any audio/video file to WAV format using pydub"""
#     output_path=os.path.splitext(input_path)[0]+"_converted.wav"
#     audio=AudioSegment.from_file(input_path)
#     audio=audio.set_channels(1).set_frame_rate(16000) #16KHz
#     audio.export(output_path,format="wav")
#     return output_path



# def chunk_audio(wav_path:str,chunk_minutes:int=10)->list:
#     audio=AudioSegment.from_wav(wav_path)
#     chunk_ms=chunk_minutes*60*1000
    
#     chunks=[]
    
#     for i, start in enumerate(range(0,len(audio),chunk_ms)):
#         chunk=audio[start:start+chunk_ms]
#         chunk_path=f"{wav_path}_chunk_{i}.wav"
#         chunk.export(chunk_path,format='wav')
        
#         chunks.append(chunk_path)
#     return chunks

# def process_input(source:str)->list:
#     if source.startswith("https://") or source.startswith("https://"):
#         print("Detected Youtube URL. Downloading audio...")
#         wav_path=download_youtube_audio(source)
#     else:
#         print("Detected local file.Connecting to WAV...")
#         wav_path=convert_to_wav(source)
        
#     print("Chunking audio...")
#     chunks=chunk_audio(wav_path)
#     print(f"Audio ready-{len(chunks)} chunk(s) created.")
#     return chunks






import os
import yt_dlp
from pydub import AudioSegment


DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s")

    # ydl_opts = {
    #     "format": "bestaudio/best",
    #     "outtmpl": output_path,
    #     "noplaylist": True,
    #     "quiet": False,
    #     "js_runtimes": {
    #         "node": {}
    #     },
    #     "remote_components": {
    #         "ejs:github"
    #     },
    #     "postprocessors": [
    #         {
    #             "key": "FFmpegExtractAudio",
    #             "preferredcodec": "wav",
    #             "preferredquality": "192",
    #         }
    #     ],
    # }
    
    ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": output_path,
    "noplaylist": True,
    "quiet": True,
    "extractor_args": {
        "youtube": {
            "player_client": ["android", "web"]
        }
    },
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }
    ],
}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        original_filename = ydl.prepare_filename(info)
        filename = os.path.splitext(original_filename)[0] + ".wav"

    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"yt-dlp completed but WAV file was not found: {filename}"
        )

    return filename


def convert_to_wav(input_path: str) -> str:
    """Convert an audio/video file to mono 16 kHz WAV."""

    output_path = os.path.splitext(input_path)[0] + "_converted.wav"

    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")

    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000

    chunks = []

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start:start + chunk_ms]

        base = os.path.splitext(wav_path)[0]
        chunk_path = f"{base}_chunk_{i}.wav"

        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks


def process_input(source: str) -> list:
    if source.startswith(("https://", "http://")):
        print("Detected URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)

    print(f"Audio ready - {len(chunks)} chunk(s) created.")

    return chunks