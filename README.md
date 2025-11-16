<<<<<<< HEAD
# ShortMaker - Local Video Batch Creator

ShortMaker is a simple yet powerful web-based tool for batch-creating short video clips. It takes a single background image and a long audio file, then slices the audio into multiple segments to generate a separate video for each segment.

The entire process is managed locally on your machine using Docker, ensuring fast performance with no time wasted on file uploads or downloads.

## ✅ Key Features

*   **Local First:** Processes files directly from your local folders for maximum speed.
*   **Web-Based UI:** An easy-to-use interface to control the video creation process without touching the command line.
*   **Batch Processing:** Create dozens of clips from a single audio source in one go.
*   **Highly Configurable:** Easily set the number of clips, clip duration, and a start offset for the audio.
*   **Containerized:** Uses Docker for a one-command setup, ensuring it runs identically on any machine.
*   **User-Friendly Feedback:** A loading overlay provides clear feedback while videos are being generated.

## ⚙️ How It Works

The application uses a "web-based controller" pattern:
1.  You place your source media files (one image, one audio) into a local `data` directory.
2.  You run the application inside a Docker container.
3.  The web interface automatically detects your files and displays them in dropdown menus.
4.  You configure your desired output (e.g., "create 10 clips of 60 seconds each") and submit.
5.  The backend script processes the files and saves the resulting `.mp4` videos directly to your local `output` directory.

---

## 🚀 Getting Started

Follow these instructions to get the ShortMaker application running on your local machine.

### Prerequisites

You must have **Docker** installed on your system.
*   [Install Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Prepare Your Media Files**
    This is the most important step. Place the image and audio files you want to use inside the `data` folder. For example:
    ```
    shortmaker-project/
    ├── data/
    │   ├── background.png
    │   └── long_podcast.mp3
    │   └── .gitkeep
    └── ...
    ```

3.  **Build the Docker Image**
    This command builds the application environment inside a self-contained image. You only need to do this once.
    ```bash
    docker build -t shortmaker-app .
    ```

4.  **Run the Docker Container**
    This command starts the application and connects your local `data` and `output` folders to the container.
    ```bash
    docker run --rm -p 5001:5000 \
      -v "$(pwd)/data:/app/data" \
      -v "$(pwd)/output:/app/output" \
      shortmaker-app
    ```
    *   `--rm`: Automatically removes the container when you stop it.
    *   `-p 5001:5000`: Maps port 5001 on your machine to port 5000 inside the container.
    *   `-v`: Mounts your local folders into the container, allowing the app to read from `data` and write to `output`.

You're all set! The server is now running.

---

## 🖥️ Usage

1.  **Open Your Browser**
    Navigate to `http://localhost:5001`.

2.  **Configure Your Job**
    *   The web page will automatically show the image and audio files it found in your `data` folder. Select the ones you want to use.
    *   Set the "Number of Clips," "Clip Duration," and "Start Offset" to your desired values.

3.  **Create Videos**
    *   Click the "Create Videos" button.
    *   A loading overlay will appear while the backend processes your files. This may take some time depending on the number and length of the clips.

4.  **Find Your Output**
    *   Once the process is complete, a success message will appear.
    *   Check the `output` folder in your project directory. All your newly created video files will be there!

### Stopping the Application

To stop the container, go to your terminal window where the app is running and press `Ctrl + C`.

---

## 📁 Project Structure

```
.
├── data/                 # Your source image and audio files go here
│   └── .gitkeep
├── output/               # Generated videos will appear here
│   └── .gitkeep
├── templates/
│   └── index.html        # The HTML front-end
├── app.py                # The main Flask application and processing logic
├── Dockerfile            # Instructions for building the Docker image
├── .gitignore            # Tells Git which files to ignore
└── README.md             # This documentation file
```
=======
# shortmaker
It takes an audio input and image and creates YouTube Shorts
>>>>>>> dcdd462dd66d4d9878dfb8b0458a4d57b464262a
