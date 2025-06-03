import logging
import requests
import json

class StockHandler:
    """股票處理器 - 處理股票查詢功能"""
    
    def __init__(self, ai_handler):
        self.ai_handler = ai_handler
        logging.info("✅ 股票處理器初始化成功")
    
    def get_stock_info(self, stock_code):
        """取得股票資訊"""
        try:
            # 這裡可以整合實際的股票 API
            # 目前返回模擬資料
            stock_info = {
                'code': stock_code,
                'name': f'股票 {stock_code}',
                'price': '100.00',
                'change': '+1.50',
                'change_percent': '+1.52%'
            }
            
            return self.format_stock_message(stock_info)
            
        except Exception as e:
            logging.error(f"股票查詢錯誤: {e}")
            return f"股票查詢時發生錯誤: {e}"
    
    def format_stock_message(self, stock_info):
        """格式化股票訊息"""
        message = f"""📈 {stock_info['name']} ({stock_info['code']})

💰 股價: {stock_info['price']}
📊 漲跌: {stock_info['change']} ({stock_info['change_percent']})"""
        
        return message