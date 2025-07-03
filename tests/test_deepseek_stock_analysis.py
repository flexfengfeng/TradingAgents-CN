#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek股票分析实战测试
演示如何使用DeepSeek AI进行实际的股票分析
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tradingagents.config.config_manager import ConfigManager
from tradingagents.llm_adapters.deepseek_adapter import create_deepseek_llm

def test_deepseek_stock_analysis():
    """
    使用DeepSeek进行实际股票分析测试
    """
    print("🚀 DeepSeek股票分析实战测试")
    print("=" * 50)
    
    # 检查API密钥
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        print("❌ 错误: 未找到DEEPSEEK_API_KEY环境变量")
        print("💡 请在.env文件中设置: DEEPSEEK_API_KEY=your_api_key")
        return False
    
    print(f"✅ DeepSeek API密钥已配置 (前缀: {api_key[:10]}...)")
    
    try:
        # 1. 创建配置管理器
        print("\n📋 初始化配置管理器...")
        config_manager = ConfigManager()
        
        # 2. 创建DeepSeek LLM
        print("🧠 创建DeepSeek LLM实例...")
        deepseek_llm = create_deepseek_llm(
            model_name="deepseek-chat",
            temperature=0.1,  # 较低温度确保分析的一致性
            max_tokens=2000
        )
        
        print(f"✅ DeepSeek LLM创建成功: {deepseek_llm.model_name}")
        
        # 3. 进行股票分析
        print("\n🔍 开始股票分析...")
        print("-" * 30)
        
        # 分析苹果公司股票
        symbol = "AAPL"
        print(f"📊 分析股票: {symbol} (苹果公司)")
        
        # 构建分析请求
        analysis_request = f"""
请对{symbol}股票进行全面分析，包括：

1. 公司基本面分析
   - 业务模式和竞争优势
   - 财务状况评估
   - 管理层表现

2. 技术面分析
   - 股价趋势分析
   - 关键技术指标
   - 支撑位和阻力位

3. 市场情绪分析
   - 投资者情绪
   - 分析师评级
   - 市场预期

4. 投资建议
   - 目标价位
   - 风险评估
   - 投资时间框架

请用中文回答，并提供具体的分析依据和数据支持。
"""
        
        print(f"💭 分析请求长度: {len(analysis_request)} 字符")
        
        # 执行分析
        print("⏳ DeepSeek正在分析中...")
        
        # 使用LLM进行分析
        response = deepseek_llm.invoke(analysis_request)
        
        print("\n📋 DeepSeek分析结果:")
        print("=" * 50)
        print(response)
        print("=" * 50)
        
        # 4. 成本统计
        print("\n💰 成本统计:")
        if hasattr(deepseek_llm, 'get_token_count'):
            input_tokens = deepseek_llm.get_token_count(analysis_request)
            output_tokens = deepseek_llm.get_token_count(response)
            
            print(f"📥 输入tokens: {input_tokens}")
            print(f"📤 输出tokens: {output_tokens}")
            
            # 计算成本
            total_cost = config_manager.calculate_cost(
                provider="deepseek",
                model_name="deepseek-chat",
                input_tokens=input_tokens,
                output_tokens=output_tokens
            )
            print(f"💵 总成本: {total_cost:.6f} CNY")
            print(f"💡 成本效益: 约 {total_cost*1000:.3f} 分钱")
        
        print("\n✅ DeepSeek股票分析测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_deepseek_multiple_stocks():
    """
    测试DeepSeek分析多只股票
    """
    print("\n🔄 DeepSeek多股票对比分析测试")
    print("=" * 50)
    
    stocks = ["AAPL", "MSFT", "GOOGL"]
    
    try:
        config_manager = ConfigManager()
        deepseek_llm = create_deepseek_llm(
            model_name="deepseek-coder",  # 使用coder模型进行更结构化的分析
            temperature=0.2
        )
        
        analysis_request = f"""
请对以下科技股进行对比分析：{', '.join(stocks)}

请从以下角度进行详细对比：

1. 估值水平对比
   - P/E比率
   - P/B比率
   - PEG比率

2. 成长性对比
   - 营收增长率
   - 利润增长率
   - 市场份额变化

3. 财务健康度对比
   - 现金流状况
   - 负债率
   - ROE/ROA

4. 风险评估对比
   - 业务风险
   - 市场风险
   - 监管风险

5. 投资优先级排序
   - 短期投资价值（1-6个月）
   - 中期投资价值（6-18个月）
   - 长期投资价值（2-5年）

请用表格形式总结关键指标，并给出明确的投资建议和理由。
"""
        
        print(f"💭 多股票分析请求: {len(stocks)}只股票")
        print("⏳ DeepSeek正在进行对比分析...")
        
        response = deepseek_llm.invoke(analysis_request)
        
        print("\n📊 DeepSeek多股票对比分析结果:")
        print("=" * 60)
        print(response)
        print("=" * 60)
        
        # 成本统计
        if hasattr(deepseek_llm, 'get_token_count'):
            input_tokens = deepseek_llm.get_token_count(analysis_request)
            output_tokens = deepseek_llm.get_token_count(response)
            
            config_manager = ConfigManager()
            total_cost = config_manager.calculate_cost(
                provider="deepseek",
                model_name="deepseek-coder",
                input_tokens=input_tokens,
                output_tokens=output_tokens
            )
            print(f"\n💰 多股票分析成本: {total_cost:.6f} CNY")
        
        return True
        
    except Exception as e:
        print(f"❌ 多股票分析测试失败: {str(e)}")
        return False

def test_deepseek_chinese_stocks():
    """
    测试DeepSeek分析中国股票
    """
    print("\n🇨🇳 DeepSeek中国股票分析测试")
    print("=" * 50)
    
    try:
        deepseek_llm = create_deepseek_llm(
            model_name="deepseek-chat",
            temperature=0.1
        )
        
        analysis_request = """
请分析以下中国科技股的投资价值：

1. 腾讯控股 (00700.HK)
2. 阿里巴巴 (09988.HK / BABA)
3. 美团 (03690.HK)
4. 比亚迪 (002594.SZ)

分析要点：
- 当前估值是否合理
- 政策环境影响
- 竞争格局变化
- 未来增长潜力
- 投资风险提示

请结合中国市场特点和监管环境，给出专业的投资建议。
"""
        
        print("⏳ DeepSeek正在分析中国股票...")
        response = deepseek_llm.invoke(analysis_request)
        
        print("\n🇨🇳 DeepSeek中国股票分析结果:")
        print("=" * 60)
        print(response)
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ 中国股票分析测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 DeepSeek股票分析实战测试套件")
    print("=" * 60)
    
    # 测试1: 单股票深度分析
    success1 = test_deepseek_stock_analysis()
    
    # 测试2: 多股票对比分析
    success2 = test_deepseek_multiple_stocks()
    
    # 测试3: 中国股票分析
    success3 = test_deepseek_chinese_stocks()
    
    # 总结
    print("\n📊 测试结果汇总:")
    print("-" * 30)
    print(f"   单股票分析: {'✅ 通过' if success1 else '❌ 失败'}")
    print(f"   多股票对比: {'✅ 通过' if success2 else '❌ 失败'}")
    print(f"   中国股票分析: {'✅ 通过' if success3 else '❌ 失败'}")
    
    total_success = sum([success1, success2, success3])
    print(f"\n🎯 总计: {total_success}/3 个测试通过")
    
    if total_success == 3:
        print("\n🎉 所有测试通过！DeepSeek可以成功进行股票分析！")
        print("\n💡 使用建议:")
        print("   - deepseek-chat: 适合自然语言分析和解释")
        print("   - deepseek-coder: 适合结构化分析和数据处理")
        print("   - 成本极低: 约0.001-0.002 CNY/1k tokens")
        print("   - 中文支持优秀，适合中国股市分析")
        print("   - 推理能力强，适合复杂的金融分析")
    elif total_success > 0:
        print(f"\n⚠️  部分测试通过 ({total_success}/3)，DeepSeek基本功能正常")
    else:
        print("\n❌ 所有测试失败，请检查配置和网络连接")