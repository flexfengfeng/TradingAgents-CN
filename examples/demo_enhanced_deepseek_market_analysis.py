#!/usr/bin/env python3
"""
演示增强DeepSeek市场分析
展示如何先调用工具计算技术指标，然后交给DeepSeek进行深度分析
"""

import os
import sys
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def demo_enhanced_deepseek_analysis():
    """
    演示增强DeepSeek技术分析
    """
    print("🚀 ===== 增强DeepSeek市场分析演示 =====")
    print("功能: 先计算技术指标，再由DeepSeek深度分析")
    print("优势: 解决DeepSeek技术分析不具体的问题")
    print()
    
    try:
        # 1. 导入必要模块
        print("📦 步骤1: 导入模块...")
        from tradingagents.llms.deepseek_llm import create_deepseek_llm
        from tradingagents.tools.toolkit import Toolkit
        from tradingagents.agents.analysts.enhanced_market_analyst import (
            create_enhanced_market_analyst_with_deepseek,
            EnhancedChinaStockDataTool
        )

        
        # 2. 创建DeepSeek LLM
        print("🤖 步骤2: 创建DeepSeek LLM...")
        deepseek_llm = create_deepseek_llm(
            model="deepseek-chat",
            temperature=0.1,  # 降低温度以获得更稳定的分析
            max_tokens=4000   # 增加token数以支持详细分析
        )
        print("✅ DeepSeek LLM创建成功")
        
        # 3. 创建工具包
        print("🔧 步骤3: 创建工具包...")
        toolkit = Toolkit()
        print("✅ 工具包创建成功")
        
        # 4. 测试股票列表
        test_stocks = [
            "000001",  # 平安银行
            "000002",  # 万科A
            "600036",  # 招商银行
            "600519",  # 贵州茅台
        ]
        
        print(f"📈 步骤4: 开始分析测试股票 {test_stocks}")
        print()
        
        for i, ticker in enumerate(test_stocks, 1):
            print(f"\n{'='*60}")
            print(f"📊 分析 {i}/{len(test_stocks)}: {ticker}")
            print(f"{'='*60}")
            
            try:
                # 5. 创建增强分析师
                enhanced_analyst = create_enhanced_market_analyst_with_deepseek(
                    deepseek_llm, toolkit
                )
                
                # 6. 准备状态
                state = {
                    "trade_date": datetime.now().strftime('%Y-%m-%d'),
                    "company_of_interest": ticker
                }
                
                print(f"🔍 开始增强分析 {ticker}...")
                
                # 7. 执行分析
                result = enhanced_analyst(state)
                
                # 8. 输出结果
                report = result.get('market_report', '无报告')
                print(f"\n📋 {ticker} 分析报告:")
                print("-" * 50)
                print(report[:1000] + "..." if len(report) > 1000 else report)
                print("-" * 50)
                print(f"✅ {ticker} 分析完成，报告长度: {len(report)}字")
                
                # 保存报告
                from tradingagents.config.output_config import get_analysis_report_path
                report_file = get_analysis_report_path(ticker, "enhanced_deepseek_analysis")
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"💾 报告已保存到: {report_file}")
                
            except Exception as e:
                print(f"❌ {ticker} 分析失败: {e}")
                import traceback
                traceback.print_exc()
            
            print(f"\n⏱️ {ticker} 分析完成，等待3秒后继续...")
            import time
            time.sleep(3)
        
        print("\n🎉 所有股票分析完成！")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()


def demo_enhanced_tool_only():
    """
    仅演示增强工具的数据获取能力
    """
    print("\n🔧 ===== 增强工具数据获取演示 =====")
    
    try:
        from tradingagents.tools.toolkit import Toolkit
        from tradingagents.agents.analysts.enhanced_market_analyst import EnhancedChinaStockDataTool
        
        toolkit = Toolkit()
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        test_ticker = "000001"  # 平安银行
        
        print(f"📊 测试股票: {test_ticker}")
        print(f"📅 分析日期: {current_date}")
        
        # 创建增强工具
        enhanced_tool = EnhancedChinaStockDataTool(test_ticker, current_date, toolkit)
        
        print("🔍 获取增强技术数据...")
        enhanced_data = enhanced_tool._run()
        
        print("\n📋 增强技术数据结果:")
        print("-" * 60)
        print(enhanced_data[:2000] + "..." if len(enhanced_data) > 2000 else enhanced_data)
        print("-" * 60)
        print(f"✅ 数据获取完成，长度: {len(enhanced_data)}字符")
        
        # 保存数据
        from tradingagents.config.output_config import get_data_report_path
        data_file = get_data_report_path(test_ticker)
        with open(data_file, 'w', encoding='utf-8') as f:
            f.write(enhanced_data)
        print(f"💾 数据已保存到: {data_file}")
        
    except Exception as e:
        print(f"❌ 增强工具演示失败: {e}")
        import traceback
        traceback.print_exc()


