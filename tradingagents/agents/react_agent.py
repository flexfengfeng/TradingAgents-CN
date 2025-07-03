#!/usr/bin/env python3
"""
ReAct Agent实现
为TradingAgents框架提供ReAct模式的智能体
"""

from typing import Dict, Any, List, Optional
import logging
import asyncio
from abc import ABC, abstractmethod


class BaseTool(ABC):
    """
    工具基类
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def run(self, *args, **kwargs) -> str:
        """执行工具"""
        pass


class ReActAgent:
    """
    ReAct Agent实现
    基于Reasoning and Acting模式的智能体
    """
    
    def __init__(self, name: str, system_message: str, tools: List[BaseTool], 
                 model: str = "deepseek", verbose: bool = False):
        self.name = name
        self.system_message = system_message
        self.tools = {tool.name: tool for tool in tools}
        self.model = model
        self.verbose = verbose
        self.logger = logging.getLogger(f"react_agent.{name}")
    
    async def arun(self, query: str) -> Dict[str, Any]:
        """
        异步运行ReAct Agent
        
        Args:
            query: 用户查询
            
        Returns:
            处理结果字典
        """
        try:
            if self.verbose:
                self.logger.info(f"[{self.name}] 开始处理查询: {query}")
            
            # 简化的ReAct实现
            # 在实际项目中，这里应该集成具体的LLM和工具调用逻辑
            result = {
                "content": f"ReAct Agent ({self.name}) 处理查询: {query}\n\n"
                          f"系统消息: {self.system_message}\n\n"
                          f"可用工具: {list(self.tools.keys())}\n\n"
                          f"注意: 这是一个简化的ReAct Agent实现，用于测试目的。",
                "status": "success",
                "model": self.model
            }
            
            if self.verbose:
                self.logger.info(f"[{self.name}] 处理完成")
            
            return result
            
        except Exception as e:
            self.logger.error(f"[{self.name}] 处理失败: {e}", exc_info=True)
            return {
                "content": f"处理失败: {str(e)}",
                "status": "error",
                "model": self.model
            }
    
    def run(self, query: str) -> Dict[str, Any]:
        """
        同步运行ReAct Agent
        
        Args:
            query: 用户查询
            
        Returns:
            处理结果字典
        """
        try:
            # 在同步环境中运行异步方法
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果已经在事件循环中，创建新的任务
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.arun(query))
                    return future.result()
            else:
                return loop.run_until_complete(self.arun(query))
        except Exception as e:
            return asyncio.run(self.arun(query))
    
    def add_tool(self, tool: BaseTool):
        """添加工具"""
        self.tools[tool.name] = tool
        if self.verbose:
            self.logger.info(f"[{self.name}] 添加工具: {tool.name}")
    
    def remove_tool(self, tool_name: str):
        """移除工具"""
        if tool_name in self.tools:
            del self.tools[tool_name]
            if self.verbose:
                self.logger.info(f"[{self.name}] 移除工具: {tool_name}")
    
    def get_tools(self) -> List[str]:
        """获取工具列表"""
        return list(self.tools.keys())