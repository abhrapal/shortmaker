import os
from moviepy.editor import ImageClip, AudioFileClip

def create_multiple_shorts(image_path, audio_path, clip_duration, num_clips, start_offset):
    """
    Slices a long audio file into multiple segments and creates a short video for each,
    with an optional offset to skip the beginning of the audio.
    """
    # --- Step 1: Validate input files ---
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found at {audio_path}")
        return

    print("Loading the main audio file...")
    main_audio = AudioFileClip(audio_path)
    
    # --- NEW DEBUGGING MESSAGES ---
    print(f"\n[DEBUG] Audio file duration: {main_audio.duration:.2f} seconds.")
    print(f"[DEBUG] Requested start offset: {start_offset:.2f} seconds.")
    print(f"[DEBUG] Requested clip duration: {clip_duration:.2f} seconds.")
    print(f"[DEBUG] Requested number of clips: {num_clips}.")
    
    # Safety check: ensure audio is long enough for the offset + one clip
    if main_audio.duration < start_offset + 1:
        # This is a likely reason for the script stopping.
        print(f"\n[STOP] Error: The audio file's total duration ({main_audio.duration:.2f}s) is shorter than the start offset ({start_offset}s).")
        print("[STOP] Cannot create any clips. Exiting.")
        return

    # --- Step 2: Loop to create the specified number of videos ---
    for i in range(num_clips):
        clip_num = i + 1
        print(f"\n--- Starting process for Short Video #{clip_num} ---")

        # --- Step 3: Calculate start and end times, including the offset ---
        start_time = start_offset + (i * clip_duration)
        end_time = start_time + clip_duration
        
        # --- NEW DEBUGGING MESSAGE ---
        print(f"[DEBUG] Calculating times for clip #{clip_num}: Start = {start_time:.2f}s, End = {end_time:.2f}s")
        
        # Safety check: Stop if the start time is beyond the audio's length
        if start_time >= main_audio.duration:
            # This is the other likely reason for the script stopping.
            print(f"[STOP] The calculated start time ({start_time:.2f}s) is past the end of the audio ({main_audio.duration:.2f}s).")
            print("[STOP] No more clips will be created. Exiting loop.")
            break
            
        end_time = min(end_time, main_audio.duration)

        print(f"Slicing audio from {start_time:.2f}s to {end_time:.2f}s")
        audio_subclip = main_audio.subclip(start_time, end_time)

        # --- Step 4: Create the video clip for this chunk ---
        image_clip = ImageClip(image_path, duration=audio_subclip.duration)
        final_clip = image_clip.set_audio(audio_subclip)

        # --- Step 5: Write the final video file ---
        output_filename = f"short_video_{clip_num}.mp4"
        print(f"Writing video file to {output_filename}...")
        final_clip.write_videofile(output_filename, codec='libx264', audio_codec='aac', fps=24)
        print(f"--- Successfully created {output_filename} ---")

    print("\nAll tasks complete!")


if __name__ == '__main__':
    # --- CONFIGURATION ---
    IMAGE_FILE = 'my_image.png'
    AUDIO_FILE = 'my_audio.mp3'
    START_OFFSET_SECONDS = 120 # 2 minutes
    CLIP_DURATION_SECONDS = 60
    NUM_VIDEOS_TO_CREATE = 4

    create_multiple_shorts(
        image_path=IMAGE_FILE,
        audio_path=AUDIO_FILE,
        clip_duration=CLIP_DURATION_SECONDS,
        num_clips=NUM_VIDEOS_TO_CREATE,
        start_offset=START_OFFSET_SECONDS
    )
