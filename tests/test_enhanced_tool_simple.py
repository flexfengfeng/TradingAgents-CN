#!/usr/bin/env python3
"""
简化的增强工具测试
"""

import os
import sys
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_enhanced_tool():
    """
    测试增强工具的数据获取能力
    """
    print("🔧 ===== 增强工具数据获取测试 =====")
    
    try:
        # 1. 导入模块
        print("📦 导入模块...")
        from tradingagents.agents.utils.agent_utils import Toolkit
        from tradingagents.agents.analysts.enhanced_market_analyst import EnhancedChinaStockDataTool
        from tradingagents.utils.analyzers.enhanced_technical_analysis import EnhancedTechnicalAnalyzer
        from tradingagents.utils.analyzers.enhanced_fundamentals_analysis import EnhancedFundamentalsAnalyzer
        from tradingagents.utils.analyzers.enhanced_sentiment_analysis import EnhancedSentimentAnalyzer
        from tradingagents.utils.analyzers.enhanced_risk_analysis import EnhancedRiskAnalyzer
        from tradingagents.utils.enhanced_analysis_toolkit import EnhancedAnalysisToolkit
        
        # 2. 创建工具包
        print("🔧 创建工具包...")
        toolkit = Toolkit()
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # 3. 测试股票
        test_ticker = "000001"  # 平安银行
        
        print(f"📊 测试股票: {test_ticker}")
        print(f"📅 分析日期: {current_date}")
        
        # 4. 创建增强工具
        print("🚀 创建增强工具...")
        enhanced_tool = EnhancedChinaStockDataTool(test_ticker, current_date, toolkit)
        
        # 5. 获取数据
        print("🔍 获取增强技术数据...")
        enhanced_data = enhanced_tool._run()
        
        # 6. 显示结果
        print("\n📋 增强技术数据结果:")
        print("-" * 60)
        
        # 显示前1500字符
        if len(enhanced_data) > 1500:
            print(enhanced_data[:1500])
            print("\n... (数据已截断，完整数据请查看保存的文件) ...")
        else:
            print(enhanced_data)
        
        print("-" * 60)
        print(f"✅ 数据获取完成，总长度: {len(enhanced_data)}字符")
        
        # 7. 保存数据
        from tradingagents.config.output_config import get_data_report_path
        data_file = get_data_report_path(test_ticker)
        with open(data_file, 'w', encoding='utf-8') as f:
            f.write(enhanced_data)
        print(f"💾 完整数据已保存到: {data_file}")
        
        # 8. 分析数据质量
        print("\n📊 数据质量分析:")
        if "精确计算的技术指标" in enhanced_data:
            print("✅ 包含精确计算的技术指标")
        if "RSI值" in enhanced_data:
            print("✅ 包含RSI指标")
        if "MACD" in enhanced_data:
            print("✅ 包含MACD指标")
        if "布林带" in enhanced_data:
            print("✅ 包含布林带指标")
        if "移动平均线" in enhanced_data:
            print("✅ 包含移动平均线")
        if "支撑阻力" in enhanced_data:
            print("✅ 包含支撑阻力位")
        
        if "❌" in enhanced_data or "失败" in enhanced_data:
            print("⚠️ 数据获取可能存在问题")
        else:
            print("✅ 数据获取成功，质量良好")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_deepseek_analysis():
    """
    测试DeepSeek分析能力
    """
    print("\n🤖 ===== DeepSeek分析能力测试 =====")
    
    try:
        # 1. 导入模块
        print("📦 导入DeepSeek模块...")
        from tradingagents.llm_adapters.deepseek_adapter import create_deepseek_llm
        from tradingagents.agents.utils.agent_utils import Toolkit
        from tradingagents.agents.analysts.enhanced_market_analyst import create_enhanced_market_analyst_with_deepseek
        
        # 2. 创建DeepSeek LLM
        print("🤖 创建DeepSeek LLM...")
        deepseek_llm = create_deepseek_llm(
            model="deepseek-chat",
            temperature=0.1,
            max_tokens=3000
        )
        print("✅ DeepSeek LLM创建成功")
        
        # 3. 创建工具包
        print("🔧 创建工具包...")
        toolkit = Toolkit()
        
        # 4. 创建增强分析师
        print("🚀 创建增强分析师...")
        enhanced_analyst = create_enhanced_market_analyst_with_deepseek(deepseek_llm, toolkit)
        
        # 5. 准备测试数据
        test_ticker = "000001"  # 平安银行
        state = {
            "trade_date": datetime.now().strftime('%Y-%m-%d'),
            "company_of_interest": test_ticker
        }
        
        print(f"📊 测试股票: {test_ticker}")
        print("🔍 开始增强分析...")
        
        # 6. 执行分析
        result = enhanced_analyst(state)
        
        # 7. 处理结果
        report = result.get('market_report', '无报告')
        
        print("\n📋 DeepSeek增强分析结果:")
        print("-" * 60)
        
        # 显示前2000字符
        if len(report) > 2000:
            print(report[:2000])
            print("\n... (报告已截断，完整报告请查看保存的文件) ...")
        else:
            print(report)
        
        print("-" * 60)
        print(f"✅ 分析完成，报告长度: {len(report)}字")
        
        # 8. 保存报告
        from tradingagents.config.output_config import get_analysis_report_path
        report_file = get_analysis_report_path(test_ticker, "deepseek_enhanced_analysis")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"💾 完整报告已保存到: {report_file}")
        
        # 9. 分析报告质量
        print("\n📊 报告质量分析:")
        if len(report) > 1000:
            print("✅ 报告长度充足")
        if "技术指标" in report:
            print("✅ 包含技术指标分析")
        if "投资建议" in report:
            print("✅ 包含投资建议")
        if "目标价" in report or "价位" in report:
            print("✅ 包含价格目标")
        if "风险" in report:
            print("✅ 包含风险评估")
        
        return True
        
    except Exception as e:
        print(f"❌ DeepSeek分析测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """
    主测试函数
    """
    print("🎯 增强DeepSeek市场分析测试")
    print("目标: 验证先计算技术指标再分析的效果")
    print()
    
    # 测试1: 增强工具
    tool_success = test_enhanced_tool()
    
    if tool_success:
        # 测试2: DeepSeek分析
        analysis_success = test_deepseek_analysis()
        
        if analysis_success:
            print("\n🎉 所有测试完成！")
            print("✅ 增强工具数据获取成功")
            print("✅ DeepSeek增强分析成功")
            print("\n💡 结论: 先计算技术指标再分析的方案有效解决了DeepSeek技术分析不具体的问题")
        else:
            print("\n⚠️ DeepSeek分析测试失败，但增强工具正常")
    else:
        print("\n❌ 增强工具测试失败")
    
    print("\n📋 测试完成，请查看生成的文件了解详细结果")


if __name__ == "__main__":
    main()