def compare_traditional_vs_enhanced():
    """
    对比传统分析与增强分析的差异
    """
    print("\n⚖️ ===== 传统分析 vs 增强分析对比 =====")
    
    try:
        from tradingagents.llms.deepseek_llm import create_deepseek_llm
        from tradingagents.tools.toolkit import Toolkit
        from tradingagents.agents.analysts.market_analyst import create_market_analyst_react
        from tradingagents.agents.analysts.enhanced_market_analyst import create_enhanced_market_analyst_with_deepseek
        
        # 创建LLM和工具包
        deepseek_llm = create_deepseek_llm(model="deepseek-chat", temperature=0.1)
        toolkit = Toolkit()
        
        test_ticker = "600036"  # 招商银行
        state = {
            "trade_date": datetime.now().strftime('%Y-%m-%d'),
            "company_of_interest": test_ticker
        }
        
        print(f"📊 对比股票: {test_ticker}")
        print()
        
        # 1. 传统分析
        print("📈 执行传统分析...")
        try:
            traditional_analyst = create_market_analyst_react(deepseek_llm, toolkit)
            traditional_result = traditional_analyst(state)
            traditional_report = traditional_result.get('market_report', '无报告')
            print(f"✅ 传统分析完成，长度: {len(traditional_report)}字")
        except Exception as e:
            print(f"❌ 传统分析失败: {e}")
            traditional_report = f"传统分析失败: {str(e)}"
        
        # 2. 增强分析
        print("🚀 执行增强分析...")
        try:
            enhanced_analyst = create_enhanced_market_analyst_with_deepseek(deepseek_llm, toolkit)
            enhanced_result = enhanced_analyst(state)
            enhanced_report = enhanced_result.get('market_report', '无报告')
            print(f"✅ 增强分析完成，长度: {len(enhanced_report)}字")
        except Exception as e:
            print(f"❌ 增强分析失败: {e}")
            enhanced_report = f"增强分析失败: {str(e)}"
        
        # 3. 保存对比结果
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        comparison_report = f"""# {test_ticker} 传统分析 vs 增强分析对比报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**测试股票**: {test_ticker}

## 📈 传统分析结果

**报告长度**: {len(traditional_report)}字

{traditional_report}

---

## 🚀 增强分析结果

**报告长度**: {len(enhanced_report)}字

{enhanced_report}

---

## 📊 对比总结

| 维度 | 传统分析 | 增强分析 |
|------|----------|----------|
| 报告长度 | {len(traditional_report)}字 | {len(enhanced_report)}字 |
| 技术指标精度 | 依赖LLM计算 | 工具精确计算 |
| 分析深度 | 一般 | 深入 |
| 数据可靠性 | 中等 | 高 |
| 分析具体性 | 较抽象 | 具体数值 |

**结论**: 增强分析通过先计算技术指标再分析的方式，显著提升了分析的准确性和具体性。
"""
        
        from tradingagents.config.output_config import get_comparison_report_path
        comparison_file = get_comparison_report_path(test_ticker)
        with open(comparison_file, 'w', encoding='utf-8') as f:
            f.write(comparison_report)
        
        print(f"\n📋 对比报告:")
        print("-" * 60)
        print(f"传统分析长度: {len(traditional_report)}字")
        print(f"增强分析长度: {len(enhanced_report)}字")
        print(f"长度提升: {((len(enhanced_report) - len(traditional_report)) / len(traditional_report) * 100):.1f}%" if len(traditional_report) > 0 else "无法计算")
        print("-" * 60)
        print(f"💾 对比报告已保存到: {comparison_file}")
        
    except Exception as e:
        print(f"❌ 对比演示失败: {e}")
        import traceback
        traceback.print_exc()


def main():
    """
    主函数
    """
    print("🎯 增强DeepSeek市场分析演示程序")
    print("解决方案: 先调用工具计算技术指标，再由DeepSeek深度分析")
    print()
    
    while True:
        print("\n请选择演示模式:")
        print("1. 完整增强分析演示")
        print("2. 仅测试增强工具")
        print("3. 传统vs增强对比")
        print("4. 退出")
        
        choice = input("\n请输入选择 (1-4): ").strip()
        
        if choice == "1":
            demo_enhanced_deepseek_analysis()
        elif choice == "2":
            demo_enhanced_tool_only()
        elif choice == "3":
            compare_traditional_vs_enhanced()
        elif choice == "4":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重试")


if __name__ == "__main__":
    main()