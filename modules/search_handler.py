import logging
import requests
from googleapiclient.discovery import build

class SearchHandler:
    """搜尋處理器 - 處理 Google 搜尋功能"""
    
    def __init__(self, config):
        self.config = config
        self.google_api_key = config.google_api_key
        self.search_engine_id = config.google_search_engine_id
        
        if self.google_api_key and self.search_engine_id:
            try:
                self.service = build("customsearch", "v1", developerKey=self.google_api_key)
                logging.info("✅ Google 搜尋服務初始化成功")
            except Exception as e:
                logging.error(f"Google 搜尋服務初始化失敗: {e}")
                self.service = None
        else:
            self.service = None
            logging.warning("⚠️ Google 搜尋功能未設定")
    
    def search_google(self, query, num_results=5):
        """執行 Google 搜尋"""
        if not self.service:
            return "搜尋功能未設定，請檢查 Google API 設定。"
        
        try:
            result = self.service.cse().list(
                q=query,
                cx=self.search_engine_id,
                num=num_results
            ).execute()
            
            if 'items' in result:
                search_results = []
                for item in result['items']:
                    search_results.append({
                        'title': item.get('title', ''),
                        'link': item.get('link', ''),
                        'snippet': item.get('snippet', '')
                    })
                return search_results
            else:
                return "沒有找到相關結果。"
                
        except Exception as e:
            logging.error(f"Google 搜尋錯誤: {e}")
            return f"搜尋時發生錯誤: {e}"