# anigamerpy 0.1.0
[動畫瘋](https://ani.gamer.com.tw/)爬蟲工具

## 下載
```
pip install anigamerpy
```

## 使用方式
本模組可獲取兩種資料

* 新番資料

即動畫瘋首頁的所有動畫
```python
from anigamerpy import anime
from loguru import logger

data = anime.Anime().new_anime().data

#0為第一筆資料 1為第二筆資料 以此類推
logger.info(data[0]['name']) #動畫名
logger.info(data[0]['watch_count']) #目前觀看次數
logger.info(data[0]['episode']) #目前集數
logger.info('https://ani.gamer.com.tw/' + data[0]['href']) #超連結 若要完整連結前面需加https://ani.gamer.com.tw/
logger.info(data[0]['image']) #圖片
```

* 搜尋資料

獲取搜尋的結果
```python
from anigamerpy import anime
from loguru import logger

data = anime.Anime().search_anime(keyword='bang dream').data #需加入搜尋關鍵字 請使用字串來搜尋

#0為第一筆資料 1為第二筆資料 以此類推
logger.info(data[0]['name']) #動畫名
logger.info(data[0]['watch_count']) #觀看次數
logger.info(data[0]['episode']) #集數
logger.info(str(data[0]['years'])[3:]) #年分
logger.info('https://ani.gamer.com.tw/' + data[0]['href']) #超連結 若要完整連結前面需加https://ani.gamer.com.tw/
logger.info(data[0]['image']) #圖片
```

## 其他
若有發現任何bug或是問題，請開issue

## License
本專案使用 MIT LICENSE

MIT © [Sakuya0502](https://github.com/Sakuya0502/anigamerpy/blob/main/LICENSE)