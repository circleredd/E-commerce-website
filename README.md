# 電商平台
[![GitHub release](https://img.shields.io/github/release/Text-Analytics-and-Retrieval/db_class2023)](https://github.com/Text-Analytics-and-Retrieval/db_class2023/releases/latest)
[![GitHub license](https://img.shields.io/github/license/Text-Analytics-and-Retrieval/db_class2023)](https://github.com/Text-Analytics-and-Retrieval/db_class2023/main/LICENSE)

一套使用Flask開發的網路書店系統，後端使用Oracle資料庫
<br>

## 功能
- 提供CRUD範例，並搭配資料分析功能。
- 以MVC架構開發。
- 一般消費者可以瀏覽、搜尋、購買商品，並查看訂單狀態。
- 後台管理者可以編輯商品，並檢視每筆訂單以及商品銷售圖表。


## 安裝
### 1. 取得原始碼
```bash
git clone https://github.com/Text-Analytics-and-Retrieval/db_class2023.git
cd db_class2023/
```
### 2. 啟動Docker container
```bash!	
docker run --ipc=host -it -v $(pwd):/workspace -p 18080:8080 -p 15000:5000 --name=db_class2023 continuumio/anaconda3
```

### 3. 安裝環境
##### 安裝python套件
```bash
cd workspace
pip install -r requirements.txt
conda install -c anaconda libaio #Oracle Instant Client會用到
```

##### 安裝Oracle Instant Client
```bash
# 下載Oracle Instant Client
wget https://download.oracle.com/otn_software/linux/instantclient/219000/instantclient-basic-linux.x64-21.9.0.0.0dbru.zip
# 下載解壓縮套件
apt-get update
apt-get install unzip
# 解壓縮檔案
unzip instantclient-basic-linux.x64-21.9.0.0.0dbru.zip
# 設定環境變數
export LD_LIBRARY_PATH=/workspace/instantclient_21_9:$LD_LIBRARY_PATH
```

##### 修改程式碼

```python=
# 移除link.py中的指令路徑
cx_Oracle.init_oracle_client()
```

```python=
# 使Flask監聽所有介面
app.run(host='0.0.0.0')
```

### 4. 啟動程式
```python=
python app.py
```

## 使用
- 輸入http://localhost:15000/進入首頁。
- 首次使用請點選註冊按鈕，並註冊帳號。
- 註冊後，點選登入即可進入頁面。
