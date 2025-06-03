import os
import logging
from flask import Flask

# 導入模組
from modules.config import Config
from modules.ai_handler import AIHandler
from modules.search_handler import SearchHandler
from modules.google_sheets_handler import GoogleSheetsHandler
from modules.google_calendar_handler import GoogleCalendarHandler
from modules.google_maps_handler import GoogleMapsHandler
from modules.weather_handler import WeatherHandler
from modules.stock_handler import StockHandler
from modules.news_handler import NewsHandler
from modules.line_bot import LineBotHandler
from modules.google_drive_handler import GoogleDriveHandler
from line_chart_integration_v3 import LineChartSenderV3

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 創建Flask應用實例
app = Flask(__name__)

def create_handlers():
    """創建並初始化所有處理器（無 MySQL 版本）"""
    # 初始化設定
    config = Config()
    
    # 初始化各模組
    ai_handler = AIHandler(config.gemini_api_key)
    search_handler = SearchHandler(config)
    # 移除 db_handler = DBHandler(config)  # 不使用 MySQL
    sheets_handler = GoogleSheetsHandler(config)
    
    # 初始化 Google Calendar Handler，不傳入 db_handler
    try:
        calendar_handler = GoogleCalendarHandler(config, None)  # 傳入 None 代替 db_handler
        logging.info("✅ Google Calendar 處理器初始化成功（無資料庫模式）")
    except Exception as e:
        logging.warning(f"⚠️ Google Calendar 處理器初始化失敗: {e}")
        calendar_handler = None
    
    # 初始化 Google Maps Handler，傳入 ai_handler  
    maps_handler = GoogleMapsHandler(config, ai_handler)
    
    weather_handler = WeatherHandler(config)
    stock_handler = StockHandler(ai_handler)
    news_handler = NewsHandler(ai_handler)
    
    # 初始化Google Drive 處理器
    try:
        drive_handler = GoogleDriveHandler(config)
        if drive_handler.is_available():
            logging.info("✅ Google Drive 處理器初始化成功")
            
            # 執行過期檔案清理
            drive_handler.cleanup_expired_files()
        else:
            logging.warning("⚠️ Google Drive 處理器初始化失敗，將使用文字模式")
            drive_handler = None
    except Exception as e:
        logging.warning(f"⚠️ Google Drive 處理器初始化失敗: {e}，將使用文字模式")
        drive_handler = None
    
    # 初始化圖表發送器（整合 Google Drive）
    chart_sender = LineChartSenderV3(
        line_bot_api=config.line_bot_api,
        stock_handler=stock_handler,
        drive_handler=drive_handler
    )
    logging.info("✅ 圖表發送器初始化成功")
    
    # 使用 AIHandler 作為 Gemini AI 處理器
    if ai_handler.model:
        logging.info("✅ Google Gemini AI 處理器初始化成功")
    else:
        logging.warning("⚠️ Gemini AI 處理器初始化失敗")
    
    # 初始化 LINE Bot 處理器（無 MySQL）
    line_bot_handler = LineBotHandler(
        config=config,
        stock_handler=stock_handler,
        chart_sender=chart_sender,
        calendar_handler=calendar_handler,
        gemini_handler=ai_handler,  # 使用 ai_handler 作為 gemini_handler
        drive_handler=drive_handler,
        search_handler=search_handler,
        weather_handler=weather_handler,
        sheets_handler=sheets_handler,
        financial_news_handler=news_handler,
        maps_handler=maps_handler,
        db_handler=None  # 不使用資料庫
    )
    logging.info("✅ LINE Bot 處理器初始化成功（無資料庫模式）")
    
    return config, line_bot_handler

# 初始化處理器
config, line_bot_handler = create_handlers()

@app.route("/", methods=['GET'])
def health_check():
    """健康檢查端點"""
    return "LINE Bot is running on Render! 🚀", 200

@app.route("/callback", methods=['POST'])
def callback():
    """LINE Webhook 回調路由"""
    from flask import request
    
    try:
        body = request.get_data(as_text=True)
        signature = request.headers.get('X-Line-Signature', '')
        
        if not signature:
            logging.error("Missing X-Line-Signature header")
            return 'Bad Request', 400
        
        return line_bot_handler.handle_webhook(body, signature)
    
    except Exception as e:
        logging.error(f"Webhook處理錯誤: {e}")
        return 'Internal Server Error', 500

@app.route("/webhook", methods=['POST'])
def webhook():
    """備用webhook端點（相容舊版本）"""
    return callback()

@app.route("/status", methods=['GET'])
def status():
    """系統狀態檢查"""
    status_info = {
        "service": "LINE Bot",
        "status": "running",
        "platform": "Render",
        "version": "1.0.0",
        "database": "disabled"  # 明確標示無資料庫
    }
    
    # 檢查各模組狀態
    try:
        # 檢查Google Drive狀態
        if hasattr(line_bot_handler, 'drive_handler') and line_bot_handler.drive_handler:
            if line_bot_handler.drive_handler.is_available():
                status_info["google_drive"] = "available"
            else:
                status_info["google_drive"] = "unavailable"
        else:
            status_info["google_drive"] = "not_configured"
        
        # 檢查LINE Bot API狀態
        if config.line_bot_api:
            status_info["line_bot_api"] = "configured"
        else:
            status_info["line_bot_api"] = "not_configured"
        
        # 檢查Gemini AI狀態
        if hasattr(line_bot_handler, 'gemini_handler') and line_bot_handler.gemini_handler:
            if line_bot_handler.gemini_handler.model:
                status_info["gemini_ai"] = "available"
            else:
                status_info["gemini_ai"] = "unavailable"
        else:
            status_info["gemini_ai"] = "not_configured"
            
    except Exception as e:
        logging.warning(f"狀態檢查警告: {e}")
        status_info["warning"] = str(e)
    
    return status_info, 200

if __name__ == "__main__":
    # 本地開發模式
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
else:
    # 生產模式（Gunicorn）
    logging.info("🚀 LINE Bot在Render中啟動")