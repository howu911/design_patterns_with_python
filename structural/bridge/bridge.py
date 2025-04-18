"""
桥接模式使用场景：
1. 需要避免抽象与实现的永久绑定 - 可以在运行时切换实现
2. 抽象和实现都应该能够独立扩展 - 修改抽象不影响实现，反之亦然
3. 需要隐藏实现细节 - 客户端只需要知道抽象接口
4. 有多个维度变化的系统 - 每个维度可以独立变化而不相互影响
5. 需要跨平台的应用程序 - 抽象层定义接口，实现层处理平台差异

桥接模式示例 - 设备控制系统

本示例展示如何使用桥接模式来设计一个跨平台的设备控制系统，
不同类型的遥控器（抽象）可以控制不同类型的设备（实现）。
"""

from abc import ABC, abstractmethod


# 实现部分接口
class Device(ABC):
    """设备接口 - 实现部分"""
    
    @abstractmethod
    def is_enabled(self):
        """检查设备是否开启"""
        pass
    
    @abstractmethod
    def enable(self):
        """开启设备"""
        pass
    
    @abstractmethod
    def disable(self):
        """关闭设备"""
        pass
    
    @abstractmethod
    def get_volume(self):
        """获取音量"""
        pass
    
    @abstractmethod
    def set_volume(self, percent):
        """设置音量"""
        pass
    
    @abstractmethod
    def get_channel(self):
        """获取频道"""
        pass
    
    @abstractmethod
    def set_channel(self, channel):
        """设置频道"""
        pass


# 具体实现类
class Television(Device):
    """电视设备 - 具体实现"""
    
    def __init__(self):
        self._enabled = False
        self._volume = 30
        self._channel = 1
    
    def is_enabled(self):
        return self._enabled
    
    def enable(self):
        self._enabled = True
        print("电视已开机")
    
    def disable(self):
        self._enabled = False
        print("电视已关机")
    
    def get_volume(self):
        return self._volume
    
    def set_volume(self, percent):
        if percent > 100:
            self._volume = 100
        elif percent < 0:
            self._volume = 0
        else:
            self._volume = percent
        print(f"电视音量设置为 {self._volume}%")
    
    def get_channel(self):
        return self._channel
    
    def set_channel(self, channel):
        self._channel = channel
        print(f"电视频道切换至 {self._channel}")


class Radio(Device):
    """收音机设备 - 具体实现"""
    
    def __init__(self):
        self._enabled = False
        self._volume = 20
        self._channel = 88.5  # FM频率
    
    def is_enabled(self):
        return self._enabled
    
    def enable(self):
        self._enabled = True
        print("收音机已开启")
    
    def disable(self):
        self._enabled = False
        print("收音机已关闭")
    
    def get_volume(self):
        return self._volume
    
    def set_volume(self, percent):
        if percent > 100:
            self._volume = 100
        elif percent < 0:
            self._volume = 0
        else:
            self._volume = percent
        print(f"收音机音量设置为 {self._volume}%")
    
    def get_channel(self):
        return self._channel
    
    def set_channel(self, channel):
        self._channel = channel
        print(f"收音机调频至 {self._channel} MHz")


# 抽象部分接口
class RemoteControl:
    """遥控器 - 抽象部分"""
    
    def __init__(self, device):
        self.device = device
    
    def toggle_power(self):
        if self.device.is_enabled():
            self.device.disable()
        else:
            self.device.enable()
    
    def volume_up(self):
        self.device.set_volume(self.device.get_volume() + 10)
    
    def volume_down(self):
        self.device.set_volume(self.device.get_volume() - 10)
    
    def channel_up(self):
        self.device.set_channel(self.device.get_channel() + 1)
    
    def channel_down(self):
        self.device.set_channel(self.device.get_channel() - 1)


# 扩展的抽象
class AdvancedRemoteControl(RemoteControl):
    """高级遥控器 - 扩展的抽象"""
    
    def mute(self):
        self.device.set_volume(0)
        print("静音")
    
    def set_channel_direct(self, channel):
        self.device.set_channel(channel)


class VoiceRemoteControl(RemoteControl):
    """语音遥控器 - 另一种扩展的抽象"""
    
    def process_voice_command(self, command):
        print(f"接收到语音命令: '{command}'")
        
        if "开机" in command or "打开" in command:
            self.device.enable()
        elif "关机" in command or "关闭" in command:
            self.device.disable()
        elif "增大音量" in command or "音量大" in command:
            self.volume_up()
        elif "减小音量" in command or "音量小" in command:
            self.volume_down()
        elif "静音" in command:
            self.device.set_volume(0)
        elif "下一个" in command or "频道增加" in command:
            self.channel_up()
        elif "上一个" in command or "频道减少" in command:
            self.channel_down()
        elif "频道" in command:
            # 解析命令中的频道号
            try:
                channel = float(command.split("频道")[1].strip())
                self.device.set_channel(channel)
            except:
                print("无法识别频道号")
        else:
            print("无法识别的命令")


# 客户端代码
if __name__ == "__main__":
    # 使用普通遥控器控制电视
    tv = Television()
    remote = RemoteControl(tv)
    
    remote.toggle_power()  # 开机
    remote.volume_up()     # 增大音量
    remote.volume_up()     # 再次增大音量
    remote.channel_up()    # 下一个频道
    remote.toggle_power()  # 关机
    
    print("\n" + "-" * 50 + "\n")
    
    # 使用高级遥控器控制收音机
    radio = Radio()
    advanced_remote = AdvancedRemoteControl(radio)
    
    advanced_remote.toggle_power()  # 开启
    advanced_remote.volume_up()     # 增大音量
    advanced_remote.set_channel_direct(104.5)  # 直接设置频道
    advanced_remote.mute()          # 静音
    advanced_remote.toggle_power()  # 关闭
    
    print("\n" + "-" * 50 + "\n")
    
    # 使用语音遥控器控制电视
    tv = Television()
    voice_remote = VoiceRemoteControl(tv)
    
    voice_remote.process_voice_command("打开电视")
    voice_remote.process_voice_command("增大音量")
    voice_remote.process_voice_command("频道 5")
    voice_remote.process_voice_command("关闭电视")
    
    print("\n" + "-" * 50 + "\n")
    
    # 演示桥接模式的灵活性 - 在运行时切换设备
    print("演示桥接模式的灵活性 - 相同的遥控器控制不同的设备:")
    
    tv = Television()
    radio = Radio()
    
    # 创建一个遥控器
    remote = AdvancedRemoteControl(tv)
    
    # 控制电视
    print("\n控制电视:")
    remote.toggle_power()
    remote.set_channel_direct(10)
    remote.mute()
    
    # 切换到控制收音机
    print("\n切换到控制收音机:")
    remote.device = radio  # 在运行时切换实现
    
    remote.toggle_power()
    remote.set_channel_direct(98.5)
    remote.mute()
