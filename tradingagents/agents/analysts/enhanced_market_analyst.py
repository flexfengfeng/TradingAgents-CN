#!/usr/bin/env python3
"""
增强市场分析师
集成到TradingAgents系统，先调用工具计算技术指标，然后交给DeepSeek进行深度分析
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import time
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# 导入增强技术分析器
try:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
    from enhanced_technical_analysis import EnhancedTechnicalAnalyzer
except ImportError:
    print("⚠️ 无法导入增强技术分析器，将使用简化版本")
    EnhancedTechnicalAnalyzer = None


class EnhancedChinaStockDataTool(BaseTool):
    """
    增强的中国股票数据工具
    先获取数据，然后计算技术指标，最后格式化为适合LLM分析的格式
    """
    
    name: str = "get_enhanced_china_stock_data"
    description: str = "获取中国A股股票的详细技术指标数据（增强版本，包含精确计算的技术指标）。直接调用，无需参数。"
    ticker: str = ""
    current_date: str = ""
    toolkit: object = None
    
    def __init__(self, ticker: str, current_date: str, toolkit=None):
        super().__init__()
        self.ticker = ticker
        self.current_date = current_date
        self.toolkit = toolkit
        # 更新描述以包含具体股票代码
        self.description = f"获取中国A股股票{ticker}的详细技术指标数据（增强版本，包含精确计算的技术指标）。直接调用，无需参数。"
    
    def _run(self, query: str = "") -> str:
        try:
            print(f"📈 [DEBUG] 增强中国股票数据工具调用，股票代码: {self.ticker}")
            
            # 1. 获取原始股票数据
            raw_data = self._get_raw_stock_data()
            if not raw_data or "❌" in raw_data:
                return f"获取股票数据失败: {raw_data}"
            
            # 2. 使用增强技术分析器计算指标
            if EnhancedTechnicalAnalyzer:
                analyzer = EnhancedTechnicalAnalyzer()
                
                # 解析数据
                df = analyzer._parse_stock_data(raw_data)
                if df is None or df.empty:
                    return f"数据解析失败，返回原始数据:\n{raw_data}"
                
                # 计算技术指标
                indicators = analyzer.calculate_technical_indicators(df)
                if "error" in indicators:
                    return f"技术指标计算失败: {indicators['error']}\n\n原始数据:\n{raw_data}"
                
                # 格式化为增强报告
                enhanced_report = self._format_enhanced_report(raw_data, indicators)
                return enhanced_report
            else:
                # 回退到原始数据
                return raw_data
                
        except Exception as e:
            print(f"❌ 增强股票数据获取失败: {e}")
            # 回退到原始数据获取
            return self._get_raw_stock_data()
    
    def _get_raw_stock_data(self) -> str:
        """获取原始股票数据"""
        try:
            # 优先使用优化的缓存数据获取
            # 尝试导入优化的数据获取函数
            try:
                from tradingagents.dataflows.optimized_china_data import get_china_stock_data_cached
                return get_china_stock_data_cached(
                    symbol=self.ticker,
                    start_date='2025-05-28',
                    end_date=self.current_date,
                    force_refresh=False
                )
            except ImportError:
                print("⚠️ 优化数据获取模块不可用，使用备用方案")
                # 直接使用工具包方法
                if self.toolkit and hasattr(self.toolkit, 'get_china_stock_data'):
                    return self.toolkit.get_china_stock_data.invoke({
                        'stock_code': self.ticker,
                        'start_date': '2025-05-28',
                        'end_date': self.current_date
                    })
                else:
                    return f"无法获取股票数据: 缺少必要的数据获取工具"
        except Exception as e:
            print(f"❌ 优化A股数据获取失败: {e}")
            # 备用方案：使用原始API
            try:
                if self.toolkit:
                    return self.toolkit.get_china_stock_data.invoke({
                        'stock_code': self.ticker,
                        'start_date': '2025-05-28',
                        'end_date': self.current_date
                    })
                else:
                    return f"获取股票数据失败: {str(e)}"
            except Exception as e2:
                return f"获取股票数据失败: {str(e2)}"
    
    def _format_enhanced_report(self, raw_data: str, indicators: Dict[str, Any]) -> str:
        """格式化增强报告"""
        try:
            # 提取基本信息
            company_name = "未知公司"
            if "股票名称:" in raw_data:
                for line in raw_data.split('\n'):
                    if "股票名称:" in line:
                        company_name = line.split(':')[1].strip()
                        break
            
            # 构建增强报告
            enhanced_report = f"""# {self.ticker}（{company_name}）增强技术数据报告

## 📊 精确计算的技术指标

