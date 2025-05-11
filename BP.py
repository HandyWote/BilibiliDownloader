import json
import os

import re
import requests
from moviepy import VideoFileClip, AudioFileClip


class P:
    """
    视频下载和处理类
    
    功能：
    1. 从指定URL获取视频和音频链接
    2. 下载视频和音频文件
    3. 合并音视频文件
    """
    def __init__(self, url):
        """
        初始化方法
        
        参数:
        url -- 视频页面的URL
        """
        information = self.geturl(url)
        print(information)
        self.videoURL = information['vurl']
        self.audioURL = information['aurl']
        self.header = information['header']
        self.name = information['name']

    def geturl(self, url):
        """
        从URL获取视频和音频链接
        
        参数:
        url -- 视频页面的URL
        
        返回:
        包含视频链接(vurl)、音频链接(aurl)、请求头(header)和视频名称(name)的字典
        """
        h = url.split('&')[0]
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            'referer': f'{h}',
            'accept-encoding': 'identity',
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"'
        }
        try:
            response = requests.get(url, headers=header)
            response.raise_for_status()  # 如果请求失败，抛出异常
            html_content = response.text
            name = re.findall('title="(.*?)"', html_content)[0]
            info = re.findall('window.__playinfo__=(.*?)</script>', html_content)[0]
            jinfo = json.loads(info)
            audio_bandwidth = 0
            audio_matches = ''
            for audio in jinfo['data']['dash']['audio']:
                if audio['bandwidth'] > audio_bandwidth:
                    audio_bandwidth = audio['bandwidth']
                    audio_matches = audio['baseUrl']
            video_bandwidth = 0
            video_matches = ''
            for video in jinfo['data']['dash']['video']:
                if video['bandwidth'] > video_bandwidth:
                    video_bandwidth = video['bandwidth']
                    video_matches = video['baseUrl']
            result = {
                'aurl': audio_matches if audio_matches else None,
                'vurl': video_matches if video_matches else None,
                'header': header,
                'name': name
            }
            return result

        except Exception:
            print("获取媒体链接失败")
            return {
                'aurl': None,
                'vurl': None,
                'header': None,
                'name': None
            }

    def getmedia(self):
        """
        下载视频和音频文件
        
        将下载的视频和音频分别存储在self.vr和self.ar属性中
        """
        try:
            self.vr = requests.get(self.videoURL, headers=self.header)
            self.ar = requests.get(self.audioURL, headers=self.header)
        except Exception:
            print('获取媒体失败')

    def writemedia(self):
        """
        将下载的视频和音频写入本地文件
        
        视频保存为video.mp4，音频保存为audio.mp3
        """
        try:
            open('video.mp4','wb').write(self.vr.content)
            open('audio.mp3', 'wb').write(self.ar.content)
        except Exception:
            print('写入媒体失败')

    def conbine(self):
        """
        合并视频和音频文件
        
        使用moviepy库将音频合并到视频中，输出文件名为视频标题.mp4
        """
        try:
            video = VideoFileClip("video.mp4")
            audio = AudioFileClip("audio.mp3")
            final_clip = video.with_audio(audio)
            final_clip.write_videofile(f"{self.name}.mp4")
        except Exception:
            print('合成失败')

    def rm(self):
        """
        删除临时文件

        删除video.mp4和audio.mp3文件
        """
        try:
            os.remove("video.mp4")
            os.remove("audio.mp3")
        except Exception:
            print("删除临时文件失败")

    def py(self):
        """
        执行完整处理流程
        
        依次调用:
        1. getmedia() - 下载媒体文件
        2. writemedia() - 保存到本地
        3. conbine() - 合并音视频
        4. 删除临时文件
        """
        self.getmedia()
        self.writemedia()
        self.conbine()
        self.rm()

if __name__ == '__main__':
    url = input('请输入网址:\n')
    p = P(url)
    p.py()
