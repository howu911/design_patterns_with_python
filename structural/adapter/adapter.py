"""
适配器模式使用场景：
1. 需要使用现有的类，但其接口与应用程序的需求不匹配
2. 希望创建一个可复用的类，该类可以与不相关或不可预见的类协同工作
3. 需要使用多个现有子类，但不能通过子类化每一个子类来适配它们的接口
4. 需要集成第三方库或遗留系统，但无法修改其源代码
5. 在系统重构过程中，需要保持原有接口不变的同时适配新接口

适配器模式示例 - 支付系统集成

本示例展示如何使用适配器模式来集成不同的支付网关，
使得应用程序可以通过统一的接口调用不同的支付服务。
"""

from abc import ABC, abstractmethod
import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass


# 目标接口 - 应用程序期望的接口
class PaymentProcessor(ABC):
    """支付处理器接口 - 目标接口"""
    
    @abstractmethod
    def process_payment(self, amount, card_number, expiry_date, cvv):
        """处理支付"""
        pass
    
    @abstractmethod
    def refund_payment(self, payment_id, amount=None):
        """退款"""
        pass
    
    @abstractmethod
    def check_payment_status(self, payment_id):
        """查询支付状态"""
        pass


# 客户端代码 - 使用目标接口
class PaymentService:
    """支付服务 - 客户端"""
    
    def __init__(self, payment_processor):
        self.payment_processor = payment_processor
    
    def make_payment(self, amount, card_details):
        """使用支付处理器进行支付"""
        return self.payment_processor.process_payment(
            amount,
            card_details["card_number"],
            card_details["expiry_date"],
            card_details["cvv"]
        )
    
    def request_refund(self, payment_id, amount=None):
        """请求退款"""
        return self.payment_processor.refund_payment(payment_id, amount)
    
    def get_payment_status(self, payment_id):
        """获取支付状态"""
        return self.payment_processor.check_payment_status(payment_id)


# 被适配者 - 现有的JSON格式支付网关
class JsonPaymentGateway:
    """JSON格式支付网关 - 被适配者"""
    
    def __init__(self, merchant_id, api_key):
        self.merchant_id = merchant_id
        self.api_key = api_key
    
    def submit_payment_json(self, payment_data):
        """提交支付数据 (JSON格式)"""
        # 这里模拟发送数据到支付网关
        print(f"JsonPaymentGateway: 发送支付请求，商户ID: {self.merchant_id}")
        print(f"支付数据: {payment_data}")
        
        # 模拟成功响应
        response = {
            "status": "success",
            "payment_id": "json_" + str(hash(payment_data["card"]["number"]))[1:8],
            "transaction_time": "2023-10-01T12:30:45Z"
        }
        return response
    
    def request_refund_json(self, refund_data):
        """请求退款 (JSON格式)"""
        print(f"JsonPaymentGateway: 发送退款请求，商户ID: {self.merchant_id}")
        print(f"退款数据: {refund_data}")
        
        # 模拟成功响应
        response = {
            "status": "success",
            "refund_id": "ref_" + refund_data["payment_id"][4:],
            "refund_time": "2023-10-02T10:15:30Z"
        }
        return response
    
    def check_status_json(self, payment_id):
        """查询支付状态 (JSON格式)"""
        print(f"JsonPaymentGateway: 查询支付状态，ID: {payment_id}")
        
        # 模拟状态响应
        response = {
            "payment_id": payment_id,
            "status": "completed",
            "amount": "###.##",  # 实际中会有真实金额
            "processed_at": "2023-10-01T12:30:45Z"
        }
        return response