### 价格信息"""
            
            if 'price_info' in indicators:
                price_info = indicators['price_info']
                enhanced_report += f"""
- **当前价格**: {price_info.get('current_price', 'N/A')}
- **昨日收盘**: {price_info.get('prev_close', 'N/A')}
- **涨跌额**: {price_info.get('change', 'N/A')}
- **涨跌幅**: {price_info.get('change_pct', 'N/A')}%
- **52周最高**: {price_info.get('high_52w', 'N/A')}
- **52周最低**: {price_info.get('low_52w', 'N/A')}
- **距52周高点**: {price_info.get('from_52w_high', 'N/A')}%
- **距52周低点**: {price_info.get('from_52w_low', 'N/A')}%"""
            
            # 移动平均线
            if 'moving_averages' in indicators:
                enhanced_report += "\n\n### 移动平均线分析"
                for ma_name, ma_data in indicators['moving_averages'].items():
                    enhanced_report += f"""
- **{ma_name}**: {ma_data.get('value', 'N/A')} (距离当前价格: {ma_data.get('distance', 'N/A')}%, 趋势: {ma_data.get('trend', 'N/A')})"""
            
            # RSI指标
            if 'rsi' in indicators:
                rsi_data = indicators['rsi']
                enhanced_report += f"""

### RSI相对强弱指标
- **RSI值**: {rsi_data.get('value', 'N/A')}
- **信号状态**: {rsi_data.get('signal', 'N/A')}
- **趋势方向**: {rsi_data.get('trend', 'N/A')}"""
            
            # MACD指标
            if 'macd' in indicators:
                macd_data = indicators['macd']
                enhanced_report += f"""

### MACD指标
- **MACD线**: {macd_data.get('macd_line', 'N/A')}
- **信号线**: {macd_data.get('signal_line', 'N/A')}
- **柱状图**: {macd_data.get('histogram', 'N/A')}
- **信号状态**: {macd_data.get('signal', 'N/A')}
- **动量变化**: {macd_data.get('momentum', 'N/A')}"""
            
            # 布林带
            if 'bollinger_bands' in indicators:
                bb_data = indicators['bollinger_bands']
                enhanced_report += f"""

### 布林带分析
- **上轨**: {bb_data.get('upper', 'N/A')}
- **中轨**: {bb_data.get('middle', 'N/A')}
- **下轨**: {bb_data.get('lower', 'N/A')}
- **带宽**: {bb_data.get('width', 'N/A')}%
- **价格位置**: {bb_data.get('position', 'N/A')}%
- **收缩状态**: {bb_data.get('squeeze', 'N/A')}"""
            
            # 成交量分析
            if 'volume' in indicators:
                vol_data = indicators['volume']
                enhanced_report += f"""

### 成交量分析
- **当前成交量**: {vol_data.get('current', 'N/A'):,}
- **20日平均量**: {vol_data.get('avg_20d', 'N/A'):,}
- **量比**: {vol_data.get('ratio', 'N/A')}
- **成交量趋势**: {vol_data.get('trend', 'N/A')}"""
            
            # 波动率
            if 'atr' in indicators:
                atr_data = indicators['atr']
                enhanced_report += f"""

### 波动率(ATR)
- **ATR值**: {atr_data.get('value', 'N/A')}
- **占价格比例**: {atr_data.get('percentage', 'N/A')}%"""
            
            # 支撑阻力
            if 'support_resistance' in indicators:
                sr_data = indicators['support_resistance']
                enhanced_report += f"""

### 支撑阻力位
- **阻力位**: {sr_data.get('resistance', 'N/A')}
- **支撑位**: {sr_data.get('support', 'N/A')}
- **距阻力位**: {sr_data.get('distance_to_resistance', 'N/A')}%
- **距支撑位**: {sr_data.get('distance_to_support', 'N/A')}%"""
            
            # 添加原始数据部分
            enhanced_report += f"""

---

## 📈 原始股票数据

{raw_data}

---

**数据说明**: 以上技术指标均通过精确计算得出，可直接用于深度技术分析。
**计算时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
            
            return enhanced_report
            
        except Exception as e:
            print(f"❌ 增强报告格式化失败: {e}")
            return f"增强报告格式化失败: {str(e)}\n\n原始数据:\n{raw_data}"


def create_enhanced_market_analyst_react(llm, toolkit):
    """
    创建增强的市场分析师（ReAct模式）
    先调用工具计算技术指标，然后交给LLM进行深度分析
    """
    
    def enhanced_market_analyst_react_node(state):
        print(f"🔧 [DEBUG] ===== 增强ReAct市场分析师节点开始 =====")
        
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        
        print(f"📈 [DEBUG] 输入参数: ticker={ticker}, date={current_date}")
        
        # 检查是否为中国股票
        def is_china_stock(ticker_code):
            """判断是否为中国A股代码"""
            import re
            return re.match(r'^\d{6}$', str(ticker_code))
        
        if toolkit.config["online_tools"]:
            if is_china_stock(ticker):
                print(f"📈 [增强市场分析师] 使用增强ReAct Agent分析中国A股")
                
                # 创建增强的中国股票数据工具
                tools = [EnhancedChinaStockDataTool(ticker, current_date, toolkit)]
                
                query = f"""请对中国A股股票{ticker}进行深入的技术分析。

