#!/usr/bin/env python3
"""
智能体基础类
为TradingAgents框架提供统一的智能体基类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import logging


class AgentNode(ABC):
    """
    智能体节点基类
    所有智能体节点都应该继承此类
    """
    
    def __init__(self, name: str):
        """
        初始化智能体节点
        
        Args:
            name: 智能体名称
        """
        self.name = name
        self.logger = logging.getLogger(f"agent.{name}")
    
    @abstractmethod
    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理输入消息并返回结果
        
        Args:
            message: 输入消息字典
            
        Returns:
            处理结果字典
        """
        pass
    
    def get_name(self) -> str:
        """
        获取智能体名称
        
        Returns:
            智能体名称
        """
        return self.name
    
    def log_info(self, message: str):
        """记录信息日志"""
        self.logger.info(f"[{self.name}] {message}")
    
    def log_error(self, message: str):
        """记录错误日志"""
        self.logger.error(f"[{self.name}] {message}")
    
    def log_warning(self, message: str):
        """记录警告日志"""
        self.logger.warning(f"[{self.name}] {message}")


class BaseAgent(AgentNode):
    """
    基础智能体类
    提供更多通用功能的智能体基类
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(name)
        self.config = config or {}
        self.state = {}
    
    def update_state(self, key: str, value: Any):
        """更新智能体状态"""
        self.state[key] = value
        self.log_info(f"状态更新: {key} = {value}")
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """获取智能体状态"""
        return self.state.get(key, default)
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self.config.get(key, default)