import os
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from moviepy.editor import ImageClip, AudioFileClip
import math

# --- PART 1: The Video Generation Logic (No changes needed here) ---
def create_multiple_shorts(image_path, audio_path, output_dir, clip_duration, num_clips, start_offset, video_width, video_height, status_callback):
    """
    Slices a long audio file and creates short videos with specific dimensions.
    """
    try:
        # (The core video creation logic remains the same as the previous version)
        if not all([image_path, audio_path, output_dir]):
            status_callback("Error: All paths (image, audio, output) must be selected.")
            return

        status_callback("Loading the main audio file...")
        main_audio = AudioFileClip(audio_path)
        
        if main_audio.duration < start_offset + 1:
            status_callback(f"Error: Audio is shorter ({main_audio.duration:.0f}s) than the offset ({start_offset}s).")
            return

        for i in range(num_clips):
            clip_num = i + 1
            start_time = start_offset + (i * clip_duration)
            end_time = start_time + clip_duration

            if start_time >= main_audio.duration:
                status_callback(f"Reached end of audio. Process finished after {i} clips.")
                break

            status_callback(f"Processing clip {clip_num}/{num_clips}...")
            
            end_time = min(end_time, main_audio.duration)
            audio_subclip = main_audio.subclip(start_time, end_time)

            image_clip = ImageClip(image_path, duration=audio_subclip.duration)
            image_clip = image_clip.resize(newsize=(video_width, video_height))
            
            final_clip = image_clip.set_audio(audio_subclip)

            output_filename = os.path.join(output_dir, f"short_video_{clip_num}.mp4")
            final_clip.write_videofile(output_filename, codec='libx264', audio_codec='aac', fps=24, logger=None)

        status_callback(f"Success! All videos created in '{output_dir}'.")

    except Exception as e:
        status_callback(f"An error occurred: {e}")


# --- PART 2: The GUI Application Class ---

class VideoGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Short Video Generator")
        
        frame = tk.Frame(root, padx=15, pady=15)
        frame.pack(padx=10, pady=10)

        # File and Folder Selection
        tk.Label(frame, text="Image File:").grid(row=0, column=0, sticky="w", pady=2)
        self.image_path = tk.Entry(frame, width=50)
        self.image_path.grid(row=0, column=1, padx=5, columnspan=2)
        tk.Button(frame, text="Browse...", command=self.select_image_file).grid(row=0, column=3)
        # ... (rest of file selection is the same)
        tk.Label(frame, text="Audio File:").grid(row=1, column=0, sticky="w", pady=2)
        self.audio_path = tk.Entry(frame, width=50)
        self.audio_path.grid(row=1, column=1, padx=5, columnspan=2)
        tk.Button(frame, text="Browse...", command=self.select_audio_file).grid(row=1, column=3)
        tk.Label(frame, text="Output Folder:").grid(row=2, column=0, sticky="w", pady=2)
        self.output_dir = tk.Entry(frame, width=50)
        self.output_dir.grid(row=2, column=1, padx=5, columnspan=2)
        tk.Button(frame, text="Browse...", command=self.select_output_folder).grid(row=2, column=3)

        # Video Dimension Fields
        tk.Label(frame, text="Video Width:").grid(row=3, column=0, sticky="w", pady=5)
        self.video_width = tk.Entry(frame, width=10)
        self.video_width.insert(0, "1080")
        self.video_width.grid(row=3, column=1, sticky="w", padx=5)
        tk.Label(frame, text="Video Height:").grid(row=4, column=0, sticky="w", pady=2)
        self.video_height = tk.Entry(frame, width=10)
        self.video_height.insert(0, "1920")
        self.video_height.grid(row=4, column=1, sticky="w", padx=5)
        
        # Other Parameters
        tk.Label(frame, text="Start Offset (s):").grid(row=5, column=0, sticky="w", pady=2)
        self.start_offset = tk.Entry(frame, width=10)
        self.start_offset.insert(0, "120")
        self.start_offset.grid(row=5, column=1, sticky="w", padx=5)
        tk.Label(frame, text="Clip Duration (s):").grid(row=6, column=0, sticky="w", pady=2)
        self.clip_duration = tk.Entry(frame, width=10)
        self.clip_duration.insert(0, "60")
        self.clip_duration.grid(row=6, column=1, sticky="w", padx=5)

        # --- NEW: Number of Clips with Calculate Button ---
        tk.Label(frame, text="Number of Clips:").grid(row=7, column=0, sticky="w", pady=2)
        self.num_clips = tk.Entry(frame, width=10)
        self.num_clips.insert(0, "4")
        self.num_clips.grid(row=7, column=1, sticky="w", padx=5)
        # This is the new button!
        tk.Button(frame, text="Calculate Max", command=self.calculate_max_clips).grid(row=7, column=2)

        # --- Generate Button & Status ---
        self.generate_button = tk.Button(frame, text="Generate Videos", command=self.start_processing_thread, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
        self.generate_button.grid(row=8, column=1, columnspan=2, pady=20, sticky="ew")
        self.status_label = tk.Label(frame, text="Ready. Select files and set dimensions.", wraplength=450)
        self.status_label.grid(row=9, column=0, columnspan=4, pady=5)

    # --- NEW: Function to Calculate Maximum Clips ---
    def calculate_max_clips(self):
        try:
            audio_file = self.audio_path.get()
            if not audio_file or not os.path.exists(audio_file):
                messagebox.showerror("Error", "Please select a valid audio file first.")
                return

            offset = int(self.start_offset.get())
            duration = int(self.clip_duration.get())

            if duration <= 0:
                messagebox.showerror("Error", "Clip duration must be a positive number.")
                return

            self.update_status("Calculating... Loading audio file.")
            main_audio = AudioFileClip(audio_file)
            
            usable_duration = main_audio.duration - offset
            if usable_duration < 0:
                usable_duration = 0
            
            # Use math.floor or integer division // to get the number of FULL clips
            max_clips = math.floor(usable_duration / duration)
            
            # Update the text box with the calculated number
            self.num_clips.delete(0, tk.END)
            self.num_clips.insert(0, str(max_clips))
            
            self.update_status(f"Calculated: A maximum of {max_clips} full clips can be made.")

        except ValueError:
            messagebox.showerror("Input Error", "Start Offset and Clip Duration must be valid numbers.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not calculate: {e}")

    # --- (The rest of the class methods are unchanged) ---
    def select_image_file(self):
        path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if path: self.image_path.delete(0, tk.END); self.image_path.insert(0, path)

    def select_audio_file(self):
        path = filedialog.askopenfilename(title="Select an Audio File", filetypes=[("Audio Files", "*.mp3 *.wav *.m4a")])
        if path: self.audio_path.delete(0, tk.END); self.audio_path.insert(0, path)

    def select_output_folder(self):
        path = filedialog.askdirectory(title="Select Output Folder")
        if path: self.output_dir.delete(0, tk.END); self.output_dir.insert(0, path)

    def update_status(self, message):
        self.root.after(0, self.status_label.config, {'text': message})

    def start_processing_thread(self):
        thread = threading.Thread(target=self.process_videos)
        thread.daemon = True
        thread.start()

    def process_videos(self):
        self.generate_button.config(state="disabled", text="Processing...")
        try:
            params = {
                "image_path": self.image_path.get(), "audio_path": self.audio_path.get(),
                "output_dir": self.output_dir.get(), "start_offset": int(self.start_offset.get()),
                "clip_duration": int(self.clip_duration.get()), "num_clips": int(self.num_clips.get()),
                "video_width": int(self.video_width.get()), "video_height": int(self.video_height.get()),
                "status_callback": self.update_status
            }
            create_multiple_shorts(**params)
        except ValueError:
            messagebox.showerror("Input Error", "Please ensure all numeric fields contain valid numbers.")
            self.update_status("Error: Invalid number in one of the fields.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        finally:
            self.generate_button.config(state="normal", text="Generate Videos")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoGeneratorApp(root)
    root.mainloop()
