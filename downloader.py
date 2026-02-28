import re
import os
import yt_dlp

class MyLogger:
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        pass

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
            'quiet': False, # 关闭 quiet 模式以便调试，或者我们需要正确处理日志
            'no_warnings': True,
            'logger': MyLogger(), # 使用自定义 logger 防止 str object has no attribute write 错误
            # 增加 User-Agent 模拟浏览器
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.douyin.com/',
                'Accept-Language': 'zh-CN,zh;q=0.9',
            },
            'extractor_args': {
                'douyin': {
                    'skip_empty_json': [True]
                }
            }
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
            error_msg = str(e)
            if "Fresh cookies" in error_msg:
                error_msg = "下载失败：抖音风控限制，需要更新 Cookies 或稍后再试。\n(目前此版本无法自动绕过登录验证)"
            else:
                error_msg = f"下载失败: {error_msg}"
            
            if status_callback:
                status_callback(error_msg)
            return False, error_msg
