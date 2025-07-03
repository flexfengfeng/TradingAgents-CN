#!/usr/bin/env python3
"""
测试增强的DeepSeek技术分析
演示如何先调用工具计算技术指标，然后交给DeepSeek进行深度分析
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tradingagents.utils.analyzers.enhanced_technical_analysis import EnhancedTechnicalAnalyzer
from tradingagents.llm_adapters.deepseek_adapter import create_deepseek_llm
from tradingagents.dataflows.optimized_china_data import get_china_stock_data_cached
from datetime import datetime, timedelta


def test_enhanced_deepseek_analysis():
    """
    测试增强的DeepSeek技术分析
    """
    print("🧪 测试增强的DeepSeek技术分析")
    print("=" * 50)
    
    # 1. 创建DeepSeek LLM
    print("\n🤖 创建DeepSeek LLM...")
    try:
        deepseek_llm = create_deepseek_llm(
            model="deepseek-chat",
            temperature=0.1,  # 降低温度以获得更稳定的分析
            max_tokens=4000   # 增加token数以获得详细分析
        )
        print("✅ DeepSeek LLM创建成功")
    except Exception as e:
        print(f"❌ DeepSeek LLM创建失败: {e}")
        return
    
    # 2. 创建增强技术分析器
    print("\n🔧 创建增强技术分析器...")
    analyzer = EnhancedTechnicalAnalyzer(llm=deepseek_llm)
    print("✅ 增强技术分析器创建成功")
    
    # 3. 获取股票数据
    symbol = "600036"  # 招商银行
    print(f"\n📊 获取股票数据: {symbol}")
    
    try:
        # 获取最近2个月的数据
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')
        
        print(f"📅 数据范围: {start_date} 到 {end_date}")
        
        # 先调用工具获取原始数据
        stock_data = get_china_stock_data_cached(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            force_refresh=False
        )
        
        print(f"✅ 股票数据获取成功，数据长度: {len(stock_data)} 字符")
        print(f"📋 数据预览: {stock_data[:200]}...")
        
    except Exception as e:
        print(f"❌ 股票数据获取失败: {e}")
        # 使用模拟数据进行测试
        print("🔄 使用模拟数据进行测试...")
        stock_data = create_mock_stock_data(symbol)
    
    # 4. 执行增强技术分析
    print("\n🔍 执行增强技术分析...")
    print("-" * 30)
    
    try:
        # 这里会先计算技术指标，然后交给DeepSeek分析
        analysis_report = analyzer.enhanced_technical_analysis(symbol, stock_data)
        
        print("\n📈 增强技术分析报告:")
        print("=" * 50)
        print(analysis_report)
        print("=" * 50)
        
        # 保存报告
        save_report(symbol, analysis_report)
        
    except Exception as e:
        print(f"❌ 增强技术分析失败: {e}")
        import traceback
        traceback.print_exc()


def test_step_by_step_analysis():
    """
    分步测试技术分析流程
    """
    print("\n🔬 分步测试技术分析流程")
    print("=" * 50)
    
    # 1. 创建分析器（不带LLM）
    analyzer = EnhancedTechnicalAnalyzer()
    
    # 2. 使用模拟数据
    symbol = "600036"
    mock_data = create_mock_stock_data(symbol)
    
    print(f"\n📊 模拟数据: {symbol}")
    print(f"数据长度: {len(mock_data)} 字符")
    
    # 3. 解析数据
    print("\n🔍 步骤1: 解析股票数据...")
    df = analyzer._parse_stock_data(mock_data)
    if df is not None:
        print(f"✅ 数据解析成功: {len(df)} 条记录")
        print("📋 数据预览:")
        print(df.head())
        print(f"📊 数据列: {list(df.columns)}")
    else:
        print("❌ 数据解析失败")
        return
    
    # 4. 计算技术指标
    print("\n🔍 步骤2: 计算技术指标...")
    indicators = analyzer.calculate_technical_indicators(df)
    
    if "error" not in indicators:
        print("✅ 技术指标计算成功")
        print("📊 指标概览:")
        for category, data in indicators.items():
            print(f"  - {category}: {type(data).__name__}")
            if isinstance(data, dict) and len(data) < 10:
                for key, value in data.items():
                    print(f"    * {key}: {value}")
    else:
        print(f"❌ 技术指标计算失败: {indicators['error']}")
        return
    
    # 5. 格式化指标
    print("\n🔍 步骤3: 格式化技术指标...")
    formatted_indicators = analyzer.format_indicators_for_analysis(indicators, symbol)
    print("✅ 技术指标格式化成功")
    print("📋 格式化结果预览:")
    print(formatted_indicators[:500] + "...")
    
    # 6. 创建DeepSeek LLM并分析
    print("\n🔍 步骤4: DeepSeek深度分析...")
    try:
        deepseek_llm = create_deepseek_llm(model="deepseek-chat", temperature=0.1)
        analyzer.llm = deepseek_llm
        
        deepseek_analysis = analyzer.analyze_with_deepseek(formatted_indicators, symbol)
        print("✅ DeepSeek分析完成")
        print("📋 分析结果预览:")
        print(deepseek_analysis[:500] + "...")
        
    except Exception as e:
        print(f"❌ DeepSeek分析失败: {e}")


def create_mock_stock_data(symbol: str) -> str:
    """
    创建模拟股票数据用于测试
    """
    import random
    from datetime import datetime, timedelta
    
    # 生成30天的模拟数据
    data_lines = []
    base_price = 35.0
    base_volume = 1000000
    
    for i in range(30):
        date = (datetime.now() - timedelta(days=29-i)).strftime('%Y-%m-%d')
        
        # 模拟价格波动
        change = random.uniform(-0.05, 0.05)  # ±5%波动
        open_price = base_price * (1 + change)
        high_price = open_price * (1 + random.uniform(0, 0.03))
        low_price = open_price * (1 - random.uniform(0, 0.03))
        close_price = open_price + random.uniform(-0.5, 0.5)
        
        # 确保价格合理性
        high_price = max(high_price, open_price, close_price)
        low_price = min(low_price, open_price, close_price)
        
        # 模拟成交量
        volume = int(base_volume * (1 + random.uniform(-0.3, 0.3)))
        
        data_lines.append(f"| {date} | {open_price:.2f} | {high_price:.2f} | {low_price:.2f} | {close_price:.2f} | {volume} |")
        
        # 更新基准价格
        base_price = close_price
    
    mock_data = f"""股票代码: {symbol}
