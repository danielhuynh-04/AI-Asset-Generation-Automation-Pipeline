"""
drive_uploader.py — Google Drive upload module
Upload assets với structured folder: Outputs/{date}/{format}/{job_id}_{filename}
"""
import os
import logging
from datetime import date
from pathlib import Path
from typing import Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive"]


def _get_drive_service():
    """Lấy Service qua OAuth 2.0 thay vì Service Account để tránh lỗi Quota 0 byte."""
    creds = None
    # Token lưu trong file token.json sau khi login lần đầu
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        
    # Nếu token hỏng hoặc chưa có, yêu cầu login qua trình duyệt
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_secret_path = os.getenv("GOOGLE_OAUTH_CLIENT_JSON", "client_secret.json")
            if not os.path.exists(client_secret_path):
                raise FileNotFoundError(
                    f"Không tìm thấy file {client_secret_path}. "
                    "Hãy tạo OAuth 2.0 Client ID trên Google Cloud Console, download file JSON, "
                    f"và đặt tên là {client_secret_path} trong thư mục gốc."
                )
            
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Lưu token lại cho những lần sau
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())

    return build("drive", "v3", credentials=creds)


def _get_or_create_folder(service, name: str, parent_id: Optional[str] = None) -> str:
    """Tìm folder theo tên trong parent, tạo mới nếu chưa có."""
    query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    results = service.files().list(
        q=query, fields="files(id,name)",
        includeItemsFromAllDrives=True, supportsAllDrives=True
    ).execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]
    # Tạo folder mới
    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id] if parent_id else [],
    }
    folder = service.files().create(
        body=metadata, fields="id", supportsAllDrives=True
    ).execute()
    return folder["id"]


def upload_asset(
    local_path: str,
    job_id: int,
    output_format: str,
    root_folder_id: Optional[str] = None,
) -> str:
    """
    Upload file lên Google Drive với cấu trúc:
    Root → Outputs → {YYYY-MM-DD} → {format} → file

    Returns:
        Shareable URL (view link)
    """
    root_folder_id = root_folder_id or os.getenv("GOOGLE_DRIVE_FOLDER_ID")
    service = _get_drive_service()

    # Tạo cấu trúc thư mục
    today_str  = date.today().isoformat()
    outputs_id = _get_or_create_folder(service, "Outputs", root_folder_id)
    date_id    = _get_or_create_folder(service, today_str, outputs_id)
    format_id  = _get_or_create_folder(service, output_format.upper(), date_id)

    # Upload file
    filename = f"job_{job_id:04d}_{Path(local_path).name}"
    ext = output_format.lower()
    mime_map = {
        "png": "image/png", "jpg": "image/jpeg",
        "gif": "image/gif", "mp3": "audio/mpeg",
    }
    mime_type = mime_map.get(ext, "application/octet-stream")

    file_metadata = {"name": filename, "parents": [format_id]}
    media = MediaFileUpload(local_path, mimetype=mime_type)
    uploaded = service.files().create(
        body=file_metadata, media_body=media, fields="id", supportsAllDrives=True
    ).execute()
    file_id = uploaded["id"]

    # Public read permission
    service.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"},
        supportsAllDrives=True,
    ).execute()

    url = f"https://drive.google.com/file/d/{file_id}/view"
    logger.info(f"[DRIVE] Uploaded job {job_id}: {url}")
    return url
