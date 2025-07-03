#!/usr/bin/env python3
"""
增强的技术分析实现
先调用工具计算技术指标，然后交给DeepSeek进行深度分析
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any


class EnhancedTechnicalAnalyzer:
    """
    增强的技术分析器
    1. 先调用数据工具获取原始数据
    2. 计算详细的技术指标
    3. 将计算结果传递给DeepSeek进行深度分析
    """
    
    def __init__(self, llm=None):
        self.llm = llm
        print("🔧 增强技术分析器初始化完成")
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        计算全面的技术指标
        
        Args:
            df: 包含OHLCV数据的DataFrame
        
        Returns:
            Dict: 计算好的技术指标
        """
        print("📊 开始计算技术指标...")
        
        indicators = {}
        
        try:
            # 确保数据足够
            if len(df) < 5:
                return {"error": "数据不足，无法计算技术指标"}
            
            # 基础价格信息
            current_price = df['Close'].iloc[-1]
            prev_close = df['Close'].iloc[-2] if len(df) > 1 else current_price
            high_52w = df['High'].rolling(252).max().iloc[-1] if len(df) >= 252 else df['High'].max()
            low_52w = df['Low'].rolling(252).min().iloc[-1] if len(df) >= 252 else df['Low'].min()
            
            indicators['price_info'] = {
                'current_price': round(current_price, 2),
                'prev_close': round(prev_close, 2),
                'change': round(current_price - prev_close, 2),
                'change_pct': round((current_price - prev_close) / prev_close * 100, 2),
                'high_52w': round(high_52w, 2),
                'low_52w': round(low_52w, 2),
                'from_52w_high': round((current_price - high_52w) / high_52w * 100, 2),
                'from_52w_low': round((current_price - low_52w) / low_52w * 100, 2)
            }
            
            # 移动平均线
            indicators['moving_averages'] = {}
            for period in [5, 10, 20, 50, 200]:
                if len(df) >= period:
                    ma = df['Close'].rolling(period).mean().iloc[-1]
                    indicators['moving_averages'][f'MA{period}'] = {
                        'value': round(ma, 2),
                        'distance': round((current_price - ma) / ma * 100, 2),
                        'trend': 'up' if df['Close'].rolling(period).mean().iloc[-1] > df['Close'].rolling(period).mean().iloc[-2] else 'down'
                    }
            
            # 指数移动平均线
            indicators['ema'] = {}
            for period in [12, 26]:
                if len(df) >= period:
                    ema = df['Close'].ewm(span=period).mean().iloc[-1]
                    indicators['ema'][f'EMA{period}'] = {
                        'value': round(ema, 2),
                        'distance': round((current_price - ema) / ema * 100, 2)
                    }
            
            # RSI计算
            if len(df) >= 14:
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                
                current_rsi = rsi.iloc[-1]
                indicators['rsi'] = {
                    'value': round(current_rsi, 2),
                    'signal': 'overbought' if current_rsi > 70 else 'oversold' if current_rsi < 30 else 'neutral',
                    'trend': 'up' if rsi.iloc[-1] > rsi.iloc[-2] else 'down'
                }
            
            # MACD计算
            if len(df) >= 26:
                exp1 = df['Close'].ewm(span=12).mean()
                exp2 = df['Close'].ewm(span=26).mean()
                macd_line = exp1 - exp2
                signal_line = macd_line.ewm(span=9).mean()
                histogram = macd_line - signal_line
                
                indicators['macd'] = {
                    'macd_line': round(macd_line.iloc[-1], 4),
                    'signal_line': round(signal_line.iloc[-1], 4),
                    'histogram': round(histogram.iloc[-1], 4),
                    'signal': 'bullish' if macd_line.iloc[-1] > signal_line.iloc[-1] else 'bearish',
                    'momentum': 'increasing' if histogram.iloc[-1] > histogram.iloc[-2] else 'decreasing'
                }
            
            # 布林带
            if len(df) >= 20:
                sma20 = df['Close'].rolling(20).mean()
                std20 = df['Close'].rolling(20).std()
                bb_upper = sma20 + (std20 * 2)
                bb_lower = sma20 - (std20 * 2)
                bb_width = (bb_upper - bb_lower) / sma20 * 100
                
                indicators['bollinger_bands'] = {
                    'upper': round(bb_upper.iloc[-1], 2),
                    'middle': round(sma20.iloc[-1], 2),
                    'lower': round(bb_lower.iloc[-1], 2),
                    'width': round(bb_width.iloc[-1], 2),
                    'position': round((current_price - bb_lower.iloc[-1]) / (bb_upper.iloc[-1] - bb_lower.iloc[-1]) * 100, 2),
                    'squeeze': 'yes' if bb_width.iloc[-1] < bb_width.rolling(20).mean().iloc[-1] else 'no'
                }
            
            # 成交量分析
            if 'Volume' in df.columns:
                avg_volume_20 = df['Volume'].rolling(20).mean().iloc[-1]
                current_volume = df['Volume'].iloc[-1]
                
                # 检查是否有有效的成交量数据
                if not pd.isna(current_volume) and not pd.isna(avg_volume_20) and avg_volume_20 > 0:
                    indicators['volume'] = {
                        'current': int(current_volume),
                        'avg_20d': int(avg_volume_20),
                        'ratio': round(current_volume / avg_volume_20, 2),
                        'trend': 'increasing' if len(df) >= 6 and df['Volume'].rolling(5).mean().iloc[-1] > df['Volume'].rolling(5).mean().iloc[-6] else 'decreasing'
                    }
                else:
                    indicators['volume'] = {
                        'current': 0,
                        'avg_20d': 0,
                        'ratio': 0,
                        'trend': 'unknown'
                    }
            
            # 波动率(ATR)
            if len(df) >= 14:
                high_low = df['High'] - df['Low']
                high_close = np.abs(df['High'] - df['Close'].shift())
                low_close = np.abs(df['Low'] - df['Close'].shift())
                ranges = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
                atr = ranges.rolling(14).mean().iloc[-1]
                
                indicators['atr'] = {
                    'value': round(atr, 2),
                    'percentage': round(atr / current_price * 100, 2)
                }
            
            # 支撑阻力位
            recent_highs = df['High'].rolling(20).max()
            recent_lows = df['Low'].rolling(20).min()
            
            indicators['support_resistance'] = {
                'resistance': round(recent_highs.iloc[-1], 2),
                'support': round(recent_lows.iloc[-1], 2),
                'distance_to_resistance': round((recent_highs.iloc[-1] - current_price) / current_price * 100, 2),
                'distance_to_support': round((current_price - recent_lows.iloc[-1]) / current_price * 100, 2)
            }
            
            print("✅ 技术指标计算完成")
            return indicators
            
        except Exception as e:
            print(f"❌ 技术指标计算失败: {e}")
            return {"error": f"技术指标计算失败: {str(e)}"}
    
    def format_indicators_for_analysis(self, indicators: Dict[str, Any], symbol: str) -> str:
        """
        将计算好的技术指标格式化为适合LLM分析的文本
        
        Args:
            indicators: 计算好的技术指标
            symbol: 股票代码
        
        Returns:
            str: 格式化的技术指标报告
        """
        if "error" in indicators:
            return f"技术指标计算失败: {indicators['error']}"
        
        report = f"""# {symbol} 技术指标详细数据

## 价格信息
- 当前价格: {indicators['price_info']['current_price']}
- 昨日收盘: {indicators['price_info']['prev_close']}
- 涨跌额: {indicators['price_info']['change']}
- 涨跌幅: {indicators['price_info']['change_pct']}%
- 52周最高: {indicators['price_info']['high_52w']}
- 52周最低: {indicators['price_info']['low_52w']}
- 距52周高点: {indicators['price_info']['from_52w_high']}%
- 距52周低点: {indicators['price_info']['from_52w_low']}%

## 移动平均线分析"""
        
        for ma_name, ma_data in indicators.get('moving_averages', {}).items():
            report += f"""
- {ma_name}: {ma_data['value']} (距离: {ma_data['distance']}%, 趋势: {ma_data['trend']})"""
        
        if 'ema' in indicators:
            report += "\n\n## 指数移动平均线"
            for ema_name, ema_data in indicators['ema'].items():
                report += f"""
- {ema_name}: {ema_data['value']} (距离: {ema_data['distance']}%)"""
        
        if 'rsi' in indicators:
            rsi_data = indicators['rsi']
            report += f"""

## RSI相对强弱指标
- RSI值: {rsi_data['value']}
- 信号: {rsi_data['signal']}
- 趋势: {rsi_data['trend']}"""
        
        if 'macd' in indicators:
            macd_data = indicators['macd']
            report += f"""

## MACD指标
- MACD线: {macd_data['macd_line']}
- 信号线: {macd_data['signal_line']}
- 柱状图: {macd_data['histogram']}
- 信号: {macd_data['signal']}
- 动量: {macd_data['momentum']}"""
        
        if 'bollinger_bands' in indicators:
            bb_data = indicators['bollinger_bands']
            report += f"""

## 布林带
- 上轨: {bb_data['upper']}
- 中轨: {bb_data['middle']}
- 下轨: {bb_data['lower']}
- 带宽: {bb_data['width']}%
- 价格位置: {bb_data['position']}%
- 收缩状态: {bb_data['squeeze']}"""
        
        if 'volume' in indicators:
            vol_data = indicators['volume']
            report += f"""

## 成交量分析
- 当前成交量: {vol_data['current']:,}
- 20日平均: {vol_data['avg_20d']:,}
- 量比: {vol_data['ratio']}
- 趋势: {vol_data['trend']}"""
        
        if 'atr' in indicators:
            atr_data = indicators['atr']
            report += f"""

## 波动率(ATR)
- ATR值: {atr_data['value']}
- 占价格比例: {atr_data['percentage']}%"""
        
        if 'support_resistance' in indicators:
            sr_data = indicators['support_resistance']
            report += f"""

## 支撑阻力位
- 阻力位: {sr_data['resistance']}
- 支撑位: {sr_data['support']}
- 距阻力位: {sr_data['distance_to_resistance']}%
- 距支撑位: {sr_data['distance_to_support']}%"""
        
        return report
    
    def analyze_with_deepseek(self, technical_data: str, symbol: str) -> str:
        """
        使用DeepSeek对技术指标进行深度分析
        
        Args:
            technical_data: 格式化的技术指标数据
            symbol: 股票代码
        
        Returns:
            str: DeepSeek的分析结果
        """
        if not self.llm:
            return "未配置LLM，无法进行深度分析"
        
        prompt = f"""你是一位资深的技术分析专家，请基于以下详细的技术指标数据，对股票{symbol}进行深入的技术分析。

{technical_data}

请提供以下分析：

1. **趋势分析**：基于移动平均线和价格走势，判断短期、中期、长期趋势
2. **动量分析**：基于RSI、MACD等指标，分析当前动量状态和可能的转折点
3. **波动性分析**：基于布林带、ATR等指标，评估当前波动性和风险水平
4. **成交量分析**：结合价格和成交量，分析资金流向和市场参与度
5. **支撑阻力分析**：识别关键的支撑阻力位，预测可能的价格目标
6. **综合评估**：给出明确的投资建议（买入/持有/卖出）和目标价位
7. **风险提示**：指出当前技术面存在的主要风险

要求：
- 分析必须基于提供的具体数值，不要泛泛而谈
- 给出具体的价格目标和止损位
- 分析要逻辑清晰，结论明确
- 字数不少于800字"""
        
        try:
            print(f"🤖 使用DeepSeek分析技术指标...")
            
            # 调用DeepSeek进行分析
            if hasattr(self.llm, 'invoke'):
                response = self.llm.invoke(prompt)
                if hasattr(response, 'content'):
                    analysis = response.content
                else:
                    analysis = str(response)
            else:
                analysis = str(self.llm(prompt))
            
            print(f"✅ DeepSeek技术分析完成，长度: {len(analysis)}字")
            return analysis
            
        except Exception as e:
            error_msg = f"DeepSeek分析失败: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def enhanced_technical_analysis(self, symbol: str, stock_data: str) -> str:
        """
        增强的技术分析主函数
        
        Args:
            symbol: 股票代码
            stock_data: 原始股票数据
        
        Returns:
            str: 完整的技术分析报告
        """
        print(f"🔍 开始增强技术分析: {symbol}")
        
        try:
            # 1. 解析股票数据
            df = self._parse_stock_data(stock_data)
            if df is None or df.empty:
                return f"无法解析股票数据: {symbol}"
            
            print(f"📊 解析到 {len(df)} 条数据记录")
            
            # 2. 计算技术指标
            indicators = self.calculate_technical_indicators(df)
            if "error" in indicators:
                return f"技术指标计算失败: {indicators['error']}"
            
            # 3. 格式化技术指标
            formatted_indicators = self.format_indicators_for_analysis(indicators, symbol)
            
            # 4. 使用DeepSeek进行深度分析
            deepseek_analysis = self.analyze_with_deepseek(formatted_indicators, symbol)
            
            # 5. 组合最终报告
            final_report = f"""# {symbol} 增强技术分析报告

## 技术指标计算结果
{formatted_indicators}

## DeepSeek深度分析
{deepseek_analysis}

---
*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*分析方法: 先计算技术指标，再由DeepSeek进行深度分析*"""
            
            print(f"✅ 增强技术分析完成，报告长度: {len(final_report)}字")
            return final_report
            
        except Exception as e:
            error_msg = f"增强技术分析失败: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def _parse_stock_data(self, stock_data: str) -> Optional[pd.DataFrame]:
        """
        解析股票数据字符串为DataFrame
        
        Args:
            stock_data: 股票数据字符串
        
        Returns:
            pd.DataFrame: 解析后的数据
        """
        try:
            # 尝试从数据中提取DataFrame表格部分
            lines = stock_data.split('\n')
            data_lines = []
            header_line = None
            data_start = False
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                
                # 寻找DataFrame表格头（包含Open、Close、High、Low等列）
                if ('Open' in line and 'Close' in line and 'High' in line and 'Low' in line) or \
                   ('datetime' in line and any(col in line for col in ['Open', 'Close', 'High', 'Low'])):
                    header_line = line
                    data_start = True
                    continue
                
                # 直接查找数据行（包含日期时间格式的行）
                if any(char.isdigit() for char in line) and ('2025' in line or '2024' in line or '2023' in line):
                    # 检查是否是标准的datetime格式开头的数据行
                    if line.startswith('2025-') or line.startswith('2024-') or line.startswith('2023-'):
                        # 分割数据行，处理空格分隔的数据
                        parts = line.split()
                        if len(parts) >= 6:  # 至少需要datetime + OHLCV
                            data_lines.append(parts)
                            data_start = True  # 标记已找到数据
                elif '数据来源' in line or '生成时间' in line:
                    # 遇到数据来源说明，停止解析
                    break
            
            if not data_lines:
                print("❌ 未找到有效的股票数据表格")
                return None
            
            # 解析表头
            if header_line:
                headers = header_line.split()
            else:
                # 使用默认列名
                headers = ['datetime', 'Open', 'Close', 'High', 'Low', 'Volume', 'Amount', 'year', 'month', 'day', 'hour', 'minute', 'Symbol']
            
            # 创建DataFrame
            max_cols = max(len(row) for row in data_lines)
            
            # 确保所有数据行都有相同的列数
            normalized_data = []
            for row in data_lines:
                if len(row) < max_cols:
                    # 补齐缺失的列
                    row.extend([''] * (max_cols - len(row)))
                elif len(row) > max_cols:
                    # 截断多余的列
                    row = row[:max_cols]
                normalized_data.append(row)
            
            # 确保列名数量匹配
            if len(headers) < max_cols:
                # 补齐缺失的列名
                for i in range(len(headers), max_cols):
                    headers.append(f'col_{i}')
            elif len(headers) > max_cols:
                # 截断多余的列名
                headers = headers[:max_cols]
            
            df = pd.DataFrame(normalized_data, columns=headers)
            
            # 数据类型转换
            try:
                # 处理datetime列 - 合并日期和时间列
                if len(df.columns) >= 2 and df.iloc[0, 0].count('-') == 2 and df.iloc[0, 1].count(':') == 2:
                    # 第一列是日期，第二列是时间
                    df['datetime'] = pd.to_datetime(df.iloc[:, 0] + ' ' + df.iloc[:, 1], errors='coerce')
                    df = df.set_index('datetime')
                    # 移除原来的日期和时间列
                    df = df.drop(df.columns[[0, 1]], axis=1)
                    # 更新列名
                    new_headers = ['Open', 'Close', 'High', 'Low', 'Volume', 'Amount'] + [f'col_{i}' for i in range(6, len(df.columns))]
                    df.columns = new_headers[:len(df.columns)]
                elif 'datetime' in df.columns:
                    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
                    df = df.set_index('datetime')
                
                # 转换数值列
                numeric_cols = ['Open', 'Close', 'High', 'Low', 'Volume', 'Amount']
                for col in numeric_cols:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # 确保必要的列存在
                required_cols = ['Open', 'High', 'Low', 'Close']
                missing_cols = [col for col in required_cols if col not in df.columns]
                if missing_cols:
                    print(f"❌ 缺少必要列: {missing_cols}")
                    return None
                
                # 删除无效行
                df = df.dropna(subset=['Close'])
                
                # 按日期排序
                if df.index.name == 'datetime':
                    df = df.sort_index()
                
                print(f"✅ 成功解析股票数据，共 {len(df)} 条记录")
                print(f"📊 数据列: {list(df.columns)}")
                print(f"📅 数据时间范围: {df.index.min()} 到 {df.index.max()}")
                return df
                
            except Exception as e:
                print(f"❌ 数据类型转换失败: {e}")
                return None
            
        except Exception as e:
            print(f"❌ 股票数据解析失败: {e}")
            return None


