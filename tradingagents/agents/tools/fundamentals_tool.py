#!/usr/bin/env python3
"""
基本面数据工具
用于获取股票的基本面和财务数据
"""

import json
from typing import Optional
from .base import BaseTool


class FundamentalsTool(BaseTool):
    """
    基本面数据工具
    获取股票的财务数据、估值指标和基本面信息
    """
    
    def __init__(self):
        super().__init__(
            name="fundamentals",
            description="获取股票的财务数据、估值指标、盈利能力和基本面信息"
        )
    
    async def run(self, ticker: str) -> str:
        """
        获取基本面数据
        
        Args:
            ticker: 股票代码
            
        Returns:
            JSON格式的基本面数据字符串
        """
        try:
            self.log_info(f"获取基本面数据: {ticker}")
            
            # 检查是否为中国股票
            if self._is_china_stock(ticker):
                return await self._get_china_fundamentals(ticker)
            else:
                return await self._get_us_fundamentals(ticker)
                
        except Exception as e:
            self.log_error(f"获取基本面数据失败: {e}")
            return json.dumps({
                "error": f"获取基本面数据失败: {str(e)}",
                "ticker": ticker
            }, ensure_ascii=False)
    
    def _is_china_stock(self, ticker: str) -> bool:
        """
        判断是否为中国A股代码
        
        Args:
            ticker: 股票代码
            
        Returns:
            是否为中国A股
        """
        import re
        return re.match(r'^\d{6}$', str(ticker)) is not None
    
    async def _get_china_fundamentals(self, ticker: str) -> str:
        """
        获取中国股票基本面数据
        
        Args:
            ticker: 股票代码
            
        Returns:
            JSON格式的基本面数据字符串
        """
        try:
            # 尝试使用缓存的中国基本面数据
            from tradingagents.utils.optimized_china_data import get_china_fundamentals_cached
            
            fundamentals_data = get_china_fundamentals_cached(ticker)
            if fundamentals_data:
                self.log_info(f"从缓存获取中国基本面数据: {ticker}")
                return json.dumps(fundamentals_data, ensure_ascii=False)
            
            # 如果缓存未命中，返回模拟数据
            self.log_warning(f"缓存未命中，返回模拟基本面数据: {ticker}")
            return json.dumps({
                "ticker": ticker,
                "company_name": f"股票{ticker}",
                "market": "中国A股",
                "data_source": "模拟数据",
                "financial_metrics": {
                    "market_cap": "100亿元",
                    "pe_ratio": 15.5,
                    "pb_ratio": 1.8,
                    "roe": 12.5,
                    "debt_to_equity": 0.45,
                    "current_ratio": 2.1,
                    "gross_margin": 25.8,
                    "net_margin": 8.2
                },
                "growth_metrics": {
                    "revenue_growth_yoy": 15.2,
                    "earnings_growth_yoy": 18.5,
                    "revenue_growth_qoq": 3.8,
                    "earnings_growth_qoq": 5.2
                },
                "dividend_info": {
                    "dividend_yield": 2.5,
                    "payout_ratio": 30.0,
                    "dividend_per_share": 0.25
                },
                "business_info": {
                    "industry": "制造业",
                    "sector": "工业",
                    "employees": 5000,
                    "description": "这是一个模拟的公司描述"
                },
                "note": "这是模拟数据，仅用于测试目的"
            }, ensure_ascii=False)
            
        except Exception as e:
            self.log_error(f"获取中国基本面数据失败: {e}")
            raise
    
    async def _get_us_fundamentals(self, ticker: str) -> str:
        """
        获取美股基本面数据
        
        Args:
            ticker: 股票代码
            
        Returns:
            JSON格式的基本面数据字符串
        """
        try:
            # 返回模拟的美股基本面数据
            self.log_info(f"获取美股基本面数据: {ticker}")
            return json.dumps({
                "ticker": ticker,
                "company_name": f"{ticker} Inc.",
                "market": "US Stock",
                "data_source": "模拟数据",
                "financial_metrics": {
                    "market_cap": "$50B",
                    "pe_ratio": 22.3,
                    "pb_ratio": 3.2,
                    "roe": 18.7,
                    "debt_to_equity": 0.35,
                    "current_ratio": 1.8,
                    "gross_margin": 42.5,
                    "net_margin": 15.8
                },
                "growth_metrics": {
                    "revenue_growth_yoy": 12.8,
                    "earnings_growth_yoy": 25.3,
                    "revenue_growth_qoq": 4.2,
                    "earnings_growth_qoq": 8.1
                },
                "dividend_info": {
                    "dividend_yield": 1.8,
                    "payout_ratio": 25.0,
                    "dividend_per_share": 2.50
                },
                "business_info": {
                    "industry": "Technology",
                    "sector": "Information Technology",
                    "employees": 15000,
                    "description": "This is a simulated company description"
                },
                "note": "这是模拟数据，仅用于测试目的"
            }, ensure_ascii=False)
            
        except Exception as e:
            self.log_error(f"获取美股基本面数据失败: {e}")
            raise