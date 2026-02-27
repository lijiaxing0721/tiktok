import re
import os
import yt_dlp

class DouyinDownloader:
    def __init__(self, download_dir):
        self.download_dir = download_dir
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

    def extract_url(self, text):
        """从文本中提取 URL"""
        url_pattern = r'(https?://[^\s]+)'
        match = re.search(url_pattern, text)
        if match:
            return match.group(0)
        return text # 如果没有匹配到，假设输入的就是 URL

    def download_video(self, input_text, status_callback=None):
        """
        下载视频
        :param input_text: 包含链接的文本或直接链接
        :param status_callback: 回调函数，用于更新状态 (message)
        """
        url = self.extract_url(input_text)
        
        if status_callback:
            status_callback(f"正在解析链接: {url}")

        ydl_opts = {
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'format': 'best', # 下载最佳质量
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            # 'restrictfilenames': True, # 暂时保留中文文件名，如果遇到问题再开启
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown Title')
                if status_callback:
                    status_callback(f"找到视频: {title}, 开始下载...")
                
                ydl.download([url])
                
                if status_callback:
                    status_callback(f"下载完成: {title}")
                return True, f"下载成功: {title}"
        except Exception as e:
            error_msg = f"下载失败: {str(e)}"
            if status_callback:
                status_callback(error_msg)
            return False, error_msg
