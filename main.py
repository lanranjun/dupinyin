import wave
import string
from pyaudio import PyAudio
from pynput.keyboard import Controller, Key, Listener
import threading

chars = list(string.ascii_lowercase)


# 监听按压
def on_press(key):
    try:
        print("正在按压:", format(key.char))
        char = format(key.char)
        if char in chars:
            file_path = f"sounds/{char}.wav"
            threading.Thread(target=play, args=(file_path, sema)).start()
    except AttributeError:
        print("正在按压:", format(key))


# 监听释放
def on_release(key):
    print("已经释放:", format(key))

    if key == Key.esc:
        # 停止监听
        return False


# 开始监听
def start_listen():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


# 播放音乐
def play(filename, sema):
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


if __name__ == '__main__':
    sema = threading.Semaphore(value=5)
    # 实例化键盘
    kb = Controller()
    start_listen()
