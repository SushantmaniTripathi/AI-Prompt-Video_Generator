import os, re, subprocess, tempfile, traceback, uuid
from datetime import datetime
from pathlib import Path
from typing import List

from flask import Flask, request, jsonify, send_from_directory, abort, Response
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core import exceptions

from manim_generator import generate_manim_code

try:
    from gtts import gTTS
    from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
except ImportError as e:
    raise RuntimeError(
        "gTTS or moviepy missing. Install once with:\n"
        "    pip install gTTS moviepy\n"
        f"Original error: {e}"
    )

# ──────────────────────────────
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_KEY:
    raise RuntimeError("Set your GEMINI_API_KEY in the environment or .env file.")

genai.configure(api_key=GEMINI_KEY)
g_model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = (
    "You are a Python/Manim narration assistant. When the user gives a topic, "
    "reply with exactly 8 lines. Each line must use [text:] [color:] [effect:] "
    "[position:] [size:]."
)

VIDEOS_DIR = Path("saved_videos")
VIDEOS_DIR.mkdir(exist_ok=True)

def _extract_sentences(script: str) -> List[str]:
    return [
        m.group(1).strip()
        for ln in script.splitlines()
        for m in [re.search(r"\[text\s*:(.*?)\]", ln, re.I)]
        if m
    ][:8]

# ──────────────────────────────
app = Flask(__name__)

# Serve index.html (frontend)
@app.get("/")
def frontend():
    return send_from_directory(directory=".", path="index.html")

# Health check
@app.get("/ping")
def health() -> str:
    return "VocaVisio AI backend online ✅"

# Video generation endpoint
@app.post("/generate")
def generate_video() -> Response:
    data = request.get_json(silent=True) or {}
    topic = (data.get("topic") or "").strip()

    if not topic:
        return jsonify({"error": "Missing JSON body field 'topic'"}), 400

    job_id = uuid.uuid4().hex[:10]
    scene_name = f"Scene_{job_id}"

    try:
        gemini_prompt = f"{SYSTEM_PROMPT}\n\nTopic: {topic}"
        gem_resp = g_model.generate_content(
            [gemini_prompt], generation_config={"temperature": 0.7}
        )
        clean_lines = [ln.strip() for ln in gem_resp.text.splitlines() if ln.strip()][:8]
        if len(clean_lines) < 8:
            return jsonify({"error": "Gemini returned fewer than 8 lines."}), 500

        script_text = "\n".join(clean_lines)
        scene_py = Path(f"generated_scene_{job_id}.py")
        scene_py.write_text(generate_manim_code(scene_name, script_text), encoding="utf-8")

        subprocess.run(
            ["manim", "-pql", str(scene_py), scene_name],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        manim_mp4 = Path(f"media/videos/{scene_py.stem}/480p15/{scene_name}.mp4")
        if not manim_mp4.exists():
            return jsonify({"error": "Manim did not produce an MP4."}), 500

        tts_clips = []
        for sentence in _extract_sentences(script_text):
            tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            gTTS(sentence, lang="en").save(tmp_mp3.name)
            tts_clips.append(AudioFileClip(tmp_mp3.name))

        with VideoFileClip(str(manim_mp4)) as vid:
            seg = vid.duration / 8.0
            placed = [
                clip.set_start(i * seg).set_end(i * seg + clip.duration)
                for i, clip in enumerate(tts_clips)
            ]
            final_vid = vid.set_audio(CompositeAudioClip(placed))

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_file = VIDEOS_DIR / f"vocavision_{timestamp}_{job_id}.mp4"
            final_vid.write_videofile(
                str(out_file), codec="libx264", audio_codec="aac",
                fps=15, logger=None
            )

        for c in tts_clips:
            try:
                Path(c.filename).unlink(missing_ok=True)
            except Exception:
                pass
            c.close()

        return send_from_directory(
            directory=VIDEOS_DIR,
            path=out_file.name,
            as_attachment=True,
            mimetype="video/mp4"
        )

    except exceptions.GoogleAPIError as e:
        return jsonify({"error": "Gemini API error", "detail": str(e)}), 502
    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "Manim render failed",
            "detail": e.stderr.decode() if e.stderr else str(e)
        }), 500
    except Exception as e:
        return jsonify({
            "error": "Unexpected server error",
            "detail": "".join(traceback.format_exception(e))
        }), 500
    finally:
        try:
            scene_py.unlink(missing_ok=True)
        except Exception:
            pass

# Direct video downloads
@app.get("/videos/<path:filename>")
def download_video(filename: str):
    safe_path = VIDEOS_DIR / filename
    if not safe_path.exists():
        abort(404)
    return send_from_directory(VIDEOS_DIR, filename, as_attachment=True)

# ──────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

