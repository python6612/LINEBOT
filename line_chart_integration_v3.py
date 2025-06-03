import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np
import io
import base64
import logging
from datetime import datetime
import os
from linebot.models import ImageSendMessage, TextSendMessage

class LineChartSenderV3:
    """LINE Bot 圖表發送器 V3 - 整合 Google Drive 上傳功能"""
    
    def __init__(self, line_bot_api, stock_handler, drive_handler=None):
        """初始化圖表發送器
        
        Args:
            line_bot_api: LINE Bot API 實例
            stock_handler: 股票處理器實例
            drive_handler: Google Drive 處理器實例（可選）
        """
        self.line_bot_api = line_bot_api
        self.stock_handler = stock_handler
        self.drive_handler = drive_handler
        
        # 設定中文字體
        self.setup_chinese_font()
        
        # 設定圖表樣式
        plt.style.use('default')
        
        logging.info("✅ LineChartSenderV3 初始化成功")
    
    def setup_chinese_font(self):
        """設定中文字體支援"""
        try:
            # 使用系統內建字體
            plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            self.chinese_font_name = 'DejaVu Sans'
            logging.info("✅ 中文字體設定完成")
        except Exception as e:
            logging.warning(f"⚠️ 中文字體設定失敗: {e}")
            self.chinese_font_name = 'DejaVu Sans'
    
    def create_stock_chart(self, stock_data, stock_name):
        """創建股票圖表"""
        try:
            # 創建圖表
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # 繪製基本線圖
            if isinstance(stock_data, list) and len(stock_data) > 0:
                prices = [float(item.get('收盤價', 0)) for item in stock_data]
                dates = list(range(len(prices)))
                
                ax.plot(dates, prices, linewidth=2, color='#2E86AB', marker='o', markersize=4)
                ax.set_title(f'{stock_name} 股價走勢', fontsize=16, fontweight='bold')
                ax.set_xlabel('時間', fontsize=12)
                ax.set_ylabel('價格 (TWD)', fontsize=12)
                ax.grid(True, alpha=0.3)
                
                # 美化圖表
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                
                plt.tight_layout()
            
            # 轉換為圖片
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='PNG', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()
            
            return img_buffer.getvalue()
            
        except Exception as e:
            logging.error(f"創建股票圖表失敗: {e}")
            return None