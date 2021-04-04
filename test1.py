import wave
import string
import time
import threading
from pyaudio import PyAudio
from pynput.keyboard import Controller, Key, Listener

"""
0、记录已按的字母存放缓存
1、先判断是不是整体认读音节
2、哪些可以自己发音并是一个字
2、判断第一个字母、前两个是不是声母
3、声母后面是不是 i 和 u
4、判断韵母
5、如果有声母必须有韵母，整体认读音节、单独发音成字
6、按空格后发音
7、清除缓存
"""

chars = list(string.ascii_lowercase)
# 声母
sm_one_char = ['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 'q', 'x', 'z', 'c', 's', 'r', 'y', 'w']
sm_two_char = ['zh', 'ch', 'sh']
sm_list = sm_two_char + sm_one_char
# 韵母
ym_one_char = ['a', 'o', 'e', 'i', 'u', 'v']
ym_two_char = ['ai', 'ei', 'ui', 'ao', 'ou', 'iu', 'ie', 've', 'er', 'an', 'en', 'in', 'un']
ym_three_char = ['ang', 'eng', 'ing', 'ong']
ym_list = ym_three_char + ym_two_char + ym_one_char
# 整体认读音节
zt_two_char = ['ri', 'zi', 'ci', 'si', 'yi', 'wu', 'yu', 'ye']
zt_three_char = ['zhi', 'chi', 'shi', 'yue', 'yin', 'yun']
zt_four_char = ['yuan', 'ying']
zt_list = zt_four_char + zt_three_char + zt_two_char

# 可以单独成字
one_char = ['a', 'e', 'ai', 'ao', 'ou', 'er', 'an', 'en']

# 缓存
cache_chars = []


# 监听按压并发音，收集已按键盘字母
def on_press(key):
    try:
        print("正在按压:", format(key.char))
        char = format(key.char)
        if char in chars:
            cache_chars.append(char)
            play(char)
    except AttributeError:
        print("正在按压:", format(key))


# 监听释放
def on_release(key):
    print("已经释放:", format(key))

    if key == Key.esc:
        # 停止监听
        return False
    if key == Key.space:
        pinyin_str = "".join(cache_chars)
        print("pinyin:", pinyin_str)
        res = read_pinyin(pinyin_str)
        if not res:
            print("不可读哦")


def read_pinyin(pinyin_str):
    if pinyin_str in zt_list:
        play(pinyin_str)
        cache_chars.clear()
        return True
    sm2 = pinyin_str[:2]
    sm1 = pinyin_str[:1]
    pinyin = []
    if sm2 in sm_two_char:
        tmp = pinyin_str[2:]
        middle, ym = is_ym(tmp)
        if not ym:
            return False
        play(sm2)
        if middle:
            play(middle)
        play(ym)
        cache_chars.clear()
        return True
    if sm1 in sm_one_char:
        tmp = pinyin_str[1:]
        middle, ym = is_ym(tmp)
        if not ym:
            return False
        play(sm1)
        if middle:
            time.sleep(0.5)
            play(middle)
        time.sleep(0.8)
        play(ym)
        cache_chars.clear()
        return True
    if pinyin_str in one_char:
        play(pinyin_str)
        cache_chars.clear()
        return True
    cache_chars.clear()
    return False


def is_ym(pinyin_str):
    if pinyin_str in ym_list:
        ym = pinyin_str
        return '', ym
    middle = pinyin_str[:1]
    ym = pinyin_str[1:]
    if middle in ['i', 'u']:
        if ym in ym_list:
            return middle, ym
    return "", ""


# 开始监听
def start_listen():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


# 播放音乐
def player(filename):
    sema.acquire()
    chunk = 1024
    wf = wave.open(filename, 'rb')
    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
                    rate=wf.getframerate(), output=True)
    data = wf.readframes(chunk)
    while data != b'':
        data = wf.readframes(chunk)
        stream.write(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    sema.release()


def play(char_str):
    file_path = f"sounds/{char_str}.wav"
    threading.Thread(target=player, args=(file_path,)).start()


if __name__ == '__main__':
    sema = threading.Semaphore(value=3)
    # 实例化键盘
    kb = Controller()
    start_listen()
