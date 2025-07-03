#!/usr/bin/env python3
"""
工具基类
为TradingAgents框架提供统一的工具接口
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging


class BaseTool(ABC):
    """
    工具基类
    所有工具都应该继承此类
    """
    
    def __init__(self, name: str, description: str):
        """
        初始化工具
        
        Args:
            name: 工具名称
            description: 工具描述
        """
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"tool.{name}")
    
    @abstractmethod
    async def run(self, *args, **kwargs) -> str:
        """
        异步执行工具
        
        Returns:
            工具执行结果字符串
        """
        pass
    
    def sync_run(self, *args, **kwargs) -> str:
        """
        同步执行工具
        
        Returns:
            工具执行结果字符串
        """
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果已经在事件循环中，创建新的任务
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.run(*args, **kwargs))
                    return future.result()
            else:
                return loop.run_until_complete(self.run(*args, **kwargs))
        except Exception:
            return asyncio.run(self.run(*args, **kwargs))
    
    def get_info(self) -> Dict[str, str]:
        """
        获取工具信息
        
        Returns:
            包含工具名称和描述的字典
        """
        return {
            "name": self.name,
            "description": self.description
        }
    
    def log_info(self, message: str):
        """记录信息日志"""
        self.logger.info(f"[{self.name}] {message}")
    
    def log_error(self, message: str):
        """记录错误日志"""
        self.logger.error(f"[{self.name}] {message}")
    
    def log_warning(self, message: str):
        """记录警告日志"""
        self.logger.warning(f"[{self.name}] {message}")