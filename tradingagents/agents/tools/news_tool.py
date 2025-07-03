#!/usr/bin/env python3
"""
新闻数据工具
用于获取股票相关的新闻和市场情绪数据
"""

import json
from datetime import datetime, timedelta
from typing import Optional
from .base import BaseTool


class NewsTool(BaseTool):
    """
    新闻数据工具
    获取股票相关的新闻、公告和市场情绪信息
    """
    
    def __init__(self):
        super().__init__(
            name="news",
            description="获取股票相关的新闻、公告、分析师报告和市场情绪信息"
        )
    
    async def run(self, ticker: str, company_name: str = "", days: int = 7) -> str:
        """
        获取新闻数据
        
        Args:
            ticker: 股票代码
            company_name: 公司名称
            days: 获取最近几天的新闻 (默认7天)
            
        Returns:
            JSON格式的新闻数据字符串
        """
        try:
            self.log_info(f"获取新闻数据: {ticker} ({company_name}), 最近{days}天")
            
            # 检查是否为中国股票
            if self._is_china_stock(ticker):
                return await self._get_china_news(ticker, company_name, days)
            else:
                return await self._get_us_news(ticker, company_name, days)
                
        except Exception as e:
            self.log_error(f"获取新闻数据失败: {e}")
            return json.dumps({
                "error": f"获取新闻数据失败: {str(e)}",
                "ticker": ticker,
                "company_name": company_name
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
    
    async def _get_china_news(self, ticker: str, company_name: str, days: int) -> str:
        """
        获取中国股票新闻数据
        
        Args:
            ticker: 股票代码
            company_name: 公司名称
            days: 天数
            
        Returns:
            JSON格式的新闻数据字符串
        """
        try:
            # 生成模拟的中国股票新闻数据
            self.log_info(f"生成中国股票新闻数据: {ticker}")
            
            news_data = {
                "ticker": ticker,
                "company_name": company_name or f"股票{ticker}",
                "market": "中国A股",
                "data_source": "模拟数据",
                "search_period": f"最近{days}天",
                "news_count": 5,
                "news_articles": [
                    {
                        "title": f"{company_name or ticker}发布季度财报，业绩超预期",
                        "summary": "公司本季度营收和净利润均实现双位数增长，超出市场预期。",
                        "source": "财经新闻网",
                        "publish_date": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                        "sentiment": "积极",
                        "relevance": 0.95
                    },
                    {
                        "title": f"{company_name or ticker}获得重要合同，业务拓展顺利",
                        "summary": "公司成功签署大额合同，预计将对未来业绩产生积极影响。",
                        "source": "证券时报",
                        "publish_date": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
                        "sentiment": "积极",
                        "relevance": 0.88
                    },
                    {
                        "title": "行业分析师上调目标价",
                        "summary": "多家券商分析师上调目标价，看好公司长期发展前景。",
                        "source": "投资快报",
                        "publish_date": (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
                        "sentiment": "积极",
                        "relevance": 0.82
                    },
                    {
                        "title": "市场波动影响股价表现",
                        "summary": "受整体市场波动影响，股价出现短期调整。",
                        "source": "市场观察",
                        "publish_date": (datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d'),
                        "sentiment": "中性",
                        "relevance": 0.65
                    },
                    {
                        "title": "公司管理层接受媒体采访",
                        "summary": "管理层详细介绍了公司战略规划和未来发展方向。",
                        "source": "经济日报",
                        "publish_date": (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
                        "sentiment": "积极",
                        "relevance": 0.78
                    }
                ],
                "sentiment_analysis": {
                    "overall_sentiment": "积极",
                    "positive_ratio": 0.8,
                    "neutral_ratio": 0.2,
                    "negative_ratio": 0.0,
                    "sentiment_score": 0.75
                },
                "key_topics": ["财报", "业绩", "合同", "分析师评级", "管理层"],
                "note": "这是模拟数据，仅用于测试目的"
            }
            
            return json.dumps(news_data, ensure_ascii=False)
            
        except Exception as e:
            self.log_error(f"获取中国股票新闻数据失败: {e}")
            raise
    
    async def _get_us_news(self, ticker: str, company_name: str, days: int) -> str:
        """
        获取美股新闻数据
        
        Args:
            ticker: 股票代码
            company_name: 公司名称
            days: 天数
            
        Returns:
            JSON格式的新闻数据字符串
        """
        try:
            # 生成模拟的美股新闻数据
            self.log_info(f"生成美股新闻数据: {ticker}")
            
            news_data = {
                "ticker": ticker,
                "company_name": company_name or f"{ticker} Inc.",
                "market": "US Stock",
                "data_source": "模拟数据",
                "search_period": f"最近{days}天",
                "news_count": 4,
                "news_articles": [
                    {
                        "title": f"{ticker} Reports Strong Q3 Earnings",
                        "summary": "Company beats analyst expectations with strong revenue and profit growth.",
                        "source": "Financial Times",
                        "publish_date": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                        "sentiment": "Positive",
                        "relevance": 0.92
                    },
                    {
                        "title": f"{ticker} Announces New Product Launch",
                        "summary": "Company unveils innovative product expected to drive future growth.",
                        "source": "Reuters",
                        "publish_date": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
                        "sentiment": "Positive",
                        "relevance": 0.85
                    },
                    {
                        "title": "Analyst Upgrades Rating",
                        "summary": "Wall Street analyst upgrades stock rating citing strong fundamentals.",
                        "source": "Bloomberg",
                        "publish_date": (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
                        "sentiment": "Positive",
                        "relevance": 0.88
                    },
                    {
                        "title": "Market Volatility Affects Stock Price",
                        "summary": "Stock experiences short-term volatility amid broader market concerns.",
                        "source": "CNBC",
                        "publish_date": (datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d'),
                        "sentiment": "Neutral",
                        "relevance": 0.70
                    }
                ],
                "sentiment_analysis": {
                    "overall_sentiment": "Positive",
                    "positive_ratio": 0.75,
                    "neutral_ratio": 0.25,
                    "negative_ratio": 0.0,
                    "sentiment_score": 0.72
                },
                "key_topics": ["earnings", "product launch", "analyst rating", "market volatility"],
                "note": "这是模拟数据，仅用于测试目的"
            }
            
            return json.dumps(news_data, ensure_ascii=False)
            
        except Exception as e:
            self.log_error(f"获取美股新闻数据失败: {e}")
            raise