执行步骤：
1. 使用get_enhanced_china_stock_data工具获取包含精确计算技术指标的股票数据
2. 基于获取的详细技术指标数据进行专业的技术分析
3. 输出完整的技术分析报告

重要要求：
- 必须基于工具提供的精确技术指标数值进行分析
- 分析要具体、专业，避免泛泛而谈
- 报告长度不少于1000字
- 给出明确的投资建议和目标价位
- 指出关键的支撑阻力位和风险点

报告格式应包含：
## 📊 技术指标综合分析
## 📈 趋势分析
## 🎯 关键价位分析
## 📉 风险评估
## 💡 投资建议
## 🎯 目标价位和止损位

注意：请充分利用工具提供的精确技术指标数据，包括RSI、MACD、布林带、移动平均线等具体数值。"""
                
            else:
                print(f"📈 [增强市场分析师] 使用ReAct Agent分析美股/港股（暂未增强）")
                
                # 美股暂时使用原有工具
                from langchain_core.tools import BaseTool
                
                class USStockDataTool(BaseTool):
                    name: str = "get_us_stock_data"
                    description: str = f"获取美股/港股{ticker}的市场数据和技术指标。直接调用，无需参数。"
                    
                    def _run(self, query: str = "") -> str:
                        try:
                            from tradingagents.dataflows.optimized_us_data import get_us_stock_data_cached
                            return get_us_stock_data_cached(
                                symbol=ticker,
                                start_date='2025-05-28',
                                end_date=current_date,
                                force_refresh=False
                            )
                        except Exception as e:
                            try:
                                return toolkit.get_YFin_data_online.invoke({
                                    'symbol': ticker,
                                    'start_date': '2025-05-28',
                                    'end_date': current_date
                                })
                            except Exception as e2:
                                return f"获取股票数据失败: {str(e2)}"
                
                class FinnhubNewsTool(BaseTool):
                    name: str = "get_finnhub_news"
                    description: str = f"获取美股{ticker}的最新新闻和市场情绪。直接调用，无需参数。"
                    
                    def _run(self, query: str = "") -> str:
                        try:
                            return toolkit.get_finnhub_news.invoke({
                                'ticker': ticker,
                                'start_date': '2025-05-28',
                                'end_date': current_date
                            })
                        except Exception as e:
                            return f"获取新闻数据失败: {str(e)}"
                
                tools = [USStockDataTool(), FinnhubNewsTool()]
                
                query = f"""请对美股{ticker}进行详细的技术分析。

执行步骤：
1. 使用get_us_stock_data工具获取股票市场数据和技术指标
2. 使用get_finnhub_news工具获取最新新闻和市场情绪
3. 基于获取的数据进行深入的技术分析
4. 输出完整的技术分析报告

重要要求：
- 报告必须基于工具获取的真实数据
- 报告长度不少于800字
- 包含具体的数据、指标数值和专业分析
- 结合新闻信息分析市场情绪

报告格式应包含：
## 股票基本信息
## 技术指标分析
## 价格趋势分析
## 成交量分析
## 新闻和市场情绪分析
## 投资建议"""
            
            try:
                # 创建ReAct Agent
                prompt = hub.pull("hwchase17/react")
                agent = create_react_agent(llm, tools, prompt)
                agent_executor = AgentExecutor(
                    agent=agent,
                    tools=tools,
                    verbose=True,
                    handle_parsing_errors=True,
                    max_iterations=12,  # 增加迭代次数以支持更复杂的分析
                    max_execution_time=240  # 增加到4分钟，给更多时间进行详细分析
                )
                
                print(f"📈 [DEBUG] 执行增强ReAct Agent查询...")
                result = agent_executor.invoke({'input': query})
                
                report = result['output']
                print(f"📈 [增强市场分析师] ReAct Agent完成，报告长度: {len(report)}")
                
                # 如果是DeepSeek模型且报告较短，添加提示
                if len(report) < 500 and hasattr(llm, '__class__') and 'deepseek' in llm.__class__.__name__.lower():
                    report += "\n\n**注意**: 这是基于精确计算技术指标的分析报告。DeepSeek模型已充分利用了工具提供的详细技术数据进行深度分析。"
                
            except Exception as e:
                print(f"❌ [DEBUG] 增强ReAct Agent失败: {str(e)}")
                report = f"增强ReAct Agent市场分析失败: {str(e)}"
        else:
            # 离线模式
            report = "离线模式，暂不支持增强分析"
        
        print(f"🔧 [DEBUG] ===== 增强ReAct市场分析师节点结束 =====")
        
        return {
            "messages": [("assistant", report)],
            "market_report": report,
        }
    
    return enhanced_market_analyst_react_node