# 便捷函数
def create_enhanced_analyzer(llm=None):
    """创建增强技术分析器实例"""
    return EnhancedTechnicalAnalyzer(llm=llm)


def enhanced_technical_analysis(symbol: str, stock_data: str, llm=None) -> str:
    """
    便捷的增强技术分析函数
    
    Args:
        symbol: 股票代码
        stock_data: 股票数据
        llm: DeepSeek LLM实例
    
    Returns:
        str: 技术分析报告
    """
    analyzer = EnhancedTechnicalAnalyzer(llm=llm)
    return analyzer.enhanced_technical_analysis(symbol, stock_data)


if __name__ == "__main__":
    # 测试代码
    print("🧪 增强技术分析器测试")
    
    # 创建分析器
    analyzer = EnhancedTechnicalAnalyzer()
    
    # 模拟数据测试
    test_data = """
股票代码: 600036
股票名称: 招商银行

| 日期 | 开盘 | 最高 | 最低 | 收盘 | 成交量 |
|------|------|------|------|------|--------|
| 2025-01-01 | 34.50 | 35.20 | 34.20 | 34.80 | 1000000 |
| 2025-01-02 | 34.80 | 35.50 | 34.60 | 35.20 | 1200000 |
| 2025-01-03 | 35.20 | 35.80 | 35.00 | 35.60 | 1100000 |
"""
    
    # 解析测试
    df = analyzer._parse_stock_data(test_data)
    if df is not None:
        print(f"✅ 数据解析成功: {len(df)} 条记录")
        print(df.head())
    else:
        print("❌ 数据解析失败")