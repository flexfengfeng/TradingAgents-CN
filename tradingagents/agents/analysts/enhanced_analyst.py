#!/usr/bin/env python3
"""
增强分析师节点
集成增强分析工具包到交易代理系统
实现"先精确计算，再交给DeepSeek分析"的完整解决方案
"""

import sys
import os
import json
from typing import Dict, Any, Optional, List, Union, Tuple
from datetime import datetime
import logging

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# 导入增强分析工具包
try:
    from tradingagents.utils.enhanced_analysis_toolkit import EnhancedAnalysisToolkit
except ImportError as e:
    logging.error(f"导入增强分析工具包失败: {e}")
    logging.error("请确保enhanced_analysis_toolkit.py文件在tradingagents.utils目录下")

# 导入必要的交易代理模块
from tradingagents.agents.base import AgentNode
from tradingagents.agents.react_agent import ReActAgent
from tradingagents.agents.tools.base import BaseTool
from tradingagents.agents.tools.stock_data_tool import StockDataTool
from tradingagents.agents.tools.fundamentals_tool import FundamentalsTool
from tradingagents.agents.tools.news_tool import NewsTool
from tradingagents.agents.tools.search_tool import SearchTool
from tradingagents.utils.cache_management import get_cache_path
from tradingagents.dataflows.optimized_china_data import get_china_stock_data_cached, get_china_fundamentals_cached


