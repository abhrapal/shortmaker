# ShortMaker 🎬

ShortMaker is a simple web-based utility designed to automate the creation of short video clips. It combines a static background image with sequential segments of an audio file, making it perfect for generating content for platforms like YouTube Shorts, TikTok, or Instagram Reels from podcasts or other long-form audio.

The application is built with Python, Flask, and MoviePy, and is containerized with Docker for easy, cross-platform setup.

---

### ## ✨ Features

*   **Web-Based UI:** Easy-to-use interface to configure and generate videos.
*   **Bulk Creation:** Generate dozens of clips from a single audio file in one go.
*   **Customizable:** Set the number of clips, duration of each clip, and start offset.
*   **Dockerized:** Hassle-free setup on Windows, macOS, and Linux without worrying about dependencies like FFmpeg.

---

### ## 🚀 Getting Started (Recommended Method: Docker)

Using Docker is the simplest and most reliable way to run ShortMaker. It ensures that the application and all its dependencies work correctly regardless of your operating system.

#### ### 1. Prerequisites

*   You must have **Docker Desktop** installed and running on your system.
    *   [Download for Windows](https://www.docker.com/products/docker-desktop/)
    *   [Download for Mac](https://www.docker.com/products/docker-desktop/)
    *   [Download for Linux](https://www.docker.com/products/docker-desktop/)

#### ### 2. Setup Instructions

1.  **Clone the Repository**
    Open your terminal or command prompt and clone this project.
    ```bash
    git clone https://github.com/abhrapal/shortmaker.git
    cd shortmaker
    ```

2.  **Create Data and Output Folders**
    You need to create two folders in the project's root directory: `data` and `output`.

    *   `data/`: Place your source image (`.png`, `.jpg`) and audio (`.mp3`, `.wav`) files here.
    *   `output/`: This is where the generated video clips will be saved.

3.  **Build the Docker Image**
    Run the following command in the project's root directory to build the Docker image. This will package the application and its dependencies.
    ```bash
    docker build -t shortmaker-app .
    ```

4.  **Run the Docker Container**
    This command starts the application. The command is slightly different depending on your operating system.

    ##### **For macOS and Linux:**
    This command maps your local `data` and `output` folders to the folders inside the container.
    ```bash
    docker run -d -p 5000:5000 -v "$(pwd)/data:/app/data" -v "$(pwd)/output:/app/output" shortmaker-app
    ```

    ##### **For Windows (Command Prompt / PowerShell):**
    Windows uses a different variable (`%cd%`) to refer to the current directory.
    ```powershell
    docker run -d -p 5000:5000 -v "%cd%\data:/app/data" -v "%cd%\output:/app/output" shortmaker-app
    ```

5.  **Access the Application**
    Open your web browser and navigate to:
    **[http://localhost:5000](http://localhost:5000)**

---

### ## 🛠️ How to Use

1.  **Place Your Files:** Add at least one image and one audio file to the `data` folder.
2.  **Open the Web UI:** Go to `http://localhost:5000`. The dropdowns will automatically populate with the files from your `data` folder.
3.  **Configure Your Clips:**
    *   Select the background image and source audio file.
    *   Enter the number of clips you want to create.
    *   Set the duration (in seconds) for each clip.
    *   Optionally, set a start offset (in seconds) to skip the beginning of your audio file.
4.  **Generate:** Click the **"Create Videos"** button.
5.  **Find Your Videos:** The generated clips will appear in the `output` folder.

---

### ## 🔧 Advanced Setup (Manual Installation)

If you prefer not to use Docker, you can run the application directly. This is recommended only for development purposes.

#### ### Prerequisites

1.  **Python 3.8+**: Ensure Python and `pip` are installed and added to your system's PATH.
2.  **FFmpeg**: This is a critical dependency for video processing. You must install it and ensure it's accessible from your system's PATH.
    *   [Official FFmpeg Download Page](https://ffmpeg.org/download.html)

#### ### Instructions

1.  **Clone the repo and create `requirements.txt`** as shown in the [Wiki Installation Guide](streamdown:incomplete-link)
