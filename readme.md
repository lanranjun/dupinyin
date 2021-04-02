## 项目目的
- 小朋友使用键盘打字，键盘标注的都是大写的英文字母
- 看着拼音打字，在键盘上不易找到对应按键，所以本人某宝购买了小写键盘贴
- 本项目实现：点击键盘字母读对应汉语拼音发音
- 本项目因个人需要**只监控了字母按键**没监控其他按键

## 在线带拼音的打字网站

https://dazi.kukuw.com/key.php?kid=p1

## 拼音发音可以从以下网站获取：
- http://du.hanyupinyin.cn/
- http://www.wenxue360.com/pinyin/

下载下来的是mp3格式 可以转wav使用
本项目使用的是wav，转换工具waveMaker

## 未实现部分
- 翘舌音发音
- 整体音节发音

## 使用方法
```
pip install -r requirements
```
- PyAudio需要下载whl文件
- pynput高版本会在pyinstaller导出exe时报错 这里使用1.6.8版本
- 生成exe文件
```
pyinstaller -F main.py
```
- dist文件夹存放生成的exe文件
- 将下载的发音文件mp3格式转为wav类型 复制到 dist/目录下，然后运行exe文件即可
- 使用键盘Esc键退出