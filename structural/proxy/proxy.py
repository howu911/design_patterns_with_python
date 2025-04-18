"""
代理模式使用场景：
1. 控制对原始对象的访问 - 代理可以在访问原始对象前执行额外的验证或权限检查
2. 延迟初始化（虚拟代理）- 对于创建成本高的对象，代理可以延迟到真正需要时才创建
3. 远程代理 - 为远程对象提供本地代表
4. 日志记录代理 - 在访问对象前后添加日志记录
5. 缓存代理 - 在代理中缓存结果，避免重复执行开销大的操作

代理模式示例 - 文件访问控制系统

本示例展示如何使用代理模式来控制对敏感文件的访问，
代理会在访问前进行权限验证，并记录访问日志。
"""

from abc import ABC, abstractmethod
import time


# 抽象主题接口
class FileAccess(ABC):
    """文件访问接口 - 抽象主题"""
    
    @abstractmethod
    def read_file(self, filename):
        pass
    
    @abstractmethod
    def write_file(self, filename, content):
        pass


# 真实主题
class RealFileAccess(FileAccess):
    """真实的文件访问类 - 实际执行文件操作"""
    
    def read_file(self, filename):
        print(f"读取文件 {filename} 的内容")
        return f"{filename} 的内容：这是一些敏感数据..."
    
    def write_file(self, filename, content):
        print(f"向文件 {filename} 写入内容")
        return f"成功写入内容到 {filename}"


# 代理类
class FileAccessProxy(FileAccess):
    """文件访问代理 - 在访问真实对象前进行权限验证和日志记录"""
    
    def __init__(self, user_role):
        self._real_file_access = None  # 延迟初始化
        self.user_role = user_role
        self.access_log = []
    
    def _check_access(self, filename, operation):
        """验证用户是否有权限访问文件"""
        if self.user_role == "admin":
            return True
        
        if operation == "read" and (self.user_role == "user" and not filename.startswith("confidential_")):
            return True
        
        if operation == "write" and self.user_role == "editor":
            return True
        
        return False
    
    def _log_access(self, filename, operation, success):
        """记录访问日志"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - 用户角色: {self.user_role}, 操作: {operation}, 文件: {filename}, 结果: {'成功' if success else '拒绝'}"
        self.access_log.append(log_entry)
    
    def _get_real_file_access(self):
        """延迟初始化真实主题对象"""
        if self._real_file_access is None:
            self._real_file_access = RealFileAccess()
        return self._real_file_access
    
    def read_file(self, filename):
        if self._check_access(filename, "read"):
            result = self._get_real_file_access().read_file(filename)
            self._log_access(filename, "read", True)
            return result
        else:
            self._log_access(filename, "read", False)
            return f"拒绝访问：您没有读取 {filename} 的权限"
    
    def write_file(self, filename, content):
        if self._check_access(filename, "write"):
            result = self._get_real_file_access().write_file(filename, content)
            self._log_access(filename, "write", True)
            return result
        else:
            self._log_access(filename, "write", False)
            return f"拒绝访问：您没有写入 {filename} 的权限"
    
    def print_access_log(self):
        """打印访问日志"""
        print("\n=== 访问日志 ===")
        for log in self.access_log:
            print(log)


# 客户端代码
if __name__ == "__main__":
    # 管理员用户 - 有完全权限
    admin_proxy = FileAccessProxy("admin")
    print(admin_proxy.read_file("regular_file.txt"))
    print(admin_proxy.read_file("confidential_data.txt"))
    print(admin_proxy.write_file("system_config.txt", "新配置数据"))
    
    print("\n" + "-" * 50 + "\n")
    
    # 普通用户 - 只能读取非机密文件
    user_proxy = FileAccessProxy("user")
    print(user_proxy.read_file("regular_file.txt"))
    print(user_proxy.read_file("confidential_data.txt"))  # 将被拒绝
    print(user_proxy.write_file("regular_file.txt", "尝试写入"))  # 将被拒绝
    
    print("\n" + "-" * 50 + "\n")
    
    # 编辑用户 - 可以写入但不能读取机密文件
    editor_proxy = FileAccessProxy("editor")
    print(editor_proxy.write_file("article.txt", "这是新文章内容"))
    print(editor_proxy.read_file("confidential_data.txt"))  # 将被拒绝
    
    # 打印所有用户的访问日志
    user_proxy.print_access_log()
