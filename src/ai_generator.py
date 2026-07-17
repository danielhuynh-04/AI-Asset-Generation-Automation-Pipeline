"""
ai_generator.py — AI Asset Generation Module
Dispatcher: Gemini Imagen 3 (primary) → Pollinations.ai (fallback, free, no key)
Prompt optimization via Gemini Pro text before generation.
"""
import os
import io
import time
import logging
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OUTPUT_DIR     = os.getenv("OUTPUT_DIR", "outputs")

# --- Pollinations config ---
POLLINATIONS_BASE = "https://image.pollinations.ai/prompt"
POLLINATIONS_AUDIO_BASE = "https://text.pollinations.ai"


def _optimize_prompt_with_llm(description: str, style_context: str = "") -> str:
    """
    Dùng LLM (Gemini Pro hoặc ChatGPT qua Pollinations) để tối ưu hóa prompt trước khi generate ảnh.
    Nếu Gemini API lỗi/hết quota → fallback ngay lập tức sang ChatGPT.
    """
    system_prompt = (
        f"You are a professional game asset prompt engineer. "
        f"Style: {style_context if style_context else 'semi-realistic cartoon game art, vibrant colors'}. "
        f"Transform this asset description into an optimized image generation prompt under 50 words. "
        f"Description: {description} "
        f"Return ONLY the optimized prompt, no explanation."
    )

    # 1. Thử dùng Gemini nếu có key
    if GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model_genai = genai.GenerativeModel("gemini-2.0-flash")
            response = model_genai.generate_content(system_prompt)
            optimized = response.text.strip()
            logger.info(f"[PROMPT_OPT] Gemini Optimized: {optimized[:80]}...")
            return optimized
        except Exception as e:
            logger.warning(f"[PROMPT_OPT] Gemini failed ({e}), falling back to ChatGPT (Pollinations)")

    # 2. Fallback sang ChatGPT (thông qua Pollinations Text API hoàn toàn miễn phí)
    try:
        encoded_prompt = urllib.parse.quote(system_prompt)
        url = f"{POLLINATIONS_AUDIO_BASE}/{encoded_prompt}?model=openai"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            optimized = response.read().decode('utf-8').strip()
            logger.info(f"[PROMPT_OPT] ChatGPT Optimized: {optimized[:80]}...")
            return optimized
    except Exception as e2:
        logger.warning(f"[PROMPT_OPT] ChatGPT falied ({e2}), using original description.")
        return description


def _generate_with_gemini_imagen(prompt: str, output_path: str) -> str:
    """
    Tạo ảnh bằng Gemini Imagen 3.
    Trả về đường dẫn file đã lưu.
    """
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)

    # Imagen 3 via Gemini API
    client = genai.ImageGenerationModel("imagen-3.0-generate-002")
    result = client.generate_images(
        prompt=prompt,
        number_of_images=1,
        aspect_ratio="1:1",  # Square cho game assets
        safety_filter_level="block_few",
    )
    image_data = result.images[0]._image_bytes
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(image_data)
    return output_path


def _generate_with_pollinations(prompt: str, output_path: str, width: int = 1024, height: int = 1024) -> str:
    """
    Tạo ảnh bằng Pollinations.ai — hoàn toàn miễn phí, không cần API key.
    URL format: https://image.pollinations.ai/prompt/{encoded_prompt}?width=W&height=H&nologo=true
    """
    encoded = urllib.parse.quote(prompt)
    url = f"{POLLINATIONS_BASE}/{encoded}?width={width}&height={height}&nologo=true&model=flux"
    logger.info(f"[POLLINATIONS] Calling: {url[:80]}...")
    # Timeout 60s vì model cần thời gian render
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    )
    with urllib.request.urlopen(req, timeout=60) as response, open(output_path, "wb") as out_file:
        out_file.write(response.read())
    return output_path


def _generate_audio_gtts(text: str, output_path: str, lang: str = "en") -> str:
    """Tạo file MP3 từ text bằng gTTS (Google Text-to-Speech) — miễn phí."""
    from gtts import gTTS
    tts = gTTS(text=text, lang=lang, slow=False)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    tts.save(output_path)
    logger.info(f"[TTS] Audio saved: {output_path}")
    return output_path


def generate_asset(
    description: str,
    model: str,
    output_format: str,
    output_path: str,
    optimize_prompt: bool = True,
    style_context: str = "",
) -> dict:
    """
    Main generation function.

    Args:
        description: Mô tả asset từ Google Sheet
        model: 'Gemini' | 'Pollinations'
        output_format: 'PNG' | 'JPG' | 'GIF' | 'MP3'
        output_path: đường dẫn file output
        optimize_prompt: dùng Gemini text để tối ưu prompt trước khi generate
        style_context: context về art style để guide prompt optimizer

    Returns:
        dict: {output_path, prompt_used, model_used, duration_ms}
    """
    start_time = time.time()

    # --- MOCK TIMEOUT cho Test Case ---
    if "MOCK_TIMEOUT" in description:
        logger.error(f"[MOCK] Giả lập API Timeout cho yêu cầu: {description[:30]}...")
        time.sleep(1) # delay giả lập
        raise TimeoutError("Simulated API Timeout for testing purposes.")

    # --- MP3 path ---
    if output_format == "MP3":
        path = _generate_audio_gtts(description, output_path)
        return {
            "output_path": path,
            "prompt_used": description,
            "model_used": "gTTS",
            "duration_ms": int((time.time() - start_time) * 1000),
        }

    # --- Optimize prompt (applies to all image models) ---
    prompt = _optimize_prompt_with_llm(description, style_context) if optimize_prompt else description

    # --- Image generation ---
    if model == "Gemini" and GEMINI_API_KEY:
        try:
            path = _generate_with_gemini_imagen(prompt, output_path)
            model_used = "Gemini-Imagen3"
        except Exception as e:
            logger.warning(f"[GENERATOR] Gemini Imagen failed ({e}), falling back to Pollinations")
            path = _generate_with_pollinations(prompt, output_path)
            model_used = "Pollinations-fallback"
    else:
        path = _generate_with_pollinations(prompt, output_path)
        model_used = "Pollinations"

    return {
        "output_path": path,
        "prompt_used": prompt,
        "model_used": model_used,
        "duration_ms": int((time.time() - start_time) * 1000),
    }
