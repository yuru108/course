# 專題說明

本專題為資料庫系統的期中專題，主要需搭建一個可運行的 3-tier 架構選課系統。

## 功能

### 加選
- 同學只能加選本系的課程
- 人數已滿的課程不可加選
- 不可加選衝堂的課程
- 不可加選與已選課程同名的課程
- 加選後學分不可超過最高學分限制 (30 學分)

### 退選
- 退選後學分不可低於最低學分限制 (9 學分)
- 退選必修課需提出警告

### 功課表
- 列出同學已選課程之課號、名稱、課程時間 (可條列或者以功課表方式表示)
- 系統應根據每個同學的系所、年級，將其必修課預選進其功課表中

### 搜尋
- 勾選想使用的搜尋，並輸入內容搜尋特定課程
- 勾選以篩選出該同學可選的課程清單

### 關注抽籤功能
- 對於人數已滿的課程，可以關注
- 當該課程有人退選導致有空額出現時，由所有關注該課程的同學亂數抽選一人加選該課程
- 同學不能關注不可加選的課程

### 登入/登出/註冊

## 技術實現

- 使用 Flask 框架搭建後端
- 使用 HTML、CSS、JavaScript 構建前端界面
- 使用 MySQL 數據庫存儲課程信息和用戶信息

如有任何建議或改進，請隨時提出 issue 或提交 pull request。
