import logging
import requests

class WeatherHandler:
    """天氣處理器 - 處理天氣查詢功能"""
    
    def __init__(self, config):
        self.config = config
        self.api_key = config.weather_api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        if not self.api_key:
            logging.warning("⚠️ 天氣 API 金鑰未設定")
    
    def get_weather(self, city):
        """取得指定城市的天氣資訊"""
        if not self.api_key:
            return "天氣功能未設定，請檢查 WEATHER_API_KEY。"
        
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'zh_tw'
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('cod') == 200:
                weather_info = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure']
                }
                
                return self.format_weather_message(weather_info)
            else:
                return f"無法取得 {city} 的天氣資訊。"
                
        except Exception as e:
            logging.error(f"天氣查詢錯誤: {e}")
            return f"天氣查詢時發生錯誤: {e}"
    
    def format_weather_message(self, weather_info):
        """格式化天氣訊息"""
        message = f"""🌤️ {weather_info['city']} 天氣資訊

🌡️ 溫度: {weather_info['temperature']}°C
☁️ 天氣: {weather_info['description']}
💧 濕度: {weather_info['humidity']}%
🔽 氣壓: {weather_info['pressure']} hPa"""
        
        return message