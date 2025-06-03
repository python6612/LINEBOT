## 功能特色

### ✅ 已包含功能
- 🤖 **AI 對話** - Google Gemini AI 智能對話
- 🌤️ **天氣查詢** - 即時天氣資訊
- 📈 **股票查詢** - 股票價格查詢
- 📰 **新聞查詢** - 最新新聞資訊
- 🔍 **Google 搜尋** - 網路搜尋功能
- 🗺️ **地點搜尋** - Google Maps 地點查詢
- 📊 **Google Sheets** - 試算表整合
- 📅 **Google Calendar** - 行事曆整合
- ☁️ **Google Drive** - 雲端儲存整合

### ❌ 已移除功能
- 🗄️ **MySQL 資料庫** - 移除所有資料庫相關功能
- 📊 **資料持久化** - 無法儲存用戶資料
- 🔄 **複雜的資料處理** - 簡化為無狀態操作


## 使用方式

### 基本指令
- `你好` - 顯示功能選單
- `天氣 台北` - 查詢台北天氣
- `股票 2330` - 查詢台積電股價
- `新聞 科技` - 查詢科技新聞
- `搜尋 Python` - Google 搜尋
- `地點 台北101` - 地點搜尋


## 專案結構

```
LINEBOT/
├── main_cloud.py          # 主應用程式
├── requirements.txt       # Python 依賴
├── render.yaml           # Render 部署設定
├── Procfile              # 啟動命令
├── modules/              # 功能模組
│   ├── config.py         # 設定管理
│   ├── ai_handler.py     # AI 處理
│   ├── line_bot.py       # LINE Bot 核心
│   ├── weather_handler.py # 天氣功能
│   ├── stock_handler.py   # 股票功能
│   └── ...               # 其他模組
├── debug/                # 除錯文件
├── note/                 # 部署說明
└── result/               # 測試結果
```