# 被适配者 - 现有的XML格式支付网关
class XmlPaymentGateway:
    """XML格式支付网关 - 被适配者"""
    
    def __init__(self, api_key, merchant_code):
        self.api_key = api_key
        self.merchant_code = merchant_code
    
    def send_payment_request(self, card_num, exp_date, security_code, amount):
        """发送支付请求 (XML格式)"""
        # 构建XML请求
        xml_request = f"""
        <PaymentRequest>
            <MerchantCode>{self.merchant_code}</MerchantCode>
            <Authentication>{self.api_key}</Authentication>
            <CardDetails>
                <CardNumber>{card_num}</CardNumber>
                <ExpiryDate>{exp_date}</ExpiryDate>
                <SecurityCode>{security_code}</SecurityCode>
            </CardDetails>
            <TransactionDetails>
                <Amount>{amount}</Amount>
                <Currency>CNY</Currency>
            </TransactionDetails>
        </PaymentRequest>
        """
        
        print(f"XmlPaymentGateway: 发送支付请求，商户代码: {self.merchant_code}")
        print(f"XML请求: {xml_request}")
        
        # 模拟XML响应
        xml_response = f"""
        <PaymentResponse>
            <Status>Success</Status>
            <PaymentID>xml_{str(hash(card_num))[1:8]}</PaymentID>
            <TransactionTime>2023-10-01T12:45:30Z</TransactionTime>
        </PaymentResponse>
        """
        
        # 解析XML响应
        root = ET.fromstring(xml_response)
        response = {
            "status": root.find("Status").text.lower(),
            "payment_id": root.find("PaymentID").text,
            "transaction_time": root.find("TransactionTime").text
        }
        
        return response
    
    def process_refund(self, payment_id, refund_amount=None):
        """处理退款请求 (XML格式)"""
        # 构建XML请求
        xml_request = f"""
        <RefundRequest>
            <MerchantCode>{self.merchant_code}</MerchantCode>
            <Authentication>{self.api_key}</Authentication>
            <PaymentID>{payment_id}</PaymentID>
            {"<Amount>" + str(refund_amount) + "</Amount>" if refund_amount else "<FullRefund>true</FullRefund>"}
        </RefundRequest>
        """
        
        print(f"XmlPaymentGateway: 发送退款请求，支付ID: {payment_id}")
        print(f"XML请求: {xml_request}")
        
        # 模拟XML响应
        xml_response = f"""
        <RefundResponse>
            <Status>Success</Status>
            <RefundID>ref_{payment_id[4:]}</RefundID>
            <RefundTime>2023-10-02T15:20:10Z</RefundTime>
        </RefundResponse>
        """
        
        # 解析XML响应
        root = ET.fromstring(xml_response)
        response = {
            "status": root.find("Status").text.lower(),
            "refund_id": root.find("RefundID").text,
            "refund_time": root.find("RefundTime").text
        }
        
        return response
    
    def get_payment_info(self, payment_id):
        """获取支付信息 (XML格式)"""
        # 构建XML请求
        xml_request = f"""
        <StatusRequest>
            <MerchantCode>{self.merchant_code}</MerchantCode>
            <Authentication>{self.api_key}</Authentication>
            <PaymentID>{payment_id}</PaymentID>
        </StatusRequest>
        """
        
        print(f"XmlPaymentGateway: 查询支付状态，ID: {payment_id}")
        print(f"XML请求: {xml_request}")
        
        # 模拟XML响应
        xml_response = f"""
        <StatusResponse>
            <PaymentID>{payment_id}</PaymentID>
            <Status>Completed</Status>
            <Amount>###.##</Amount>
            <ProcessedAt>2023-10-01T12:45:30Z</ProcessedAt>
        </StatusResponse>
        """
        
        # 解析XML响应
        root = ET.fromstring(xml_response)
        response = {
            "payment_id": root.find("PaymentID").text,
            "status": root.find("Status").text.lower(),
            "amount": root.find("Amount").text,
            "processed_at": root.find("ProcessedAt").text
        }
        
        return response


