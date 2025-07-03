#!/usr/bin/env python3
"""
DeepSeek LLM适配器
提供与LangChain兼容的DeepSeek API接口
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional, Union, Iterator

import requests
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.outputs import LLMResult, Generation
from pydantic import Field

logger = logging.getLogger(__name__)


class DeepSeekLLM(LLM):
    """
    DeepSeek LLM适配器
    
    支持DeepSeek API的LangChain兼容接口
    """
    
    model_name: str = Field(default="deepseek-chat")
    api_key: str = Field(default="")
    base_url: str = Field(default="https://api.deepseek.com")
    max_tokens: int = Field(default=4000)
    temperature: float = Field(default=0.7)
    top_p: float = Field(default=0.95)
    enable_stream: bool = Field(default=False, alias="stream")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 从环境变量获取API密钥
        if not self.api_key:
            self.api_key = os.getenv("DEEPSEEK_API_KEY", "")
        
        if not self.api_key:
            logger.warning("DeepSeek API密钥未设置，请设置DEEPSEEK_API_KEY环境变量")
    
    @property
    def _llm_type(self) -> str:
        return "deepseek"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        调用DeepSeek API生成回复
        """
        try:
            # 构建请求消息
            messages = [{"role": "user", "content": prompt}]
            
            # 调用API
            response = self._make_request(messages, **kwargs)
            
            if response and "choices" in response and len(response["choices"]) > 0:
                return response["choices"][0]["message"]["content"]
            else:
                logger.error(f"DeepSeek API返回格式异常: {response}")
                return "API调用失败，请检查配置"
                
        except Exception as e:
            logger.error(f"DeepSeek API调用失败: {e}")
            return f"API调用失败: {str(e)}"
    
    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """
        批量生成回复
        """
        generations = []
        
        for prompt in prompts:
            try:
                text = self._call(prompt, stop=stop, run_manager=run_manager, **kwargs)
                generations.append([Generation(text=text)])
            except Exception as e:
                logger.error(f"生成回复失败: {e}")
                generations.append([Generation(text=f"生成失败: {str(e)}")])
        
        return LLMResult(generations=generations)
    
    async def _agenerate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """
        异步批量生成回复
        """
        # 简单实现：调用同步版本
        return self._generate(prompts, stop=stop, run_manager=run_manager, **kwargs)
    
    def _make_request(self, messages: List[Dict], **kwargs) -> Dict:
        """
        发送请求到DeepSeek API
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 合并参数
        params = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            "top_p": kwargs.get("top_p", self.top_p),
            "stream": kwargs.get("stream", self.enable_stream)
        }
        
        # 移除None值
        params = {k: v for k, v in params.items() if v is not None}
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=params,
                timeout=60
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"DeepSeek API请求失败: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    logger.error(f"API错误详情: {error_detail}")
                except:
                    logger.error(f"API响应状态码: {e.response.status_code}")
            raise
    
    def convert_langchain_messages(self, messages: List[BaseMessage]) -> List[Dict]:
        """
        将LangChain消息格式转换为DeepSeek API格式
        """
        converted_messages = []
        
        for message in messages:
            if isinstance(message, SystemMessage):
                converted_messages.append({
                    "role": "system",
                    "content": message.content
                })
            elif isinstance(message, HumanMessage):
                converted_messages.append({
                    "role": "user",
                    "content": message.content
                })
            elif isinstance(message, AIMessage):
                converted_messages.append({
                    "role": "assistant",
                    "content": message.content
                })
            else:
                # 默认作为用户消息处理
                converted_messages.append({
                    "role": "user",
                    "content": str(message.content)
                })
        
        return converted_messages
    
    def chat_with_messages(
        self, 
        messages: List[BaseMessage], 
        **kwargs
    ) -> str:
        """
        使用LangChain消息格式进行对话
        """
        try:
            # 转换消息格式
            api_messages = self.convert_langchain_messages(messages)
            
            # 调用API
            response = self._make_request(api_messages, **kwargs)
            
            if response and "choices" in response and len(response["choices"]) > 0:
                return response["choices"][0]["message"]["content"]
            else:
                logger.error(f"DeepSeek API返回格式异常: {response}")
                return "API调用失败，请检查配置"
                
        except Exception as e:
            logger.error(f"DeepSeek聊天调用失败: {e}")
            return f"聊天调用失败: {str(e)}"
    
    def bind_tools(self, tools: List[Any]) -> "DeepSeekLLM":
        """
        绑定工具（DeepSeek暂不支持工具调用，返回自身）
        """
        logger.warning("DeepSeek暂不支持工具调用功能")
        return self
    
    def get_token_count(self, text: str) -> int:
        """
        估算token数量（简单实现）
        """
        # 简单估算：中文按字符数，英文按单词数*1.3
        chinese_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
        english_chars = len(text) - chinese_chars
        english_words = len(text.split()) if english_chars > chinese_chars else 0
        
        return chinese_chars + int(english_words * 1.3)
    
    def get_num_tokens(self, text: str) -> int:
        """
        获取文本的token数量（LangChain兼容方法）
        """
        return self.get_token_count(text)
    
    def validate_api_key(self) -> bool:
        """
        验证API密钥是否有效
        """
        if not self.api_key:
            return False
        
        try:
            # 发送一个简单的测试请求
            test_messages = [{"role": "user", "content": "Hello"}]
            response = self._make_request(test_messages, max_tokens=10)
            return "choices" in response and len(response["choices"]) > 0
        except Exception as e:
            logger.error(f"API密钥验证失败: {e}")
            return False


def create_deepseek_llm(
    model_name: str = "deepseek-chat",
    api_key: str = "",
    base_url: str = "https://api.deepseek.com",
    max_tokens: int = 4000,
    temperature: float = 0.7,
    **kwargs
) -> DeepSeekLLM:
    """
    创建DeepSeek LLM实例的便捷函数
    
    Args:
        model_name: 模型名称，默认为"deepseek-chat"
        api_key: API密钥
        base_url: API基础URL
        max_tokens: 最大token数
        temperature: 温度参数
        **kwargs: 其他参数
    
    Returns:
        DeepSeekLLM实例
    """
    return DeepSeekLLM(
        model_name=model_name,
        api_key=api_key,
        base_url=base_url,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs
    )


# 导出主要类和函数
__all__ = ["DeepSeekLLM", "create_deepseek_llm"]