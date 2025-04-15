"""
建造者模式使用场景：
1. 需要构建复杂对象，且对象的构建过程需要分步骤进行。
2. 需要构建的对象的类型和内容经常变化，但构建的步骤相对稳定。
3. 需要避免使用构造函数来构建复杂对象，因为构造函数参数过多，难以管理。

建造者模式示例 - 构建电脑

本示例展示如何使用建造者模式来构建复杂的电脑对象，
电脑由多个组件组成（CPU、内存、存储等），使用建造者模式可以分步骤构建。
"""

from abc import ABC, abstractmethod


class Computer:
    """要构建的产品 - 电脑类"""
    
    def __init__(self):
        self.cpu = None
        self.memory = None
        self.storage = None
        self.gpu = None
        
    def __str__(self):
        return f"Computer [CPU: {self.cpu}, Memory: {self.memory}, Storage: {self.storage}, GPU: {self.gpu or 'None'}]"


class ComputerBuilder(ABC):
    """抽象建造者接口"""
    
    def __init__(self):
        self.computer = Computer()
        
    @abstractmethod
    def build_cpu(self):
        pass
    
    @abstractmethod
    def build_memory(self):
        pass
    
    @abstractmethod
    def build_storage(self):
        pass
    
    @abstractmethod
    def build_gpu(self):
        pass
    
    def get_computer(self):
        return self.computer


class GamingComputerBuilder(ComputerBuilder):
    """具体建造者 - 游戏电脑"""
    
    def build_cpu(self):
        self.computer.cpu = "Intel i9 12900K"
        return self
    
    def build_memory(self):
        self.computer.memory = "32GB DDR5"
        return self
    
    def build_storage(self):
        self.computer.storage = "2TB NVMe SSD"
        return self
    
    def build_gpu(self):
        self.computer.gpu = "NVIDIA RTX 4090"
        return self


class OfficeComputerBuilder(ComputerBuilder):
    """具体建造者 - 办公电脑"""
    
    def build_cpu(self):
        self.computer.cpu = "Intel i5 12400"
        return self
    
    def build_memory(self):
        self.computer.memory = "16GB DDR4"
        return self
    
    def build_storage(self):
        self.computer.storage = "512GB SSD"
        return self
    
    def build_gpu(self):
        # 办公电脑不需要独立显卡
        return self


class ComputerDirector:
    """指挥者类"""
    
    def __init__(self, builder):
        self.builder = builder
    
    def build_computer(self):
        return self.builder.build_cpu().build_memory().build_storage().build_gpu().get_computer()
    
    def build_minimal_computer(self):
        return self.builder.build_cpu().build_memory().build_storage().get_computer()


# 客户端代码
if __name__ == "__main__":
    # 创建游戏电脑
    gaming_builder = GamingComputerBuilder()
    director = ComputerDirector(gaming_builder)
    gaming_pc = director.build_computer()
    print("Gaming PC:", gaming_pc)
    
    # 创建办公电脑
    office_builder = OfficeComputerBuilder()
    director = ComputerDirector(office_builder)
    office_pc = director.build_minimal_computer()
    print("Office PC:", office_pc)
    
    # 直接使用建造者（不使用指挥者）
    custom_pc = GamingComputerBuilder().build_cpu().build_memory().build_gpu().get_computer()  # 注意：没有存储设备
    print("Custom PC (without storage):", custom_pc)
