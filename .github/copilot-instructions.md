<!-- Copilot / AI agent instructions for ShortMaker project -->
# ShortMaker — AI assistant guidance

Purpose: Quickly orient an AI coding assistant to be productive in this repository.

 - **Big picture:** This repo provides a simple GUI tool to slice a long audio file into short videos using a static image per short:
   - `gui_video_maker.py` — a `tkinter` GUI that collects paths and parameters and runs the canonical `create_multiple_shorts` implementation in a background thread.

 - **Core function to change or reuse:** `create_multiple_shorts(...)` in `gui_video_maker.py` is the trusted implementation. Keep the function signature compatible with the GUI:
   `create_multiple_shorts(image_path, audio_path, output_dir, clip_duration, num_clips, start_offset, video_width, video_height, status_callback)`
   - `status_callback(msg)` is used by the GUI to surface progress and should be a thread-safe updater (the GUI uses `root.after`).

- **Key implementation patterns to follow** (discoverable in code):
  - Output filenames: `short_video_{n}.mp4` (1-indexed). Keep this naming scheme unless a clear reason to change.
  - MoviePy options: `write_videofile(..., codec='libx264', audio_codec='aac', fps=24)`. GUI calls set `logger=None` to avoid console spam.
  - Safety checks: the code verifies `main_audio.duration` against `start_offset` and avoids starting a clip past the audio end. Preserve these checks when refactoring.
  - GUI concurrency: `tkinter` code spawns a `threading.Thread` to run processing; keep this approach to avoid blocking the UI.

- **Environment & tooling (how to run / debug)**
  - Python deps: `moviepy` (and its transitive dependencies). Ensure `ffmpeg` is installed and on PATH.
   - Install commands (macOS zsh):
     ```bash
     python3 -m pip install --user -r requirements.txt
     brew install ffmpeg
     ```
   - Run GUI: `python3 gui_video_maker.py` and use the file dialogs.

- **Project-specific conventions**
  - User-visible messages use `print()` (CLI) or `status_callback()` (GUI) rather than a project-wide logging framework.
  - Input validation is defensive — prefer returning early with a clear message rather than throwing unhandled exceptions (GUI wraps calls in try/except and shows messageboxes).
  - Keep MoviePy operations synchronous inside the worker thread — avoid spawning additional processes unless necessary.

- **Integration points & external dependencies**
  - `moviepy.editor` for `ImageClip` and `AudioFileClip` — audio slicing and video composition are performed in-memory and written with ffmpeg. The GUI also uses `ImageClip.resize(newsize=(width,height))` before attaching audio.
  - `tkinter` for simple GUI; no other GUI frameworks are present.

- **When editing code** — concrete examples
  - If you modify `create_multiple_shorts` to accept a `logger` or return structured results, keep a thin adaptor for the GUI that maps `status_callback` to that interface.
  - If changing output naming, update `gui_video_maker.py` so the UI and code produce consistent filenames (current pattern: `short_video_{n}.mp4`).
  - If improving progress feedback, update the GUI `status_label` usage and avoid calling Tk widgets from worker threads — always use the provided `status_callback`.

- **Model preference (project-level instruction):** Enable Claude Haiku 4.5 for all clients — prefer Claude Haiku 4.5 for code completion, suggestions, and automated edits when available.

If anything above is unclear or you want additional coverage (unit tests, packaging, CI steps), tell me which area to expand and I will update this file.
