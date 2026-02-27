import os
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform

from downloader import DouyinDownloader

class DouyinApp(App):
    def build(self):
        self.title = "抖音视频下载工具"
        
        # 布局
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 输入框
        self.url_input = TextInput(
            hint_text="请在此粘贴抖音分享链接...",
            multiline=True,
            size_hint=(1, 0.3)
        )
        layout.add_widget(self.url_input)
        
        # 状态标签
        self.status_label = Label(
            text="等待输入...",
            size_hint=(1, 0.2),
            halign="center",
            valign="middle"
        )
        self.status_label.bind(size=self.status_label.setter('text_size')) # 确保文本换行
        layout.add_widget(self.status_label)
        
        # 下载按钮
        self.download_btn = Button(
            text="开始下载",
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        self.download_btn.bind(on_press=self.start_download)
        layout.add_widget(self.download_btn)
        
        # 确定下载目录
        self.download_dir = self.get_download_dir()
        self.downloader = DouyinDownloader(self.download_dir)
        
        # 请求权限 (仅 Android)
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.INTERNET, 
                Permission.WRITE_EXTERNAL_STORAGE, 
                Permission.READ_EXTERNAL_STORAGE
            ])

        return layout

    def get_download_dir(self):
        """获取下载目录，根据平台自动适配"""
        download_dir = ""
        if platform == 'android':
            try:
                from android.storage import primary_external_storage_path
                # 通常是 /storage/emulated/0/Download
                base_path = primary_external_storage_path()
                if base_path:
                    download_dir = os.path.join(base_path, 'Download', 'DouyinVideos')
                else:
                    # Fallback
                    download_dir = os.path.join('/sdcard/Download', 'DouyinVideos')
            except ImportError:
                # Fallback if module not found (e.g. testing on PC but platform set to android manually?)
                download_dir = os.path.join(os.getcwd(), 'Downloads')
        else:
            # PC 端默认在当前目录下的 Downloads
            download_dir = os.path.join(os.getcwd(), 'Downloads')
        
        if not os.path.exists(download_dir):
            try:
                os.makedirs(download_dir)
            except Exception as e:
                print(f"创建目录失败: {e}")
                # 回退到应用私有目录或当前目录
                return os.getcwd()
                
        return download_dir

    def update_status(self, message):
        """在主线程更新 UI"""
        def _update(dt):
            self.status_label.text = message
        Clock.schedule_once(_update)

    def start_download(self, instance):
        url_text = self.url_input.text.strip()
        if not url_text:
            self.update_status("请输入链接！")
            return

        self.download_btn.disabled = True
        self.update_status("准备下载...")
        
        # 启动线程下载，避免阻塞 UI
        threading.Thread(target=self.run_download, args=(url_text,)).start()

    def run_download(self, text):
        try:
            success, msg = self.downloader.download_video(
                text, 
                status_callback=self.update_status
            )
            if success:
                self.update_status(f"下载成功！\n保存位置: {self.download_dir}")
            else:
                self.update_status(f"下载失败: {msg}")
        except Exception as e:
            self.update_status(f"发生错误: {str(e)}")
        finally:
            # 恢复按钮状态
            Clock.schedule_once(lambda dt: setattr(self.download_btn, 'disabled', False))

if __name__ == '__main__':
    DouyinApp().run()