股票名称: 招商银行
数据来源: 模拟数据

历史价格数据:
| 日期 | 开盘 | 最高 | 最低 | 收盘 | 成交量 |
|------|------|------|------|------|--------|
""" + "\n".join(data_lines)
    
    return mock_data


def save_report(symbol: str, report: str):
    """
    保存分析报告
    """
    try:
        from tradingagents.config.output_config import get_analysis_report_path
        
        # 获取报告文件路径
        filename = get_analysis_report_path(symbol)
        
        # 保存报告
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n💾 报告已保存: {filename}")
        
    except Exception as e:
        print(f"❌ 报告保存失败: {e}")


def compare_traditional_vs_enhanced():
    """
    对比传统分析和增强分析的差异
    """
    print("\n⚖️ 对比传统分析 vs 增强分析")
    print("=" * 50)
    
    symbol = "600036"
    mock_data = create_mock_stock_data(symbol)
    
    # 1. 传统分析（直接让LLM分析原始数据）
    print("\n📊 传统分析方式:")
    print("-" * 20)
    
    try:
        deepseek_llm = create_deepseek_llm(model="deepseek-chat", temperature=0.1)
        
        traditional_prompt = f"""请对以下股票数据进行技术分析：

{mock_data}

请提供技术分析报告，包括趋势、指标分析和投资建议。"""
        
        traditional_result = deepseek_llm.invoke(traditional_prompt)
        traditional_analysis = traditional_result.content if hasattr(traditional_result, 'content') else str(traditional_result)
        
        print(f"✅ 传统分析完成，长度: {len(traditional_analysis)} 字符")
        print(f"📋 传统分析预览: {traditional_analysis[:300]}...")
        
    except Exception as e:
        print(f"❌ 传统分析失败: {e}")
        traditional_analysis = "传统分析失败"
    
    # 2. 增强分析（先计算指标再分析）
    print("\n🔧 增强分析方式:")
    print("-" * 20)
    
    try:
        analyzer = EnhancedTechnicalAnalyzer(llm=deepseek_llm)
        enhanced_analysis = analyzer.enhanced_technical_analysis(symbol, mock_data)
        
        print(f"✅ 增强分析完成，长度: {len(enhanced_analysis)} 字符")
        print(f"📋 增强分析预览: {enhanced_analysis[:300]}...")
        
    except Exception as e:
        print(f"❌ 增强分析失败: {e}")
        enhanced_analysis = "增强分析失败"
    
    # 3. 保存对比报告
    comparison_report = f"""# 技术分析方式对比报告

## 股票信息
- 代码: {symbol}
- 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 传统分析方式
（直接让LLM分析原始数据）

{traditional_analysis}

---

## 增强分析方式
（先计算技术指标，再让LLM深度分析）

{enhanced_analysis}

---

## 对比总结

### 传统方式特点：
- 依赖LLM的内置知识
- 可能缺乏精确的数值计算
- 分析可能较为泛泛

### 增强方式特点：
- 先进行精确的技术指标计算
- 基于具体数值进行分析
- 分析更加详细和准确
- 结合了工具计算和AI分析的优势
"""
    
    # 保存对比报告
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        from tradingagents.config.output_config import get_comparison_report_path
        comparison_file = get_comparison_report_path(symbol)
        
        with open(comparison_file, 'w', encoding='utf-8') as f:
            f.write(comparison_report)
        
        print(f"\n💾 对比报告已保存: {comparison_file}")
        
    except Exception as e:
        print(f"❌ 对比报告保存失败: {e}")


if __name__ == "__main__":
    print("🚀 增强DeepSeek技术分析测试")
    print("=" * 60)
    
    # 测试选项
    tests = {
        "1": ("完整增强分析测试", test_enhanced_deepseek_analysis),
        "2": ("分步流程测试", test_step_by_step_analysis),
        "3": ("传统vs增强对比", compare_traditional_vs_enhanced),
        "4": ("运行所有测试", None)
    }
    
    print("\n请选择测试项目:")
    for key, (name, _) in tests.items():
        print(f"  {key}. {name}")
    
    choice = input("\n请输入选择 (1-4): ").strip()
    
    if choice == "4":
        # 运行所有测试
        for key, (name, func) in tests.items():
            if func:
                print(f"\n{'='*20} {name} {'='*20}")
                func()
    elif choice in tests and tests[choice][1]:
        print(f"\n{'='*20} {tests[choice][0]} {'='*20}")
        tests[choice][1]()
    else:
        print("❌ 无效选择")
    
    print("\n🎉 测试完成！")