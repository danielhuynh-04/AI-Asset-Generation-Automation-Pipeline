import os
import shutil

src_dir = "e:/AI Asset Generation Automation Pipeline"
dst_dir = "e:/AI Asset Generation Automation Pipeline/LeThanhHaiHuynh_Test_Submit"

print(f"Starting packaging process to: {dst_dir}")

# Create directories
dirs_to_create = [
    "automation/src",
    "automation/docs",
    "automation/tests",
    "prompt_engineering/iterations",
    "database",
    "report_sample",
]
for d in dirs_to_create:
    path = os.path.join(dst_dir, d)
    os.makedirs(path, exist_ok=True)
    print(f"Created directory: {path}")

# Helper for copy
def copy_file(src, dst):
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied {os.path.basename(src)}")
    else:
        print(f"WARNING: File not found {src}")

# Copy automation folders
try:
    shutil.copytree(os.path.join(src_dir, "src"), os.path.join(dst_dir, "automation", "src"), dirs_exist_ok=True)
    shutil.copytree(os.path.join(src_dir, "docs"), os.path.join(dst_dir, "automation", "docs"), dirs_exist_ok=True)
    shutil.copytree(os.path.join(src_dir, "tests"), os.path.join(dst_dir, "automation", "tests"), dirs_exist_ok=True)
except Exception as e:
    print(f"Error copying folders: {e}")

# Copy automation files
copy_file(os.path.join(src_dir, ".env.example"), os.path.join(dst_dir, "automation", ".env.example"))
copy_file(os.path.join(src_dir, "requirements.txt"), os.path.join(dst_dir, "automation", "requirements.txt"))
copy_file(os.path.join(src_dir, "README.md"), os.path.join(dst_dir, "automation", "README.md"))

# Copy prompt engineering
copy_file(os.path.join(src_dir, "prompt_engineering", "prompt_engineering_report.md"), os.path.join(dst_dir, "prompt_engineering", "prompt_engineering_report.md"))
try:
    shutil.copytree(os.path.join(src_dir, "prompt_engineering", "iterations"), os.path.join(dst_dir, "prompt_engineering", "iterations"), dirs_exist_ok=True)
except Exception as e:
    print(f"Error copying iterations: {e}")

# Copy database
copy_file(os.path.join(src_dir, "database", "schema.sql"), os.path.join(dst_dir, "database", "schema.sql"))

# Copy README to root
copy_file(os.path.join(src_dir, "README.md"), os.path.join(dst_dir, "README.md"))

# Copy Video Script
copy_file(os.path.join(src_dir, "SCRIPT_CHI_TIET_TIENG_VIET.md"), os.path.join(dst_dir, "SCRIPT_CHI_TIET_TIENG_VIET.md"))
copy_file(os.path.join(src_dir, "SCRIPT_DETAILED_ENGLISH.md"), os.path.join(dst_dir, "SCRIPT_DETAILED_ENGLISH.md"))

# Create video link txt
with open(os.path.join(dst_dir, "video_link.txt"), "w", encoding="utf-8") as f:
    f.write("Xin chào Ban tuyển dụng Athena Studio,\n\nLink Video Present bài làm (dưới 10 phút):\nhttps://... (Ứng viên sẽ paste link Youtube/Google Drive vào đây)\n")
print("Created video_link.txt")

print("Packaging completed successfully!")
