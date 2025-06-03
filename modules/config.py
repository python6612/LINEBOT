import os
import logging
import json
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler

class Config:
    """設定管理類別（無 MySQL 版本）"""
    def __init__(self):
        # 加載環境變數
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        load_dotenv(dotenv_path=dotenv_path)

        self.line_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
        self.line_secret = os.getenv("LINE_CHANNEL_SECRET")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.google_search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.weather_api_key = os.getenv("WEATHER_API_KEY")
        self.news_api_key = os.getenv("NEWS_API")
        
        # 移除 MySQL 相關設定
        # self.mysql_host = os.getenv("MYSQL_HOST")
        # self.mysql_user = os.getenv("MYSQL_USER")
        # self.mysql_password = os.getenv("MYSQL_PASSWORD")
        # self.mysql_database = os.getenv("MYSQL_DATABASE")
        
        self.google_sheets_id = os.getenv("GOOGLE_SHEETS_ID")
        self.google_calendar_id = os.getenv("GOOGLE_CALENDAR_ID")
        
        # 處理 Google Service Account (支援環境變數或檔案)
        self.google_service_account_key = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY")
        self.service_account_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'service_account.json')
        
        # 如果有環境變數形式的 service account key，將其寫入檔案
        if self.google_service_account_key:
            try:
                # 嘗試解析 JSON 字串
                service_account_data = json.loads(self.google_service_account_key)
                with open(self.service_account_file, 'w') as f:
                    json.dump(service_account_data, f)
                logging.info("✅ Google Service Account 金鑰已從環境變數載入")
            except json.JSONDecodeError:
                logging.warning("⚠️ GOOGLE_SERVICE_ACCOUNT_KEY 不是有效的 JSON 格式")

        # 初始化 LINE Bot API
        if self.line_access_token and self.line_secret:
            self.line_bot_api = LineBotApi(self.line_access_token)
            self.handler = WebhookHandler(self.line_secret)
        else:
            self.line_bot_api = None
            self.handler = None

        # 驗證配置
        if not self.line_access_token or not self.line_secret or not self.gemini_api_key:
            logging.error("請確保環境變數中設定了 LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET 和 GEMINI_API_KEY。")
        
        if not self.google_search_engine_id:
            logging.warning("未設定 GOOGLE_SEARCH_ENGINE_ID，搜尋功能可能無法正常運作。")