# 适配器 - 将JSON支付网关适配到目标接口
class JsonPaymentAdapter(PaymentProcessor):
    """JSON支付网关适配器 - 适配器"""
    
    def __init__(self, json_gateway):
        self.json_gateway = json_gateway
    
    def process_payment(self, amount, card_number, expiry_date, cvv):
        """适配JSON网关的支付方法"""
        # 转换数据格式
        payment_data = {
            "card": {
                "number": card_number,
                "expiry": expiry_date,
                "cvv": cvv
            },
            "transaction": {
                "amount": amount,
                "currency": "CNY"
            }
        }
        
        # 调用JSON网关的方法
        return self.json_gateway.submit_payment_json(payment_data)
    
    def refund_payment(self, payment_id, amount=None):
        """适配JSON网关的退款方法"""
        refund_data = {
            "payment_id": payment_id,
            "full_refund": amount is None
        }
        
        if amount:
            refund_data["amount"] = amount
        
        return self.json_gateway.request_refund_json(refund_data)
    
    def check_payment_status(self, payment_id):
        """适配JSON网关的状态查询方法"""
        return self.json_gateway.check_status_json(payment_id)


# 适配器 - 将XML支付网关适配到目标接口
class XmlPaymentAdapter(PaymentProcessor):
    """XML支付网关适配器 - 适配器"""
    
    def __init__(self, xml_gateway):
        self.xml_gateway = xml_gateway
    
    def process_payment(self, amount, card_number, expiry_date, cvv):
        """适配XML网关的支付方法"""
        return self.xml_gateway.send_payment_request(
            card_number, expiry_date, cvv, amount
        )
    
    def refund_payment(self, payment_id, amount=None):
        """适配XML网关的退款方法"""
        return self.xml_gateway.process_refund(payment_id, amount)
    
    def check_payment_status(self, payment_id):
        """适配XML网关的状态查询方法"""
        return self.xml_gateway.get_payment_info(payment_id)


# 客户端代码
if __name__ == "__main__":
    print("=== 适配器模式演示 - 支付系统 ===")
    
    # 创建被适配者实例
    json_gateway = JsonPaymentGateway("merchant123", "secret_key_json")
    xml_gateway = XmlPaymentGateway("secret_key_xml", "merchant456")
    
    # 创建适配器
    json_adapter = JsonPaymentAdapter(json_gateway)
    xml_adapter = XmlPaymentAdapter(xml_gateway)
    
    # 模拟支付信息
    test_amount = 199.99
    test_card = {
        "card_number": "1234 5678 9012 3456",
        "expiry_date": "12/25",
        "cvv": "123"
    }
    
    print("\n--- 使用JSON支付网关 ---")
    # 创建支付服务并使用JSON适配器
    payment_service = PaymentService(json_adapter)
    
    # 进行支付
    json_payment_result = payment_service.make_payment(test_amount, test_card)
    print(f"支付结果: {json_payment_result}")
    
    # 查询状态
    json_payment_id = json_payment_result["payment_id"]
    json_status = payment_service.get_payment_status(json_payment_id)
    print(f"支付状态: {json_status}")
    
    # 退款
    json_refund = payment_service.request_refund(json_payment_id)
    print(f"退款结果: {json_refund}")
    
    print("\n--- 使用XML支付网关 ---")
    # 切换到XML适配器
    payment_service.payment_processor = xml_adapter
    
    # 进行支付
    xml_payment_result = payment_service.make_payment(test_amount, test_card)
    print(f"支付结果: {xml_payment_result}")
    
    # 查询状态
    xml_payment_id = xml_payment_result["payment_id"]
    xml_status = payment_service.get_payment_status(xml_payment_id)
    print(f"支付状态: {xml_status}")
    
    # 部分退款
    xml_refund = payment_service.request_refund(xml_payment_id, 50.00)
    print(f"退款结果: {xml_refund}")
    
    print("\n=== 适配器模式优势 ===")
    print("1. 统一接口: 客户端代码(PaymentService)使用统一的接口(PaymentProcessor)，无需关心底层支付网关的差异")
    print("2. 系统解耦: 当需要集成新的支付网关时，只需创建新的适配器，无需修改现有代码")
    print("3. 兼容性: 可以集成具有不同接口、数据格式的第三方系统")
    print("4. 可维护性: 适配逻辑集中在适配器中，便于管理和维护")
