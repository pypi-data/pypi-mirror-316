import argparse
import os
import requests
from dotenv import load_dotenv
import shutil
import re
from datetime import datetime, timedelta
import logging
import sys
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def setup_logging():
    """Configure logging for the script."""
    logging.basicConfig(
        level=logging.INFO,  # Change to DEBUG for more detailed logs
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("transcription_translation.log")  # Logs saved to 'transcription_translation.log'
        ]
    )

def load_api_key(secrets_dir=None):
    """
    Load the OpenAI API key from the .env file located in the secrets directory.
    If no secrets directory is provided, it will look for the .env file in the current working directory.
    """
    if secrets_dir:
        dotenv_path = os.path.join(secrets_dir, '.env')
    else:
        dotenv_path = '.env'  # Default to the current directory

    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)  # Load the .env file
        api_key = os.getenv('OPENAI_API_KEY')  # Fetch the OpenAI API key from the .env file
        if not api_key:
            logging.error("API key not found in the .env file.")
        return api_key
    else:
        logging.error(f"No .env file found at {dotenv_path}.")
        return None

def get_session_with_retries(proxy_host_ip=None, proxy_host_port=None):
    """
    Create a requests session with retry logic.
    """
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    if proxy_host_ip and proxy_host_port:
        proxy_url = f"http://{proxy_host_ip}:{proxy_host_port}"
        session.proxies.update({
            "http": proxy_url,
            "https": proxy_url
        })
        logging.info(f"Configured proxy for session: {proxy_url}")

    return session

def send_audio_to_openai(api_key, audio_file, subtitle_file, input_lang, target_lang='en', proxy_host_ip=None, proxy_host_port=None):
    """
    Send the audio file to OpenAI's /v1/audio/translations endpoint to get a translation/transcription
    in SRT format based on the provided subtitle prompt.

    Args:
        api_key (str): OpenAI API key.
        audio_file (str): Path to the audio file.
        subtitle_file (str): Path to the subtitle file.
        input_lang (str): Input language code (e.g., 'zh' for Chinese).
        target_lang (str): Target language code ('en' for English, 'zh' for Chinese).
        proxy_host_ip (str, optional): Proxy host IP address.
        proxy_host_port (str, optional): Proxy host port number.

    Returns:
        dict or None: JSON response from OpenAI API or None if failed.
    """
    # Initialize the language variables
    if input_lang == "zh":
        desired_input_lang = "Chinese Language"
    else:
        desired_input_lang = "Chinese Language"  # Assuming only Chinese is handled

    if target_lang == 'en':
        desired_target_lang = "English Language"  # Target language for translation
    elif target_lang == 'zh':
        desired_target_lang = "Chinese Language"
    else:
        desired_target_lang = f"{target_lang} Language"  # Generic for other languages

    url = "https://api.openai.com/v1/audio/translations"

    # Prepare the prompt from the subtitle text
    try:
        with open(subtitle_file, 'r', encoding='utf-8') as f:
            prompt_text = f.read()
    except FileNotFoundError:
        logging.error(f"Subtitle file not found: {subtitle_file}")
        return None

    try:
        # Open the audio file
        with open(audio_file, 'rb') as audio:
            files = {'file': audio}
            
            prompt = {
                "prompt": f"use the provided text {prompt_text} as baseline for original subtitles, and convert from {desired_input_lang} to {desired_target_lang}. The srt formatted file must only contain {desired_target_lang} and not a mix of languages."
            }

            headers = {
                "Authorization": f"Bearer {api_key}",
            }

            data = {
                'model': 'whisper-1',  # Whisper model
                'language': target_lang,  # Language to translate to
                'response_format': 'verbose_json',  # Get detailed response for segments and timestamps
                'timestamp_granularities[]': 'segment',  # Ensure segment-level timestamps
                'prompt': prompt
            }

            # Configure proxies if provided
            proxies = None
            if proxy_host_ip and proxy_host_port:
                proxy_url = f"http://{proxy_host_ip}:{proxy_host_port}"
                proxies = {
                    "http": proxy_url,
                    "https": proxy_url
                }
                logging.info(f"Using proxy: {proxy_url}")

            # Send the POST request to OpenAI API
            response = requests.post(url, headers=headers, data=data, files=files, proxies=proxies)

            if response.status_code == 200:
                return response.json()  # Return the full response as JSON to handle detailed segment data
            else:
                logging.error(f"Error: {response.status_code}, {response.text}")
                return None
    except Exception as e:
        logging.error(f"Error processing audio file: {e}")
        return None

