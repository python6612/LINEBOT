import logging
from flask import request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

class LineBotHandler:
    """LINE Bot 處理器（無資料庫版本）"""
    
    def __init__(self, config, stock_handler=None, chart_sender=None, 
                 calendar_handler=None, gemini_handler=None, drive_handler=None,
                 search_handler=None, weather_handler=None, sheets_handler=None,
                 financial_news_handler=None, maps_handler=None, db_handler=None):
        
        self.config = config
        self.line_bot_api = config.line_bot_api
        self.handler = config.handler
        
        # 各種處理器
        self.stock_handler = stock_handler
        self.chart_sender = chart_sender
        self.calendar_handler = calendar_handler
        self.gemini_handler = gemini_handler
        self.drive_handler = drive_handler
        self.search_handler = search_handler
        self.weather_handler = weather_handler
        self.sheets_handler = sheets_handler
        self.financial_news_handler = financial_news_handler
        self.maps_handler = maps_handler
        self.db_handler = db_handler  # 可以是 None
        
        # 註冊事件處理器
        self.register_handlers()
        
        logging.info("✅ LINE Bot 處理器初始化成功（無資料庫模式）")
    
    def register_handlers(self):
        """註冊 LINE Bot 事件處理器"""
        if self.handler:
            @self.handler.add(MessageEvent, message=TextMessage)
            def handle_text_message(event):
                self.handle_text_message_event(event)
        else:
            logging.warning("⚠️ LINE Bot handler 未初始化，無法註冊事件處理器")
    
    def handle_webhook(self, body, signature):
        """處理 LINE Webhook"""
        if not self.handler:
            logging.error("LINE Bot handler 未初始化")
            return 'Service Unavailable', 503
            
        try:
            self.handler.handle(body, signature)
            return 'OK', 200
        except InvalidSignatureError:
            logging.error("Invalid signature")
            return 'Bad Request', 400
        except Exception as e:
            logging.error(f"Webhook 處理錯誤: {e}")
            return 'Internal Server Error', 500    
    def handle_text_message_event(self, event):
        """處理文字訊息事件"""
        user_message = event.message.text
        user_id = event.source.user_id
        
        try:
            # 基本指令處理
            if user_message.lower() in ['hello', 'hi', '你好', '嗨']:
                reply_text = "你好！我是建宏的 LINE Bot 助手 🤖\n\n可以試試以下功能：\n• 天氣查詢\n• 股票查詢\n• 新聞查詢\n• AI 對話"
            
            elif user_message.startswith('天氣'):
                city = user_message.replace('天氣', '').strip()
                if not city:
                    city = '台北'
                reply_text = self.weather_handler.get_weather(city) if self.weather_handler else "天氣功能未啟用"
            
            elif user_message.startswith('股票'):
                stock_code = user_message.replace('股票', '').strip()
                if not stock_code:
                    stock_code = '2330'
                reply_text = self.stock_handler.get_stock_info(stock_code) if self.stock_handler else "股票功能未啟用"
            
            elif user_message.startswith('新聞'):
                query = user_message.replace('新聞', '').strip()
                if not query:
                    query = '台灣'
                reply_text = self.financial_news_handler.get_news(query) if self.financial_news_handler else "新聞功能未啟用"
            
            elif user_message.startswith('搜尋'):
                query = user_message.replace('搜尋', '').strip()
                if query:
                    reply_text = self.search_handler.search_google(query) if self.search_handler else "搜尋功能未啟用"
                else:
                    reply_text = "請提供搜尋關鍵字，例如：搜尋 Python"
            
            elif user_message.startswith('地點'):
                location = user_message.replace('地點', '').strip()
                if location:
                    reply_text = self.maps_handler.search_places(location) if self.maps_handler else "地圖功能未啟用"
                else:
                    reply_text = "請提供地點名稱，例如：地點 台北101"
            
            else:
                # 使用 AI 處理一般對話
                reply_text = self.gemini_handler.process_text(user_message) if self.gemini_handler else "AI 功能未啟用"
            
            # 發送回覆
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_text)
            )
            
        except Exception as e:
            logging.error(f"處理文字訊息錯誤: {e}")
            error_message = "抱歉，處理您的訊息時發生錯誤，請稍後再試。"
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=error_message)
            )