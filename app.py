import os
from flask import Flask, request, render_template
from moviepy.editor import ImageClip, AudioFileClip

UPLOAD_FOLDER = '/app/data'
OUTPUT_FOLDER = '/app/output'
# Define allowed extensions for discovery
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'm4a'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def home():
    """
    Scans the data directory and passes lists of available image
    and audio files to the template.
    """
    image_files = []
    audio_files = []
    try:
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            extension = filename.rsplit('.', 1)[1].lower()
            if extension in ALLOWED_IMAGE_EXTENSIONS:
                image_files.append(filename)
            elif extension in ALLOWED_AUDIO_EXTENSIONS:
                audio_files.append(filename)
    except FileNotFoundError:
        # This can happen if the volume mount isn't set up correctly
        pass # The template will handle the empty lists
        
    return render_template('index.html', image_files=image_files, audio_files=audio_files)

@app.route('/process', methods=['POST'])
def process_files():
    """
    Receives filenames from the form, processes them, and saves the output.
    """
    # --- Part 1: Get selected filenames and config from the form ---
    selected_image = request.form.get('selected_image')
    selected_audio = request.form.get('selected_audio')
    
    try:
        num_clips = request.form.get('num_clips', type=int)
        clip_duration = request.form.get('clip_duration', type=int)
        start_offset = request.form.get('start_offset', type=int)
    except (TypeError, ValueError):
        return "Error: Invalid configuration values. Please enter numbers.", 400

    if not all([selected_image, selected_audio, num_clips, clip_duration, start_offset is not None]):
        return "Error: Missing selections. Please choose an image, audio, and set all config values.", 400

    # --- Part 2: Construct full file paths ---
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], selected_image)
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], selected_audio)

    # --- Part 3: Core Slicing Logic ---
    output_filenames = []
    try:
        main_audio = AudioFileClip(audio_path)
        
        for i in range(num_clips):
            start_time = start_offset + (i * clip_duration)
            end_time = start_time + clip_duration
            
            if start_time >= main_audio.duration:
                break
            
            end_time = min(end_time, main_audio.duration)
            audio_subclip = main_audio.subclip(start_time, end_time)
            
            if audio_subclip.duration == 0:
                continue

            video_clip = ImageClip(image_path, duration=audio_subclip.duration)
            final_clip = video_clip.set_audio(audio_subclip)
            
            output_filename = f"{os.path.splitext(selected_image)[0]}_clip_{i+1}.mp4"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            final_clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', threads=4)
            output_filenames.append(output_filename)
            
        main_audio.close()

    except Exception as e:
        return f"An error occurred during video processing: {str(e)}", 500

    # --- Part 4: Show a simple success message ---
    return f"""
    <h2>✅ Processing Complete!</h2>
    <p>Created {len(output_filenames)} video(s). Please check the <code>output</code> folder in your project directory.</p>
    <p><a href="/">Go Back</a></p>
    """

if __name__ == '__main__':
    # We still ensure the directories exist inside the container
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
