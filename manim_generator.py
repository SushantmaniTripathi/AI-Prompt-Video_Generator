# manim_generator.py – upgraded for better layout and longer scripts
import re

# ─────────────────────────────────────────────────────────────
# 1. Colour tables
# ─────────────────────────────────────────────────────────────
MANIM_COLORS = {
    "white", "black", "red", "green", "blue", "yellow",
    "orange", "purple", "pink", "gray", "teal", "gold", "maroon",
}

CUSTOM_COLOR_HEX = {
    "lightblue":  "#ADD8E6", "darkblue": "#00008B",
    "lightgreen": "#90EE90", "darkgreen": "#006400",
    "brown":      "#A52A2A", "violet":   "#EE82EE",
    "cyan":       "#00FFFF", "lime":     "#00FF00",
    "navy":       "#000080", "darkgray": "#A9A9A9",
}

# ─────────────────────────────────────────────────────────────
# 2. Helpers
# ─────────────────────────────────────────────────────────────
def _parse_chunks(line: str) -> dict:
    props = {
        "text": "", "color": "white", "effect": "fade_in",
        "position": "center", "size": "medium",
    }
    for chunk in re.findall(r"\[(.*?)\]", line):
        if ":" in chunk:
            k, v = chunk.split(":", 1)
            props[k.strip().lower()] = v.strip()
    return props

def _font_size(sz: str) -> int:
    return {
        "smaller": 24, "small": 28, "medium": 36,
        "large":   48, "larger": 56,
    }.get(sz.lower(), 36)

def _effect_to_anim(effect: str, obj: str) -> list[str]:
    e = effect.lower()
    fade = f"FadeIn({obj})"
    tbl = {
        "fade_in":  [fade],
        "fade_out": [fade, f"FadeOut({obj})"],
        "grow":     [f"GrowFromCenter({obj})"],
        "zoom_in":  [fade, f"ScaleInPlace({obj},1.4)"],
        "zoom_out": [fade, f"ScaleInPlace({obj},0.6)"],
        "flash":    [fade, f"Flash({obj})"],
        "shake":    [fade, f"Wiggle({obj})"],
        "wiggle":   [fade, f"Wiggle({obj})"],
        "bounce":   [fade, f"ApplyMethod({obj}.shift,UP*0.4,rate_func=there_and_back)"],
        "appear":   [fade],
        "write":    [f"Write({obj})"],
        "slide_in": [fade, f"ApplyMethod({obj}.shift, LEFT*2, run_time=1.5)"],
        "slide":    [fade, f"ApplyMethod({obj}.shift, LEFT*2, run_time=1.5)"],
        "fall":     [fade, f"ApplyMethod({obj}.shift,DOWN*1.5,run_time=2)"],
        "move":     [fade, f"ApplyMethod({obj}.shift,UP*1,run_time=2)"],
        "flow":     [fade, f"ApplyMethod({obj}.shift,RIGHT*1.5,run_time=2)"],
        "spiral":   [fade, f"ApplyMethod({obj}.shift,(LEFT+UP)*1,run_time=2)"],
        "pop":      [f"GrowFromCenter({obj})"],
        "expand":   [f"GrowFromCenter({obj})"],
    }
    return tbl.get(e, [fade])

def _center_vec(pos: str) -> str:
    return {
        "top": "UP*2", "bottom": "DOWN*2", "left": "LEFT*3",
        "right": "RIGHT*3", "topleft": "UP*2 + LEFT*3",
        "topright": "UP*2 + RIGHT*3", "bottomleft": "DOWN*2 + LEFT*3",
        "bottomright": "DOWN*2 + RIGHT*3",
    }.get(pos.lower(), "ORIGIN")

def _tts_matched_wait(words: int) -> float:
    secs = words * 0.42 + 0.3
    return max(1.0, min(round(secs, 2), 6.0))

# ─────────────────────────────────────────────────────────────
# 3. Main generator
# ─────────────────────────────────────────────────────────────
def generate_manim_code(scene_name: str, raw_script: str) -> str:
    lines = [ln for ln in raw_script.strip().splitlines() if ln.strip()]
    out: list[str] = [
        "from manim import *\n",
        f"class {scene_name}(Scene):",
        "    def construct(self):",
        "        last_obj = None",
    ]
    for idx, line in enumerate(lines, 1):
        p = _parse_chunks(line)
        text = p["text"].strip()
        if not text:
            continue
        obj = f"txt_{idx}"
        col_key = p["color"].lower()
        color_expr = (
            f'"{col_key}"'
            if col_key in MANIM_COLORS
            else f'ManimColor("{CUSTOM_COLOR_HEX.get(col_key, "#FFFFFF")}")'
        )
        escaped = text.replace('"', r'\"')
        out += [
            "        if last_obj: self.remove(last_obj)",
            f"        {obj} = Text(\"{escaped}\", "
            f"color={color_expr}, font_size={_font_size(p['size'])}, line_spacing=1.2"
            f").scale(0.9).set_width(11).move_to({_center_vec(p['position'])})",
        ]
        for anim in _effect_to_anim(p["effect"], obj):
            out.append(f"        self.play({anim})")
        out += [
            f"        self.wait({_tts_matched_wait(len(text.split()))})",
            f"        last_obj = {obj}",
            "",
        ]
    return "\n".join(out)
