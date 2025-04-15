#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


# 抽象产品
class Product(ABC):
    @abstractmethod
    def operation(self) -> str:
        pass


# 具体产品A
class ConcreteProductA(Product):
    def operation(self) -> str:
        return "产品A的操作结果"


# 具体产品B
class ConcreteProductB(Product):
    def operation(self) -> str:
        return "产品B的操作结果"


# 简单工厂类
class SimpleFactory:
    @staticmethod
    def create_product(product_type: str) -> Product:
        """
        根据产品类型创建具体产品实例
        
        Args:
            product_type: 产品类型标识符
            
        Returns:
            Product: 具体产品实例
            
        Raises:
            ValueError: 当产品类型不支持时抛出
        """
        if product_type == "A":
            return ConcreteProductA()
        elif product_type == "B":
            return ConcreteProductB()
        else:
            raise ValueError(f"不支持的产品类型: {product_type}")


# 客户端代码
if __name__ == "__main__":
    # 使用简单工厂创建产品
    factory = SimpleFactory()
    
    # 创建并使用产品A
    product_a = factory.create_product("A")
    print(f"产品A: {product_a.operation()}")
    
    # 创建并使用产品B
    product_b = factory.create_product("B")
    print(f"产品B: {product_b.operation()}")
    
    # 测试异常情况
    try:
        factory.create_product("C")
    except ValueError as e:
        print(f"错误: {e}")
