import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

class GoogleCalendarHandler:
    """Google Calendar 處理器（無資料庫版本）"""
    
    def __init__(self, config, db_handler=None):
        self.config = config
        self.db_handler = db_handler  # 可以是 None
        self.service = None
        self.calendar_id = config.google_calendar_id
        
        try:
            if hasattr(config, 'service_account_file'):
                scope = ['https://www.googleapis.com/auth/calendar']
                creds = Credentials.from_service_account_file(
                    config.service_account_file, 
                    scopes=scope
                )
                self.service = build('calendar', 'v3', credentials=creds)
                logging.info("✅ Google Calendar 處理器初始化成功（無資料庫模式）")
            else:
                logging.warning("⚠️ Google Calendar 服務帳戶檔案未找到")
                
        except Exception as e:
            logging.error(f"Google Calendar 初始化失敗: {e}")
            self.service = None
    
    def get_events(self, max_results=10):
        """取得行事曆事件"""
        if not self.service or not self.calendar_id:
            return "Google Calendar 功能未設定。"
        
        try:
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            if not events:
                return "目前沒有行事曆事件。"
            
            message = "📅 近期行事曆事件：\n\n"
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                message += f"• {event['summary']}\n"
                message += f"  時間: {start}\n\n"
            
            return message.strip()
            
        except Exception as e:
            logging.error(f"取得 Google Calendar 事件錯誤: {e}")
            return f"取得行事曆事件時發生錯誤: {e}"