def translate_srt(api_key, srt_content, source_lang, target_lang, proxy_host_ip=None, proxy_host_port=None):
    """
    Translate the given SRT content from source_lang to target_lang using OpenAI's Chat Completion API.

    Args:
        api_key (str): OpenAI API key.
        srt_content (str): Content of the SRT file.
        source_lang (str): Source language code (e.g., 'en').
        target_lang (str): Target language code (e.g., 'fr').
        proxy_host_ip (str, optional): Proxy host IP address.
        proxy_host_port (str, optional): Proxy host port number.

    Returns:
        str or None: Translated SRT content or None if failed.
    """
    language_map = {
        'en': "English",
        'fr': "French",
        'de': "German",
        'es': "Spanish",
        'zh': "Chinese",
        'ar': "Arabic"
    }

    # Validate source and target languages
    if source_lang not in language_map:
        logging.error(f"Unsupported source language: {source_lang}")
        return None

    if target_lang not in language_map:
        logging.error(f"Unsupported target language: {target_lang}")
        return None

    desired_target_lang = language_map[target_lang]

    # Define the messages for the Chat Completion API
    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional subtitle translator. Your task is to translate provided subtitle text "
                "into the specified target language while strictly preserving the SRT format, including timing "
                "and numbering. Do not add extra commentary or text outside the subtitle entries."
            )
        },
        {
            "role": "user",
            "content": (
                f"Please translate the following SRT subtitles from {language_map[source_lang]} into {desired_target_lang} language. "
                f"All subtitle lines must be fully translated into {desired_target_lang}, preserving the exact SRT structure "
                f"including the numbering and timestamps. The output should contain no additional explanations or formatting errors. "
                f"Only return the translated SRT file content.\n\n{srt_content}"
            )
        }
    ]

    # Set up headers for the API request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Define the payload for the API request
    payload = {
        "model": "gpt-4",  # You can change this to "gpt-3.5-turbo" if needed
        "messages": messages,
        "temperature": 0.2
    }

    # Configure proxies if provided
    proxies = None
    if proxy_host_ip and proxy_host_port:
        proxy_url = f"http://{proxy_host_ip}:{proxy_host_port}"
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }
        logging.info(f"Using proxy: {proxy_url}")

    try:
        # Send the POST request to OpenAI API with optional proxies
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            proxies=proxies,
            timeout=60  # Optional: Set a timeout for the request
        )

        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            translated_srt = result['choices'][0]['message']['content'].strip()
            return translated_srt
        else:
            logging.error(f"Error during chat completion translation: {response.status_code}, {response.text}")
            return None

    except requests.RequestException as e:
        logging.error(f"Network error during chat completion translation: {e}")
        return None

def convert_to_srt(transcription_json):
    """
    Convert the verbose JSON transcription response into SRT format.
    """
    segments = transcription_json.get('segments', [])
    if not segments:
        logging.warning("No transcription segments found.")
        return ""

    srt_output = []
    index = 1

    for segment in segments:
        try:
            start_time = segment.get('start')
            end_time = segment.get('end')
            text = segment.get('text', '').strip()

            if start_time is None or end_time is None or not text:
                logging.warning(f"Skipping incomplete segment: {segment}")
                continue

            # Format the start and end times in SRT format (HH:MM:SS,MS)
            start_str = format_time(start_time)
            end_str = format_time(end_time)

            srt_output.append(f"{index}")
            srt_output.append(f"{start_str} --> {end_str}")
            srt_output.append(text)
            srt_output.append("")  # Blank line to separate subtitles

            index += 1
        except Exception as e:
            logging.error(f"Error processing segment {segment}: {e}")
            continue

    return "\n".join(srt_output)

