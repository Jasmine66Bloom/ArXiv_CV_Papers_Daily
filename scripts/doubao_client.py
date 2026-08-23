"""豆包大模型 API 客户端封装（支持多种模型，包括 DeepSeek）"""
import time

import requests

from typing import Optional, List, Dict
from dataclasses import dataclass

# 复用连接池，避免每次请求都重新建立TCP连接
_SESSION = requests.Session()


@dataclass
class Message:
    """消息内容"""
    content: str


@dataclass
class Choice:
    """响应选项"""
    message: Message


@dataclass
class DoubaoResponse:
    """豆包/DeepSeek API 响应封装，兼容 OpenAI SDK 格式"""
    choices: List[Choice]
    
    @classmethod
    def from_api_response(cls, response_data: dict) -> "DoubaoResponse":
        """从 API 响应数据创建 DoubaoResponse 对象"""
        try:
            # 新版 chat/completions 接口返回 choices
            choices = response_data.get("choices")
            if choices:
                parsed_choices: List[Choice] = []
                for choice in choices:
                    message = choice.get("message", {})
                    content = message.get("content", "")
                    if isinstance(content, list):
                        # 聚合多段内容
                        parts = []
                        for part in content:
                            if isinstance(part, dict):
                                parts.append(part.get("text", ""))
                            else:
                                parts.append(str(part))
                        content = "".join(parts)
                    parsed_choices.append(Choice(message=Message(content=str(content).strip())))
                return cls(choices=parsed_choices)

            # 兼容旧版 /responses 返回格式
            output = response_data.get("output", [])
            text_parts: List[str] = []
            reasoning_parts: List[str] = []

            def collect_from_content(content_items, target_parts):
                for item in content_items or []:
                    item_type = item.get("type")
                    if item_type in {"output_text", "output_rich_text", "summary_text"}:
                        target_parts.append(item.get("text", ""))

            if isinstance(output, dict):
                message = output.get("message", {})
                collect_from_content(message.get("content", []), text_parts)
            elif isinstance(output, list):
                for block in output:
                    block_type = block.get("type")
                    if block_type == "message":
                        collect_from_content(block.get("content", []), text_parts)
                    elif block_type in {"reasoning", "summary"}:
                        collect_from_content(block.get("summary", []), reasoning_parts)
                    else:
                        collect_from_content(block.get("content", []), text_parts)

            if not text_parts and reasoning_parts:
                text_parts = reasoning_parts

            content = "".join(text_parts).strip()
            return cls(choices=[Choice(message=Message(content=content))])
        except Exception as e:
            raise ValueError(f"解析豆包 API 响应失败: {e}, 响应数据: {response_data}")


class DoubaoCompletions:
    """豆包 Chat Completions 接口封装"""
    
    def __init__(self, client: "DoubaoClient"):
        self.client = client
    
    def create(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        top_p: float = 0.9,
        **kwargs
    ) -> DoubaoResponse:
        """创建对话完成请求（兼容 chat/completions 接口）

        Args:
            messages: 对话消息列表
            model: 模型名称，默认使用客户端配置的模型
        """
        normalized_messages = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if isinstance(content, list):
                normalized_messages.append({"role": role, "content": content})
            else:
                normalized_messages.append({"role": role, "content": str(content)})
        
        payload = {
            "model": model or self.client.model,
            "messages": normalized_messages,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens
        }
        
        # 发送请求
        headers = {
            "Authorization": f"Bearer {self.client.api_key}",
            "Content-Type": "application/json"
        }
        
        # 增强请求的重试机制，避免偶发 EOF/SSL 错误
        max_retries = kwargs.get("max_retries", 3)
        retry_delay = kwargs.get("retry_delay", 2)
        
        for attempt in range(max_retries):
            try:
                response = _SESSION.post(
                    f"{self.client.base_url}/api/v3/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=kwargs.get("timeout", 60)
                )
                
                if response.status_code != 200:
                    raise Exception(f"豆包 API 请求失败: {response.status_code} - {response.text}")
                
                response_data = response.json()
                return DoubaoResponse.from_api_response(response_data)
            except Exception as e:
                if attempt < max_retries - 1:
                    # 指数退避，避免瞬时网络抖动导致长时间阻塞
                    time.sleep(min(retry_delay * (2 ** attempt), 30))
                    continue
                raise


class DoubaoChat:
    """豆包 Chat 接口封装"""
    
    def __init__(self, client: "DoubaoClient"):
        self.completions = DoubaoCompletions(client)


class DoubaoClient:
    """豆包大模型客户端
    
    提供与 OpenAI SDK 兼容的接口，方便替换现有的 ChatGLM 调用。
    
    使用示例:
        client = DoubaoClient(api_key="your-api-key")
        response = client.chat.completions.create(
            model="doubao-seed-1-6-flash-250828",  # 可覆盖客户端配置的模型
            messages=[{"role": "user", "content": "你好"}],
            temperature=0.7,
            max_tokens=100
        )
        print(response.choices[0].message.content)
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "doubao-seed-1-6-flash-250828",
        base_url: str = "https://ark.cn-beijing.volces.com"
    ):
        """初始化豆包客户端
        
        Args:
            api_key: API 密钥
            model: 模型名称，默认为 doubao-seed-1-6-flash-250828
            base_url: API 基础 URL
        """
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.chat = DoubaoChat(self)
