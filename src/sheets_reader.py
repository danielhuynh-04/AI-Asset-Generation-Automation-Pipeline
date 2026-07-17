"""
sheets_reader.py — Google Sheets ingestion module
Đọc job requests từ Google Sheet qua service account, chuẩn bị rows cho pipeline.
"""
import os
import logging
from typing import Optional
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

EXPECTED_COLUMNS = ["id", "description", "example_url", "output_format", "model", "status"]


def _get_client() -> gspread.Client:
    """Khởi tạo gspread client từ service account JSON."""
    creds_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "credentials.json")
    if not os.path.exists(creds_path):
        raise FileNotFoundError(
            f"Service account file not found: {creds_path}. "
            "Please follow setup guide in README.md (Bước 0.3)"
        )
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    return gspread.authorize(creds)


def read_pending_rows(
    sheet_id: Optional[str] = None,
    sheet_name: Optional[str] = None,
    skip_done: bool = True,
) -> list[dict]:
    """
    Đọc tất cả rows từ Google Sheet.

    Args:
        sheet_id: Google Sheet ID (mặc định từ .env)
        sheet_name: Tên tab (mặc định từ .env)
        skip_done: Bỏ qua rows có status=DONE (idempotency)

    Returns:
        list[dict] — mỗi dict là 1 row với keys từ header row
    """
    sheet_id = sheet_id or os.getenv("GOOGLE_SHEET_ID")

    if not sheet_id:
        raise ValueError("GOOGLE_SHEET_ID not configured. Check .env file.")

    client = _get_client()
    spreadsheet = client.open_by_key(sheet_id)
    # Luôn lấy sheet đầu tiên (index 0) thay vì dựa vào tên cứng "Sheet1" hay "Trang tính 1"
    worksheet = spreadsheet.get_worksheet(0)

    all_records = worksheet.get_all_records()  # list[dict] từ header row

    if not all_records:
        logger.info("[SHEETS] No rows found in sheet.")
        return []

    # Validate columns
    if all_records:
        missing_cols = [c for c in EXPECTED_COLUMNS if c not in all_records[0]]
        if missing_cols:
            logger.warning(f"[SHEETS] Missing expected columns: {missing_cols}")

    # Thêm row_index (1-based, bỏ header) để có thể ghi lại status
    result = []
    for i, row in enumerate(all_records, start=2):  # row 2 = first data row
        if skip_done and str(row.get("status", "")).upper() == "DONE":
            logger.debug(f"[SHEETS] Skipping row {i} — already DONE")
            continue
        row["_row_index"] = i
        result.append(row)

    logger.info(f"[SHEETS] Read {len(result)} pending rows from sheet")
    return result


def update_row_status(
    sheet_id: str,
    row_index: int,
    status: str,
    sheet_name: Optional[str] = None,
):
    """Ghi lại status vào cột 'status' của row tương ứng trong Sheet."""
    client = _get_client()
    spreadsheet = client.open_by_key(sheet_id)
    worksheet = spreadsheet.get_worksheet(0)

    # Tìm column index của 'status'
    header = worksheet.row_values(1)
    if "status" not in header:
        logger.error("[SHEETS] 'status' column not found — cannot update")
        return
    col_index = header.index("status") + 1  # gspread dùng 1-based

    worksheet.update_cell(row_index, col_index, status)
    logger.info(f"[SHEETS] Row {row_index} status updated to '{status}'")