def format_time(seconds):
    """
    Convert seconds to SRT time format: HH:MM:SS,MS
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

def save_srt_file(srt_content, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_content)
        logging.info(f"SRT file saved: {output_path}")
    except Exception as e:
        logging.error(f"Error saving SRT file: {e}")

# Helper function to parse SRT timestamp
def parse_srt_timestamp(timestamp: str) -> timedelta:
    return datetime.strptime(timestamp, "%H:%M:%S,%f") - datetime(1900, 1, 1)

# Helper function to format timedelta to SRT timestamp format
def format_srt_timestamp(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    milliseconds = int((td.total_seconds() - total_seconds) * 1000)
    formatted_time = str(timedelta(seconds=total_seconds))
    if '.' in formatted_time:
        formatted_time = formatted_time.split('.')[0]
    return f"{formatted_time},{milliseconds:03d}"

# Estimate audio length based on word count (words per minute average 150)
def estimate_audio_length(word_count: int, wpm=150) -> timedelta:
    audio_length_minutes = word_count / wpm
    return timedelta(minutes=audio_length_minutes)

# Function to fix the start time of the first subtitle based on the audio length estimate
def fix_first_segment_start_time(srt_file_path):
    with open(srt_file_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()

    # Split the SRT content into blocks for each subtitle
    srt_blocks = srt_content.strip().split('\n\n')

    if not srt_blocks:
        logging.warning(f"No subtitle blocks found in {srt_file_path}.")
        return

    # Get the first subtitle block (index 0)
    first_segment = srt_blocks[0]
    
    # Extract the timestamp and content from the first segment
    match = re.match(r'(\d+)\n([\d:,]+) --> ([\d:,]+)\n(.+)', first_segment, re.DOTALL)
    if match:
        segment_number = match.group(1)
        start_time = match.group(2)
        end_time = match.group(3)
        text = match.group(4)

        # Count the words in the segment text (naive word count)
        word_count = len(text.split())
        
        # Estimate the audio length for the segment
        estimated_audio_length = estimate_audio_length(word_count)

        # Calculate the correct start time for the first segment
        end_time_obj = parse_srt_timestamp(end_time)
        correct_start_time = end_time_obj - estimated_audio_length

        # Format the new start time
        corrected_start_time = format_srt_timestamp(correct_start_time)

        # Replace the start time in the first segment
        updated_first_segment = first_segment.replace(start_time, corrected_start_time, 1)
        
        # Reconstruct the entire SRT content with the updated first segment
        updated_srt_content = updated_first_segment + '\n\n' + '\n\n'.join(srt_blocks[1:])

        # Write the updated content back to the SRT file
        with open(srt_file_path, 'w', encoding='utf-8') as file:
            file.write(updated_srt_content)

        logging.info(f"First segment start time corrected to: {corrected_start_time}")
    else:
        logging.error(f"Failed to parse SRT content in {srt_file_path}.")

# Existing function to process the video directory
def process_video_directory(input_dir, api_key, input_lang, target_lang, additional_langs, proxy_host_ip=None, proxy_host_port=None):
    """Process each subdirectory under the input directory, look for audio and subtitle files."""
    for root, dirs, files in os.walk(input_dir):
        # Modify 'dirs' in-place to exclude hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for dir_name in dirs:
            video_dir = os.path.join(root, dir_name)
            video_base_name = os.path.basename(video_dir)
            logging.info(f"Looking inside video directory: {video_dir}")
            
            # Find the audio and subtitle files
            subtitle_file = None
            for file in os.listdir(video_dir):
                if file.endswith("_asr_zh.txt"):
                    subtitle_file = os.path.join(video_dir, file)
            
            if subtitle_file:
                print(f"Found subtitle file: {subtitle_file}")
                
                # Step 1: Ensure only the processed vocals file is used (remove the original vocals.wav if it exists)
                vocals_processed_path = os.path.join(video_dir, f"{video_base_name}_vocals_processed.wav")
                print(vocals_processed_path)
                print(os.path.exists(vocals_processed_path))
                if os.path.exists(vocals_processed_path):
                    print(f"Found processed vocals file: {vocals_processed_path}")
                else :
                    print(f"Processed vocals file not found: {vocals_processed_path}")
                    return

                
                # Step 2: Send the audio and subtitle files to OpenAI for English SRT
                result_en = send_audio_to_openai(
                    api_key=api_key,
                    audio_file=vocals_processed_path,
                    subtitle_file=subtitle_file,
                    input_lang=input_lang,
                    target_lang='en',
                    proxy_host_ip=proxy_host_ip,
                    proxy_host_port=proxy_host_port
                )
                if result_en:
                    logging.info("English transcription and alignment complete.")
                    # Save English SRT
                    srt_content_en = convert_to_srt(result_en)
                    intermediate_srt_path_en = os.path.join(video_dir, f"{video_base_name}_srt_en.srt")
                    save_srt_file(srt_content_en, intermediate_srt_path_en)
                    fix_first_segment_start_time(intermediate_srt_path_en)
                else:
                    logging.error(f"Failed to generate English SRT for {video_dir}. Skipping translations.")
                    continue  # Skip translations if transcription failed
                
                # Prepare a list of all target languages (including additional languages)
                all_target_langs = [target_lang]
                if additional_langs:
                    all_target_langs.extend(additional_langs)
                
                # Step 3: Translate English SRT to each target language
                for lang in all_target_langs:
                    if lang == 'en':
                        # Already have English SRT
                        continue
                    # Translate English SRT to target language
                    try:
                        with open(intermediate_srt_path_en, 'r', encoding='utf-8') as f:
                            english_srt_content = f.read()
                    except Exception as e:
                        logging.error(f"Failed to read English SRT file: {e}")
                        continue

                    translated_srt = translate_srt(
                        api_key=api_key,
                        srt_content=english_srt_content,
                        source_lang='en',
                        target_lang=lang,
                        proxy_host_ip=proxy_host_ip,
                        proxy_host_port=proxy_host_port
                    )
                    if translated_srt:
                        # Save the translated SRT with the final name
                        final_srt_path = os.path.join(video_dir, f"{video_base_name}_srt_en_{lang}.srt")
                        save_srt_file(translated_srt, final_srt_path)
                        logging.info(f"Translated SRT saved at: {final_srt_path}")
                    else:
                        logging.error(f"Failed to translate English SRT into target language '{lang}' for {video_dir}.")
            else:
                logging.warning(f"Audio file or subtitle file not found in '{video_dir}'. Skipping directory.")

                    
def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(description="Audio Transcription and Translation")
    
    # Required flag: input directory
    parser.add_argument('--input-dir', required=True, help='Path to input directory containing subdirectories of video names.')
    
    # Optional flags
    parser.add_argument('--secrets-dir', help='Directory containing .env file with API key.')
    parser.add_argument('--input-lang', default='zh', help='Language of the input audio file. Default is Chinese (zh).')
    parser.add_argument('--target-lang', default='en', help='Target language for translation. Default is English (en). Other available languages: zh, es, fr, de, ar.')
    parser.add_argument('--additional-langs', nargs='*', help='Additional language(s) to generate subtitles for. e.g., --additional-langs es fr')
    
    # Flags for API keys
    parser.add_argument('--openai-api-token', help='OpenAI API key (if not using secrets-dir).')
    
    # Proxy settings
    parser.add_argument('--proxy-host-ip', help='Proxy host IP address (e.g., 192.168.1.100).')
    parser.add_argument('--proxy-host-port', help='Proxy host port number (e.g., 8080).')
    
    args = parser.parse_args()

    # Determine the API key
    api_key = None
    if args.secrets_dir:
        api_key = load_api_key(args.secrets_dir)  # Load from secrets directory
    elif args.openai_api_token:
        api_key = args.openai_api_token  # Use the token directly

    if not api_key:
        logging.error("API key not provided. Exiting.")
        sys.exit(1)
    
    # Validate proxy settings if provided
    if (args.proxy_host_ip and not args.proxy_host_port) or (args.proxy_host_port and not args.proxy_host_ip):
        logging.error("Both '--proxy-host-ip' and '--proxy-host-port' must be specified together.")
        sys.exit(1)

    # Validate the proxy host IP and port to be valid
    if args.proxy_host_ip:
        ip_pattern = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
        if not ip_pattern.match(args.proxy_host_ip):
            logging.error("Invalid proxy host IP format. It must be in dot notation (e.g., 192.168.1.1).")
            sys.exit(1)

    if args.proxy_host_port:
        if not args.proxy_host_port.isdigit() or not (0 < int(args.proxy_host_port) <= 65535):
            logging.error("Invalid proxy host port. It must be a number between 1 and 65535.")
            sys.exit(1)

    # Log proxy usage
    if args.proxy_host_ip and args.proxy_host_port:
        proxy_url = f"http://{args.proxy_host_ip}:{args.proxy_host_port}"
        logging.info(f"Using proxy: {proxy_url}")
    else:
        logging.info("No proxy settings provided. Proceeding without proxy.")

    # Process the input directory
    process_video_directory(
        input_dir=args.input_dir,
        api_key=api_key,
        input_lang=args.input_lang,
        target_lang=args.target_lang,
        additional_langs=args.additional_langs,
        proxy_host_ip=args.proxy_host_ip,
        proxy_host_port=args.proxy_host_port
    )

def check_dependencies():
    """
    Verify that all required external dependencies are installed and accessible.
    """
    # Check for FFmpeg if used elsewhere in the script
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        logging.error("FFmpeg is not installed or not found in PATH. Please install FFmpeg to proceed.")
        sys.exit(1)
    


# Ensure dependencies are checked before running main
def entry_point():
    setup_logging()
    check_dependencies()
    main()

if __name__ == "__main__":
    main()