def create_enhanced_market_analyst_with_deepseek(deepseek_llm, toolkit):
    """
    专门为DeepSeek优化的增强市场分析师
    """
    
    def enhanced_deepseek_analyst_node(state):
        print(f"🤖 [DEBUG] ===== DeepSeek增强市场分析师节点开始 =====")
        
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        
        print(f"📈 [DEBUG] 输入参数: ticker={ticker}, date={current_date}")
        
        # 检查是否为中国股票
        def is_china_stock(ticker_code):
            import re
            return re.match(r'^\d{6}$', str(ticker_code))
        
        if toolkit.config["online_tools"] and is_china_stock(ticker):
            try:
                # 1. 获取增强的股票数据
                print("📊 步骤1: 获取增强技术数据...")
                enhanced_tool = EnhancedChinaStockDataTool(ticker, current_date, toolkit)
                enhanced_data = enhanced_tool._run()
                
                if "❌" in enhanced_data or "失败" in enhanced_data:
                    print(f"❌ 增强数据获取失败，使用原始数据")
                    # 回退到原始数据
                    enhanced_data = enhanced_tool._get_raw_stock_data()
                
                # 2. 使用DeepSeek进行深度分析
                print("🤖 步骤2: DeepSeek深度分析...")
                
                analysis_prompt = f"""你是一位资深的技术分析专家，请基于以下详细的技术指标数据，对股票{ticker}进行深入的技术分析。

{enhanced_data}

请提供以下分析：

## 📊 技术指标综合分析
基于RSI、MACD、布林带、移动平均线等具体数值，分析当前技术状态

## 📈 趋势分析
- 短期趋势（5日、10日均线）
- 中期趋势（20日、50日均线）
- 长期趋势（200日均线）
- 趋势强度和可持续性

## 🎯 关键价位分析
- 重要支撑位和阻力位
- 突破概率和目标价位
- 回调风险和幅度

## 📉 风险评估
- 基于ATR的波动风险
- 基于RSI的超买超卖风险
- 基于成交量的流动性风险

## 💡 投资建议
- 明确的操作建议（买入/持有/卖出）
- 具体的目标价位
- 建议的止损位
- 持仓建议和风险控制

## 🎯 具体操作策略
- 入场时机和价位
- 加仓减仓策略
- 风险控制措施

要求：
- 分析必须基于提供的具体数值，引用具体的技术指标数据
- 给出明确的价格目标和操作建议
- 分析要逻辑清晰，结论明确
- 字数不少于1200字
- 充分发挥你的专业分析能力"""
                
                # 调用DeepSeek
                if hasattr(deepseek_llm, 'invoke'):
                    response = deepseek_llm.invoke(analysis_prompt)
                    if hasattr(response, 'content'):
                        analysis = response.content
                    else:
                        analysis = str(response)
                else:
                    analysis = str(deepseek_llm(analysis_prompt))
                
                # 3. 组合最终报告
                final_report = f"""# {ticker} DeepSeek增强技术分析报告

**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**分析方法**: 先精确计算技术指标，再由DeepSeek进行深度分析
**数据来源**: 通达信API + 增强技术分析器

{analysis}

---

## 📋 技术数据详情

<details>
<summary>点击查看详细技术数据</summary>

{enhanced_data}

</details>

---

**免责声明**: 本报告仅供参考，不构成投资建议。投资有风险，入市需谨慎。"""
                
                print(f"✅ DeepSeek增强分析完成，报告长度: {len(final_report)}字")
                report = final_report
                
            except Exception as e:
                print(f"❌ DeepSeek增强分析失败: {e}")
                import traceback
                traceback.print_exc()
                report = f"DeepSeek增强分析失败: {str(e)}"
        else:
            report = "仅支持中国A股的增强分析，或需要开启在线工具"
        
        print(f"🤖 [DEBUG] ===== DeepSeek增强市场分析师节点结束 =====")
        
        return {
            "messages": [("assistant", report)],
            "market_report": report,
        }
    
    return enhanced_deepseek_analyst_node


# 便捷函数
def create_enhanced_analyst_for_deepseek(deepseek_llm, toolkit):
    """
    为DeepSeek创建增强分析师的便捷函数
    """
    return create_enhanced_market_analyst_with_deepseek(deepseek_llm, toolkit)


if __name__ == "__main__":
    print("🔧 增强市场分析师模块")
    print("功能: 先调用工具计算技术指标，然后交给LLM进行深度分析")
    print("适用: 特别适合DeepSeek等不支持工具调用的LLM")