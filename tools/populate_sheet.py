import os
import sys

# Thêm src vào sys.path để import các module local
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import sheets_reader
from dotenv import load_dotenv

load_dotenv()

PROMPTS = [
    # 1. Characters (PNG)
    [101, "A cute cheerful chubby animal mascot, semi-realistic cartoon game art, smooth cel-shading, soft ambient light, centered, front-facing, transparent background, high detail", "", "PNG", "Gemini", "PENDING"],
    [102, "A brave mighty warrior knight character, semi-realistic cartoon game art, smooth cel-shading, epic inner glow, centered, front-facing, transparent background, high detail", "", "PNG", "Gemini", "PENDING"],
    [103, "A wise magical wizard character with staff, semi-realistic cartoon game art, smooth cel-shading, mystical purple glow, centered, front-facing, transparent background, high detail", "", "PNG", "Pollinations", "PENDING"],
    
    # 2. Bingo Balls (PNG)
    [104, "A shiny glossy green 3D Bingo sphere, semi-realistic cartoon game art, smooth cel-shading, Monochromatic Colorway, transparent background, high detail", "", "PNG", "Gemini", "PENDING"],
    [105, "A shiny glossy orange 3D Bingo sphere, semi-realistic cartoon game art, smooth cel-shading, Monochromatic Colorway, transparent background, high detail", "", "PNG", "Pollinations", "PENDING"],
    [106, "A shiny glossy purple 3D Bingo sphere, semi-realistic cartoon game art, smooth cel-shading, Monochromatic Colorway, transparent background, high detail", "", "PNG", "Gemini", "PENDING"],

    # 3. UI Buttons (PNG)
    [107, "A glossy vibrant green 2D game Spin button, gold border frame, semi-realistic cartoon game art, straight-on, transparent background, high detail", "", "PNG", "Pollinations", "PENDING"],
    [108, "A glossy vibrant cyan 2D game Back button, gold border frame, semi-realistic cartoon game art, straight-on, transparent background, high detail", "", "PNG", "Gemini", "PENDING"],
    # Row 9: bẫy MOCK_TIMEOUT để kiểm tra Retry Mechanism
    [109, "A glossy vibrant red 2D game Play button, MOCK_TIMEOUT, gold border frame, semi-realistic cartoon game art, straight-on, transparent background", "", "PNG", "Gemini", "PENDING"],

    # 4. Wooden Backgrounds / Frames (JPG)
    [110, "A wooden game card frame, semi-realistic cartoon game art, deep brown color, smooth cel-shading, straight-on, high detail", "", "JPG", "Pollinations", "PENDING"],
    [111, "A wooden table texture background, semi-realistic cartoon game art, deep brown color, warm ambient lighting, top-down view, high detail", "", "JPG", "Gemini", "PENDING"],
    [112, "A theatrical game stage scene background, deep purple and gold palette, semi-realistic cartoon game art, dramatic lighting, high detail", "", "JPG", "Gemini", "PENDING"],

    # 5. Audio Edge Cases (MP3) & Invalid Format (WEBP)
    [113, "Catchy happy background music full of energy for a casual bingo game loop", "", "MP3", "Gemini", "PENDING"],
    [114, "A magical sparkling sound effect, short and crisp for a game UI button click", "", "MP3", "Gemini", "PENDING"],
    # Row 15: bẫy Invalid Format để kiểm tra Validator
    [115, "A glossy vibrant yellow 2D game victory badge, semi-realistic cartoon game art, gold border, straight-on, transparent background", "", "WEBP", "Pollinations", "PENDING"]
]

def populate_sheet():
    print("🚀 Connecting to Google Sheets...")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not sheet_id:
        print("❌ Lỗi: Không tìm thấy GOOGLE_SHEET_ID trong file .env")
        return
        
    client = sheets_reader._get_client()
    spreadsheet = client.open_by_key(sheet_id)
    worksheet = spreadsheet.get_worksheet(0)
    
    print(f"✅ Connected to Sheet ID: {sheet_id}")
    print("📝 Appending 15 highly-optimized Assignment 2 Prompt rows...")
    
    # Append the rows
    worksheet.append_rows(PROMPTS, value_input_option='USER_ENTERED')
    
    print("🎉 Thành công! 15 dòng dữ liệu test đã được dội hoàn hảo vào Google Sheet của bạn.")
    print("👉 Hãy mở Google Sheet ra kiểm tra, rồi chạy `python src/main.py` để chứng kiến sức mạnh hệ thống nhé!")

if __name__ == "__main__":
    populate_sheet()
