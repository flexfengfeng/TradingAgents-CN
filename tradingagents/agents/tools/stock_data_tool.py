#!/usr/bin/env python3
"""
股票数据工具
用于获取股票价格和技术指标数据
"""

import json
from typing import Optional
from .base import BaseTool


class StockDataTool(BaseTool):
    """
    股票数据工具
    获取股票的历史价格数据和技术指标
    """
    
    def __init__(self):
        super().__init__(
            name="stock_data",
            description="获取股票的历史价格数据、技术指标和基本信息"
        )
    
    async def run(self, ticker: str, period: str = "1y") -> str:
        """
        获取股票数据
        
        Args:
            ticker: 股票代码
            period: 数据周期 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            JSON格式的股票数据字符串
        """
        try:
            self.log_info(f"获取股票数据: {ticker}, 周期: {period}")
            
            # 检查是否为中国股票
            if self._is_china_stock(ticker):
                return await self._get_china_stock_data(ticker, period)
            else:
                return await self._get_us_stock_data(ticker, period)
                
        except Exception as e:
            self.log_error(f"获取股票数据失败: {e}")
            return json.dumps({
                "error": f"获取股票数据失败: {str(e)}",
                "ticker": ticker,
                "period": period
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
    
    async def _get_china_stock_data(self, ticker: str, period: str) -> str:
        """
        获取中国股票数据
        
        Args:
            ticker: 股票代码
            period: 数据周期
            
        Returns:
            JSON格式的股票数据字符串
        """
        try:
            # 尝试使用缓存的中国股票数据
            from tradingagents.utils.optimized_china_data import get_china_stock_data_cached
            
            stock_data = get_china_stock_data_cached(ticker)
            if stock_data:
                self.log_info(f"从缓存获取中国股票数据: {ticker}")
                return json.dumps(stock_data, ensure_ascii=False)
            
            # 如果缓存未命中，返回模拟数据
            self.log_warning(f"缓存未命中，返回模拟数据: {ticker}")
            return json.dumps({
                "ticker": ticker,
                "company_name": f"股票{ticker}",
                "market": "中国A股",
                "currency": "CNY",
                "data_source": "模拟数据",
                "period": period,
                "price_data": {
                    "current_price": 10.50,
                    "open": 10.20,
                    "high": 10.80,
                    "low": 10.00,
                    "volume": 1000000,
                    "change": 0.30,
                    "change_percent": 2.94
                },
                "technical_indicators": {
                    "ma5": 10.25,
                    "ma10": 10.15,
                    "ma20": 10.05,
                    "rsi": 65.5,
                    "macd": 0.15
                },
                "note": "这是模拟数据，仅用于测试目的"
            }, ensure_ascii=False)
            
        except Exception as e:
            self.log_error(f"获取中国股票数据失败: {e}")
            raise
    
    async def _get_us_stock_data(self, ticker: str, period: str) -> str:
        """
        获取美股数据
        
        Args:
            ticker: 股票代码
            period: 数据周期
            
        Returns:
            JSON格式的股票数据字符串
        """
        try:
            # 返回模拟的美股数据
            self.log_info(f"获取美股数据: {ticker}")
            return json.dumps({
                "ticker": ticker,
                "company_name": f"{ticker} Inc.",
                "market": "US Stock",
                "currency": "USD",
                "data_source": "模拟数据",
                "period": period,
                "price_data": {
                    "current_price": 150.25,
                    "open": 148.50,
                    "high": 152.00,
                    "low": 147.80,
                    "volume": 2500000,
                    "change": 1.75,
                    "change_percent": 1.18
                },
                "technical_indicators": {
                    "ma5": 149.80,
                    "ma10": 148.90,
                    "ma20": 147.50,
                    "rsi": 58.2,
                    "macd": 0.85
                },
                "note": "这是模拟数据，仅用于测试目的"
            }, ensure_ascii=False)
            
        except Exception as e:
            self.log_error(f"获取美股数据失败: {e}")
            raise