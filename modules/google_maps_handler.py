import logging
import requests

class GoogleMapsHandler:
    """Google Maps 處理器"""
    
    def __init__(self, config, ai_handler):
        self.config = config
        self.ai_handler = ai_handler
        self.api_key = config.google_api_key
        
        if not self.api_key:
            logging.warning("⚠️ Google Maps API 金鑰未設定")
        else:
            logging.info("✅ Google Maps 處理器初始化成功")
    
    def search_places(self, query):
        """搜尋地點"""
        if not self.api_key:
            return "Google Maps 功能未設定，請檢查 GOOGLE_API_KEY。"
        
        try:
            # 使用 Google Places API 搜尋
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            params = {
                'query': query,
                'key': self.api_key,
                'language': 'zh-TW'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'OK' and data.get('results'):
                places = data['results'][:3]  # 取前3個結果
                
                message = f"🗺️ 搜尋結果：{query}\n\n"
                for i, place in enumerate(places, 1):
                    name = place.get('name', '未知地點')
                    address = place.get('formatted_address', '地址未知')
                    rating = place.get('rating', 'N/A')
                    
                    message += f"{i}. {name}\n"
                    message += f"   📍 {address}\n"
                    message += f"   ⭐ 評分: {rating}\n\n"
                
                return message.strip()
            else:
                return f"找不到 '{query}' 的相關地點。"
                
        except Exception as e:
            logging.error(f"Google Maps 搜尋錯誤: {e}")
            return f"地點搜尋時發生錯誤: {e}"