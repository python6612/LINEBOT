import logging
import base64
import mimetypes
import google.generativeai as genai

class AIHandler:
    """AI處理類別，負責處理Google Gemini AI相關功能"""
    def __init__(self, gemini_api_key):
        self.api_key = gemini_api_key
        self.model = None
        self.chat = None
        
        # 初始化AI模型
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("gemini-2.0-flash")
                self.chat = self.model.start_chat()
                logging.info("Google Gemini AI 已初始化。")
            except Exception as e:
                logging.error(f"初始化 Google Gemini AI 失敗: {e}")
        else:
            logging.warning("未設定 GEMINI_API_KEY，文字和圖片分析功能將無法使用。")

    def process_text(self, text):
        """處理文字訊息"""
        if not self.chat:
            return "AI 文字處理功能未初始化，請檢查 GEMINI_API_KEY。"
        try:
            # 添加角色提示
            user_prompt = f"""
你現在的名字: 建宏。請根據以下描述扮演他：
- 個性：溫和、理性、喜歡用清楚的方式說話
- 興趣：AI、Python、自動化、LINE Bot 整合
- 態度：不炫技，喜歡幫助別人，能講重點

以下是收到的訊息：
{text}
請用他的語氣回應對方。
"""
            response = self.chat.send_message(user_prompt)
            return response.text.strip() if response.text else "AI 回應錯誤或空白"
        except Exception as e:
            logging.error(f"Google AI Studio API 錯誤: {e}")
            return f"與 Google AI Studio 通訊時發生錯誤: {e}"

    def process_image(self, image_binary):
        """處理圖片訊息"""
        if not self.model:
            return "AI 圖片分析功能未初始化，請檢查 GOOGLE_API_KEY。"
        try:
            image_base64 = base64.b64encode(image_binary).decode("utf-8")
            mime_type, _ = mimetypes.guess_type("temp_image.jpg")
            if not mime_type or not mime_type.startswith('image/'):
                mime_type = 'image/jpeg'

            gemini_image_content = {
                "mime_type": mime_type,
                "data": image_base64
            }

            # 添加角色提示進行圖片分析
            prompt_text = {
                "text": """
你現在的名字: 建宏。請根據以下描述扮演他：
- 個性：溫和、理性、喜歡用清楚的方式說話
- 興趣：AI、Python、自動化、LINE Bot 整合
- 態度：不炫技，喜歡幫助別人，能講重點

請分析這張圖片，並以中文50字左右回答。用建宏的語氣回應對方。
"""
            }

            vision_model = genai.GenerativeModel("gemini-2.0-flash")
            response = vision_model.generate_content([gemini_image_content, prompt_text])

            return response.text.strip() if response and response.text else "無法識別圖片內容，請再試一次。"
        except Exception as e:
            logging.error(f"處理 base64 圖片錯誤: {e}")
            return f"圖片分析發生錯誤：{e}"