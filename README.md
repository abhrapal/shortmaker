# ShortMaker 🎬

ShortMaker is a simple web-based utility designed to automate the creation of short video clips. It combines a static background image with sequential segments of an audio file, making it perfect for generating content for platforms like YouTube Shorts, TikTok, or Instagram Reels from podcasts or other long-form audio.

The application is built with Python, Flask, and MoviePy, and is containerized with Docker for easy, cross-platform setup.

---

### ## ✨ Features

*   **Web-Based UI:** Easy-to-use interface to configure and generate videos.
*   **Bulk Creation:** Generate dozens of clips from a single audio file in one go.
*   **Customizable:** Set the number of clips, duration of each clip, and start offset.
*   **Dockerized:** Hassle-free setup on Windows, macOS, and Linux without worrying about dependencies.

---

### ## 📂 Project Structure

When you clone the repository, you will have the following structure. Understanding the role of each folder is key to using the application correctly.

```
shortmaker/
├── 📄 app.py               # The main Flask application logic.
├── 📄 Dockerfile           # Instructions for building the Docker image.
├── 📁 templates/           # Contains the HTML for the web interface.
│   └── 📄 index.html
├── 📁 data/                # (You create this) Place your input media here.
└── 📁 output/              # (You create this) Generated videos are saved here.
```
*   **`templates/`**: This folder is a core part of the application and comes with the repository. It holds the `index.html` file that creates the web user interface.
*   **`data/` & `output/`**: These folders are the only ones you need to create manually. They are used to pass files to and from the Docker container.

---

### ## 🤔 Why Docker is Recommended

While a manual setup is possible, using **Docker is strongly recommended** to ensure the application works perfectly without complex configuration. Here's why:

1.  **Solving "Dependency Hell"**: The `moviepy` library depends on a tool called **FFmpeg**, which can be difficult to install correctly. Furthermore, this project relies on specific versions of Python libraries that might conflict with other projects on your machine.
2.  **A Perfect, Isolated Environment**: The `Dockerfile` in this repository is a recipe that builds a clean, self-contained Linux environment. It automatically installs the correct version of Python, FFmpeg, and all necessary Python libraries.
3.  **Consistency Across Machines**: Because the application runs inside this container, it behaves identically on Windows, macOS, and Linux. It completely eliminates "it works on my machine" problems.

#### ### A Note on Docker: Build vs. Run

You might notice that the `docker run` command only mentions the `data` and `output` folders. **This is intentional.**

*   The application's source code (like `app.py` and the `templates` folder) is copied **into the image** during the `docker build` step. It becomes a permanent part of the application.
*   The `docker run` command's volume flags (`-v`) are used only for **dynamic data**—the input files you provide (`data`) and the video files the application creates (`output`).

By using Docker, you skip all the frustrating setup and get straight to using the application.

---

### ## 🚀 Getting Started (Recommended Method: Docker)

Using Docker is the simplest and most reliable way to run ShortMaker.

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
    Create the two required folders in the project's root directory: `data` and `output`.
    *   `data/`: Place your source image (`.png`, `.jpg`) and audio (`.mp3`, `.wav`) files here.
    *   `output/`: This is where the generated video clips will be saved.

3.  **Build the Docker Image**
    Run the following command in the project's root directory to build the Docker image.
    ```bash
    docker build -t shortmaker-app .
    ```

4.  **Run the Docker Container**
    This command starts the application. The command is slightly different depending on your operating system.

    ##### **For macOS and Linux:**
    ```bash
    docker run -d -p 5000:5000 -v "$(pwd)/data:/app/data" -v "$(pwd)/output:/app/output" shortmaker-app
    ```

    ##### **For Windows (Command Prompt / PowerShell):**
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

### ## 📚 Wiki

For more detailed information on technical architecture, troubleshooting, and advanced usage, please visit the **[Project Wiki](https://github.com/abhrapal/shortmaker/wiki)**.