class EnhancedAnalystNode(AgentNode):
    """
    增强分析师节点
    集成增强分析工具包，提供全面的股票分析能力
    """
    
    def __init__(self, name="enhanced_analyst", model="deepseek", online=True, cache_dir=None):
        super().__init__(name=name)
        self.model = model
        self.online = online
        self.cache_dir = cache_dir or get_cache_path()
        
        # 初始化增强分析工具包
        try:
            self.toolkit = EnhancedAnalysisToolkit()
            logging.info("✅ 增强分析工具包初始化成功")
        except Exception as e:
            logging.error(f"❌ 增强分析工具包初始化失败: {e}")
            self.toolkit = None
        
        # 初始化ReAct Agent
        self.agent = self._create_react_agent()
        
        # 分析结果缓存
        self.analysis_cache = {}
    
    def _create_react_agent(self) -> ReActAgent:
        """创建ReAct Agent"""
        system_message = self._get_system_message()
        tools = self._get_tools()
        
        return ReActAgent(
            name=self.name,
            system_message=system_message,
            tools=tools,
            model=self.model,
            verbose=True
        )
    
    def _get_system_message(self) -> str:
        """获取系统消息"""
        return """
        你是一个专业的增强型股票分析师，拥有先进的数据处理和分析能力。
        你的工作流程是：
        1. 接收用户的股票分析请求
        2. 使用增强分析工具包获取精确计算的技术指标、基本面指标、情绪指标和风险指标
        3. 基于这些精确计算的指标，进行深入的专业分析
        4. 生成全面、专业的分析报告
        
        你的分析报告应该包括以下部分：
        1. 技术分析：趋势判断、支撑阻力位、技术指标信号
        2. 基本面分析：估值水平、财务健康度、成长性评估
        3. 情绪分析：市场情绪、新闻影响、舆论热度
        4. 风险评估：波动风险、下行风险、流动性风险
        5. 综合评估：整体评分、投资建议、风险提示
        
        你的优势在于：
        1. 精确计算：所有指标都经过精确计算，避免了大语言模型在数值计算上的不精确性
        2. 全面分析：整合技术、基本面、情绪和风险多个维度
        3. 专业解读：基于精确数据，提供专业的市场洞察
        4. 量化评估：提供量化的评分和明确的投资建议
        
        请记住，你的分析建立在精确计算的基础上，这使你的分析比普通分析更加可靠。
        """
    
    def _get_tools(self) -> List[BaseTool]:
        """获取工具列表"""
        tools = []
        
        # 根据在线/离线模式选择不同的工具
        if self.online:
            # 在线模式：使用实时数据工具
            tools.extend([
                StockDataTool(),
                FundamentalsTool(),
                NewsTool(),
                SearchTool()
            ])
        else:
            # 离线模式：使用缓存数据和搜索工具
            tools.extend([
                SearchTool()
            ])
        
        return tools
    
    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """处理输入消息并返回分析结果"""
        try:
            # 解析输入消息
            ticker = message.get("ticker")
            query = message.get("query", "")
            
            if not ticker:
                return {"error": "缺少股票代码(ticker)参数"}
            
            # 检查缓存
            cache_key = f"{ticker}_{datetime.now().strftime('%Y-%m-%d')}"
            if cache_key in self.analysis_cache:
                logging.info(f"使用缓存的分析结果: {cache_key}")
                return self.analysis_cache[cache_key]
            
            # 获取股票数据
            stock_data, company_name = await self._get_stock_data(ticker)
            if not stock_data:
                return {"error": f"无法获取股票 {ticker} 的数据"}
            
            # 获取基本面数据
            fundamentals_data = await self._get_fundamentals_data(ticker)
            
            # 获取新闻数据
            news_data = await self._get_news_data(ticker, company_name)
            
            # 使用增强分析工具包进行分析
            if self.toolkit:
                logging.info(f"使用增强分析工具包分析 {ticker} ({company_name})")
                analysis_results = self.toolkit.comprehensive_analysis(
                    ticker=ticker,
                    stock_data=stock_data,
                    fundamentals_data=fundamentals_data,
                    news_data=news_data,
                    company_name=company_name
                )
                
                # 生成增强分析报告
                enhanced_report = self.toolkit.generate_enhanced_report(analysis_results)
                
                # 使用DeepSeek进行深度解读
                deepseek_analysis = await self._get_deepseek_analysis(ticker, company_name, enhanced_report, query)
                
                # 合并结果
                result = {
                    "ticker": ticker,
                    "company_name": company_name,
                    "analysis_date": datetime.now().strftime('%Y-%m-%d'),
                    "enhanced_analysis": analysis_results,
                    "enhanced_report": enhanced_report,
                    "deepseek_analysis": deepseek_analysis
                }
                
                # 缓存结果
                self.analysis_cache[cache_key] = result
                
                return result
            else:
                # 如果增强分析工具包不可用，回退到ReAct Agent
                logging.warning("增强分析工具包不可用，回退到ReAct Agent")
                return await self._fallback_to_react_agent(ticker, company_name, stock_data, fundamentals_data, news_data, query)
        
        except Exception as e:
            logging.error(f"增强分析师处理失败: {e}", exc_info=True)
            return {"error": f"分析处理失败: {str(e)}"}
    
    async def _get_stock_data(self, ticker: str) -> Tuple[str, str]:
        """获取股票数据"""
        company_name = "未知公司"
        
        try:
            # 优先使用缓存的中国股票数据
            if ticker.startswith("0") or ticker.startswith("3") or ticker.startswith("6"):
                stock_data = get_china_stock_data_cached(ticker)
                if stock_data:
                    # 从数据中提取公司名称
                    if "company_name" in stock_data:
                        company_name = stock_data["company_name"]
                    # 转换为字符串格式
                    return json.dumps(stock_data, ensure_ascii=False), company_name
            
            # 如果缓存未命中或非中国股票，使用ReAct Agent获取
            if self.agent:
                response = await self.agent.arun(f"获取股票 {ticker} 的历史价格数据")
                if isinstance(response, dict) and "content" in response:
                    # 尝试从回复中提取公司名称
                    if "公司名称" in response["content"]:
                        name_line = [line for line in response["content"].split("\n") if "公司名称" in line]
                        if name_line:
                            company_name = name_line[0].split(":")[-1].strip()
                    
                    return response["content"], company_name
            
            return "", company_name
        
        except Exception as e:
            logging.error(f"获取股票数据失败: {e}", exc_info=True)
            return "", company_name
    
    async def _get_fundamentals_data(self, ticker: str) -> str:
        """获取基本面数据"""
        try:
            # 优先使用缓存的中国基本面数据
            if ticker.startswith("0") or ticker.startswith("3") or ticker.startswith("6"):
                fundamentals_data = get_china_fundamentals_cached(ticker)
                if fundamentals_data:
                    return json.dumps(fundamentals_data, ensure_ascii=False)
            
            # 如果缓存未命中或非中国股票，使用ReAct Agent获取
            if self.agent:
                response = await self.agent.arun(f"获取股票 {ticker} 的基本面数据，包括市盈率、市净率、净资产收益率等财务指标")
                if isinstance(response, dict) and "content" in response:
                    return response["content"]
            
            return ""
        
        except Exception as e:
            logging.error(f"获取基本面数据失败: {e}", exc_info=True)
            return ""
    
    async def _get_news_data(self, ticker: str, company_name: str) -> str:
        """获取新闻数据"""
        try:
            if self.agent:
                # 使用公司名称可能获得更好的新闻结果
                search_term = company_name if company_name != "未知公司" else ticker
                response = await self.agent.arun(f"获取与 {search_term} 相关的最新财经新闻")
                if isinstance(response, dict) and "content" in response:
                    return response["content"]
            
            return ""
        
        except Exception as e:
            logging.error(f"获取新闻数据失败: {e}", exc_info=True)
            return ""
    
    async def _get_deepseek_analysis(self, ticker: str, company_name: str, enhanced_report: str, query: str) -> str:
        """使用DeepSeek进行深度解读"""
        try:
            if self.agent:
                # 构建提示词
                prompt = f"""
                请基于以下增强分析报告，对 {ticker}（{company_name}）进行深度专业解读。
                
                增强分析报告：
                {enhanced_report}
                
                {"请重点关注: " + query if query else "请提供全面的专业解读，包括投资建议和风险提示。"}
                
                你的解读应该：
                1. 提炼报告中最关键的信息点
                2. 结合市场环境进行专业解读
                3. 提供明确的投资建议和操作思路
                4. 指出潜在风险和需要关注的要点
                
                请以专业分析师的身份，给出深度、专业、有洞察力的解读。
                """
                
                response = await self.agent.arun(prompt)
                if isinstance(response, dict) and "content" in response:
                    return response["content"]
            
            return "DeepSeek深度解读不可用"
        
        except Exception as e:
            logging.error(f"获取DeepSeek分析失败: {e}", exc_info=True)
            return f"DeepSeek分析失败: {str(e)}"
    
    async def _fallback_to_react_agent(self, ticker: str, company_name: str, 
                                     stock_data: str, fundamentals_data: str, 
                                     news_data: str, query: str) -> Dict[str, Any]:
        """回退到ReAct Agent进行分析"""
        try:
            if self.agent:
                # 构建提示词
                prompt = f"""
                请对 {ticker}（{company_name}）进行全面分析，包括技术分析、基本面分析、情绪分析和风险评估。
                
                股票数据：
                {stock_data}
                
                基本面数据：
                {fundamentals_data}
                
                新闻数据：
                {news_data}
                
                {"请重点关注: " + query if query else "请提供全面的专业分析，包括投资建议和风险提示。"}
                
                请以专业分析师的身份，给出深度、专业、有洞察力的分析报告。
                """
                
                response = await self.agent.arun(prompt)
                if isinstance(response, dict) and "content" in response:
                    return {
                        "ticker": ticker,
                        "company_name": company_name,
                        "analysis_date": datetime.now().strftime('%Y-%m-%d'),
                        "react_agent_analysis": response["content"]
                    }
            
            return {"error": "分析失败，ReAct Agent不可用"}
        
        except Exception as e:
            logging.error(f"回退到ReAct Agent失败: {e}", exc_info=True)
            return {"error": f"分析失败: {str(e)}"}


def create_enhanced_analyst(model="deepseek", online=True, cache_dir=None) -> EnhancedAnalystNode:
    """创建增强分析师节点的工厂函数"""
    return EnhancedAnalystNode(model=model, online=online, cache_dir=cache_dir)


if __name__ == "__main__":
    # 简单测试
    import asyncio
    
    async def test_enhanced_analyst():
        analyst = create_enhanced_analyst(online=True)
        result = await analyst.process({"ticker": "000001", "query": "重点分析估值和风险"})
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    asyncio.run(test_enhanced_analyst())