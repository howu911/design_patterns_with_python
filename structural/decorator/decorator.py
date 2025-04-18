"""
装饰器模式使用场景：
1. 需要在不修改现有对象结构的情况下，动态地添加功能
2. 需要为对象添加的功能可以动态地组合搭配
3. 希望通过分离职责来保持类的简洁性，而不是通过继承添加功能
4. 当使用继承扩展功能会导致子类数量剧增时（组合爆炸）
5. 当需要在运行时根据条件决定对象的功能时

装饰器模式示例 - 文本处理系统

本示例展示如何使用装饰器模式来设计一个灵活的文本处理系统，
可以动态地为文本添加各种格式化功能，如加粗、斜体、添加前缀等。
"""

from abc import ABC, abstractmethod


# 抽象组件接口
class TextComponent(ABC):
    """文本组件接口 - 定义所有具体组件和装饰器的共同接口"""
    
    @abstractmethod
    def get_text(self):
        """获取文本内容"""
        pass


# 具体组件
class PlainText(TextComponent):
    """具体组件 - 基础文本，不包含任何格式"""
    
    def __init__(self, text):
        self.text = text
    
    def get_text(self):
        return self.text


# 装饰器基类
class TextDecorator(TextComponent):
    """装饰器基类 - 包含对组件的引用，并实现基础接口"""
    
    def __init__(self, text_component):
        self._text_component = text_component
    
    @abstractmethod
    def get_text(self):
        pass


# 具体装饰器 - 加粗
class BoldDecorator(TextDecorator):
    """具体装饰器 - 为文本添加加粗格式"""
    
    def get_text(self):
        return f"<b>{self._text_component.get_text()}</b>"


# 具体装饰器 - 斜体
class ItalicDecorator(TextDecorator):
    """具体装饰器 - 为文本添加斜体格式"""
    
    def get_text(self):
        return f"<i>{self._text_component.get_text()}</i>"


# 具体装饰器 - 下划线
class UnderlineDecorator(TextDecorator):
    """具体装饰器 - 为文本添加下划线格式"""
    
    def get_text(self):
        return f"<u>{self._text_component.get_text()}</u>"


# 具体装饰器 - 颜色
class ColorDecorator(TextDecorator):
    """具体装饰器 - 为文本添加颜色"""
    
    def __init__(self, text_component, color):
        super().__init__(text_component)
        self.color = color
    
    def get_text(self):
        return f'<span style="color:{self.color}">{self._text_component.get_text()}</span>'


# 具体装饰器 - 添加前缀
class PrefixDecorator(TextDecorator):
    """具体装饰器 - 为文本添加前缀"""
    
    def __init__(self, text_component, prefix):
        super().__init__(text_component)
        self.prefix = prefix
    
    def get_text(self):
        return f"{self.prefix} {self._text_component.get_text()}"


# 具体装饰器 - 添加后缀
class SuffixDecorator(TextDecorator):
    """具体装饰器 - 为文本添加后缀"""
    
    def __init__(self, text_component, suffix):
        super().__init__(text_component)
        self.suffix = suffix
    
    def get_text(self):
        return f"{self._text_component.get_text()} {self.suffix}"


# 具体装饰器 - 转换为大写
class UpperCaseDecorator(TextDecorator):
    """具体装饰器 - 将文本转换为大写"""
    
    def get_text(self):
        return self._text_component.get_text().upper()


# 具体装饰器 - 转换为小写
class LowerCaseDecorator(TextDecorator):
    """具体装饰器 - 将文本转换为小写"""
    
    def get_text(self):
        return self._text_component.get_text().lower()


# 应用场景 - 文本编辑器
class TextEditor:
    """文本编辑器 - 使用装饰器模式处理文本"""
    
    def __init__(self):
        self.formats = []
    
    def create_formatted_text(self, text, formats):
        """根据指定的格式创建文本"""
        text_component = PlainText(text)
        
        for format_name, *args in formats:
            if format_name == "bold":
                text_component = BoldDecorator(text_component)
            elif format_name == "italic":
                text_component = ItalicDecorator(text_component)
            elif format_name == "underline":
                text_component = UnderlineDecorator(text_component)
            elif format_name == "color":
                text_component = ColorDecorator(text_component, args[0])
            elif format_name == "prefix":
                text_component = PrefixDecorator(text_component, args[0])
            elif format_name == "suffix":
                text_component = SuffixDecorator(text_component, args[0])
            elif format_name == "uppercase":
                text_component = UpperCaseDecorator(text_component)
            elif format_name == "lowercase":
                text_component = LowerCaseDecorator(text_component)
        
        return text_component.get_text()


# 客户端代码
if __name__ == "__main__":
    print("=== 装饰器模式演示 - 基础示例 ===")
    
    # 创建基础文本
    simple_text = PlainText("Hello, World!")
    print(f"原始文本: {simple_text.get_text()}")
    
    # 使用单个装饰器
    bold_text = BoldDecorator(simple_text)
    print(f"加粗文本: {bold_text.get_text()}")
    
    # 组合多个装饰器
    italic_bold_text = ItalicDecorator(bold_text)
    print(f"加粗+斜体: {italic_bold_text.get_text()}")
    
    # 更复杂的组合
    decorated_text = UnderlineDecorator(
        ColorDecorator(
            ItalicDecorator(
                BoldDecorator(
                    PlainText("装饰器模式")
                )
            ),
            "red"
        )
    )
    print(f"多重装饰: {decorated_text.get_text()}")
    
    # 使用前缀和后缀装饰器
    prefixed_suffixed_text = SuffixDecorator(
        PrefixDecorator(
            PlainText("核心内容"),
            "开始:"
        ),
        ":结束"
    )
    print(f"带前后缀: {prefixed_suffixed_text.get_text()}")
    
    print("\n=== 装饰器模式应用 - 文本编辑器 ===")
    
    # 使用文本编辑器创建格式化文本
    editor = TextEditor()
    
    # 创建标题文本
    title = editor.create_formatted_text(
        "欢迎使用文本编辑器",
        [
            ("bold",),
            ("color", "blue"),
            ("underline",),
        ]
    )
    print(f"标题: {title}")
    
    # 创建引用文本
    quote = editor.create_formatted_text(
        "这是一段引用的文字",
        [
            ("italic",),
            ("prefix", "引用:"),
            ("color", "gray"),
        ]
    )
    print(f"引用: {quote}")
    
    # 创建警告文本
    warning = editor.create_formatted_text(
        "注意!",
        [
            ("uppercase",),
            ("bold",),
            ("color", "red"),
            ("suffix", "- 重要警告"),
        ]
    )
    print(f"警告: {warning}")
    
    print("\n=== 装饰器模式的灵活性 ===")
    
    # 根据条件动态添加装饰器
    def generate_formatted_text(text, is_important, is_quote, color=None):
        component = PlainText(text)
        
        if is_important:
            component = BoldDecorator(component)
            if color is None:
                color = "red"  # 重要文本默认使用红色
        
        if is_quote:
            component = ItalicDecorator(component)
            component = PrefixDecorator(component, "引用:")
        
        if color:
            component = ColorDecorator(component, color)
        
        return component.get_text()
    
    # 测试不同组合
    print("普通文本:", generate_formatted_text("普通文本", False, False))
    print("重要文本:", generate_formatted_text("重要文本", True, False))
    print("引用文本:", generate_formatted_text("引用文本", False, True))
    print("重要引用+自定义颜色:", generate_formatted_text("重要引用文本", True, True, "purple"))
