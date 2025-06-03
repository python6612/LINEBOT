import logging
import gspread
from google.oauth2.service_account import Credentials

class GoogleSheetsHandler:
    """Google Sheets 處理器"""
    
    def __init__(self, config):
        self.config = config
        self.client = None
        self.sheets_id = config.google_sheets_id
        
        try:
            if hasattr(config, 'service_account_file'):
                # 使用服務帳戶認證
                scope = [
                    'https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive'
                ]
                
                creds = Credentials.from_service_account_file(
                    config.service_account_file, 
                    scopes=scope
                )
                self.client = gspread.authorize(creds)
                logging.info("✅ Google Sheets 處理器初始化成功")
            else:
                logging.warning("⚠️ Google Sheets 服務帳戶檔案未找到")
                
        except Exception as e:
            logging.error(f"Google Sheets 初始化失敗: {e}")
            self.client = None
    
    def read_sheet_data(self, sheet_name="工作表1"):
        """讀取工作表資料"""
        if not self.client or not self.sheets_id:
            return "Google Sheets 功能未設定。"
        
        try:
            sheet = self.client.open_by_key(self.sheets_id)
            worksheet = sheet.worksheet(sheet_name)
            data = worksheet.get_all_records()
            
            return f"成功讀取 {len(data)} 筆資料"
            
        except Exception as e:
            logging.error(f"讀取 Google Sheets 錯誤: {e}")
            return f"讀取工作表時發生錯誤: {e}"
    
    def write_sheet_data(self, data, sheet_name="工作表1"):
        """寫入工作表資料"""
        if not self.client or not self.sheets_id:
            return "Google Sheets 功能未設定。"
        
        try:
            sheet = self.client.open_by_key(self.sheets_id)
            worksheet = sheet.worksheet(sheet_name)
            
            # 簡單的資料寫入
            worksheet.append_row(data)
            
            return "資料寫入成功"
            
        except Exception as e:
            logging.error(f"寫入 Google Sheets 錯誤: {e}")
            return f"寫入工作表時發生錯誤: {e}"