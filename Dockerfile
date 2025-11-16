# 1. Start with the full, standard Python 3.12 image
FROM python:3.12

# 2. Install FFmpeg dependency
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# 3. Set the working directory
WORKDIR /app

# 4. CRITICAL FIX: Install known stable versions directly.
#    We are abandoning requirements.txt to force this specific version.
RUN pip install --no-cache-dir "moviepy==1.0.3" "Flask" "Pillow<10"

# 5. Copy the rest of the application code
COPY . .

# 6. Expose the port the app runs on
EXPOSE 5000

# 7. Define the command to run the application
CMD ["python3", "app.py"]
