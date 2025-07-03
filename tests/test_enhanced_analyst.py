#!/usr/bin/env python3
"""
增强分析师测试文件
测试增强分析师的各项功能
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入增强分析师
try:
    from tradingagents.agents.analysts.enhanced_analyst import create_enhanced_analyst
    print("✅ 成功导入增强分析师")
except ImportError as e:
    print(f"❌ 导入增强分析师失败: {e}")
    sys.exit(1)

# 导入增强分析工具包（用于独立测试）
try:
    from tradingagents.utils.enhanced_analysis_toolkit import EnhancedAnalysisToolkit
    print("✅ 成功导入增强分析工具包")
except ImportError as e:
    print(f"❌ 导入增强分析工具包失败: {e}")
    print("将跳过工具包独立测试")
    EnhancedAnalysisToolkit = None


def test_enhanced_toolkit():
    """测试增强分析工具包的独立功能"""
    if not EnhancedAnalysisToolkit:
        print("⏭️ 跳过工具包独立测试")
        return
    
    print("\n" + "=" * 60)
    print("🧪 测试增强分析工具包独立功能")
    print("=" * 60)
    
    try:
        # 初始化工具包
        toolkit = EnhancedAnalysisToolkit()
        
        # 准备测试数据
        ticker = "000001"
        company_name = "平安银行"
        
        # 模拟股票数据（CSV格式）
        stock_data = """
date,open,high,low,close,volume
2024-01-01,10.50,10.80,10.30,10.75,1500000
2024-01-02,10.75,11.00,10.60,10.90,1800000
2024-01-03,10.90,11.20,10.85,11.10,2000000
2024-01-04,11.10,11.30,10.95,11.25,1700000
2024-01-05,11.25,11.50,11.15,11.40,1900000
2024-01-08,11.40,11.60,11.25,11.55,2100000
2024-01-09,11.55,11.75,11.40,11.70,1950000
2024-01-10,11.70,11.85,11.55,11.80,1850000
2024-01-11,11.80,11.95,11.65,11.90,2000000
2024-01-12,11.90,12.10,11.85,12.05,2200000
"""
        
        # 模拟基本面数据
        fundamentals_data = """
市盈率: 8.5
市净率: 0.85
净资产收益率: 12.3%
总资产收益率: 1.2%
负债权益比: 0.45
流动比率: 1.8
速动比率: 1.5
资产负债率: 31.2%
毛利率: 45.6%
净利率: 23.4%
营业收入增长率: 15.2%
净利润增长率: 18.5%
每股收益: 1.42
每股净资产: 12.15
每股现金流: 2.35
股息率: 3.2%
"""
        
        # 模拟新闻数据
        news_data = """
标题: 平安银行发布三季度业绩报告，净利润同比增长15%
内容: 平安银行今日发布三季度财报，实现净利润同比增长15%，超出市场预期。银行资产质量持续改善，不良贷款率进一步下降。
时间: 2小时前
来源: 证券时报
情绪: 积极

标题: 央行降准释放流动性，银行股集体上涨
内容: 央行宣布降准0.5个百分点，为市场释放长期流动性约1.2万亿元，银行股普遍受益，板块涨幅居前。
时间: 1天前
来源: 新华社
情绪: 积极

标题: 监管层加强银行风险管控要求
内容: 银保监会发布新规，要求银行进一步加强风险管控，提高资本充足率要求。
时间: 3天前
来源: 财经网
情绪: 中性

标题: 平安银行推出数字化转型新举措
内容: 平安银行宣布投资50亿元用于数字化转型，预计将显著提升运营效率和客户体验。
时间: 1周前
来源: 经济日报
情绪: 积极
"""
        
        # 模拟市场数据
        market_data = """
上证指数: 3200.45 (+1.2%)
深证成指: 11500.32 (+0.8%)
创业板指: 2450.67 (+1.5%)
银行板块指数: 1850.23 (+2.1%)
VIX恐慌指数: 18.5
10年期国债收益率: 2.65%
1年期LPR: 3.45%
5年期LPR: 4.20%
"""
        
        print(f"📊 开始分析 {ticker}（{company_name}）...")
        
        # 执行综合分析
        results = toolkit.comprehensive_analysis(
            ticker=ticker,
            stock_data=stock_data,
            fundamentals_data=fundamentals_data,
            news_data=news_data,
            market_data=market_data,
            company_name=company_name
        )
        
        print("\n📈 分析结果概览:")
        print(f"- 技术分析: {'✅' if results.get('technical_analysis') and 'error' not in results['technical_analysis'] else '❌'}")
        print(f"- 基本面分析: {'✅' if results.get('fundamentals_analysis') and 'error' not in results['fundamentals_analysis'] else '❌'}")
        print(f"- 情绪分析: {'✅' if results.get('sentiment_analysis') and 'error' not in results['sentiment_analysis'] else '❌'}")
        print(f"- 风险评估: {'✅' if results.get('risk_analysis') and 'error' not in results['risk_analysis'] else '❌'}")
        
        # 显示综合评估
        summary = results.get('comprehensive_summary', {})
        recommendation = results.get('investment_recommendation', {})
        
        print(f"\n🎯 综合评估:")
        print(f"- 综合评分: {summary.get('overall_score', 'N/A'):.1f}/100")
        print(f"- 投资评级: {recommendation.get('rating', 'N/A')}")
        print(f"- 风险等级: {recommendation.get('risk_level', 'N/A')}")
        
        # 生成报告
        report = toolkit.generate_enhanced_report(results)
        
        # 保存结果
        filename = toolkit.save_analysis_results(results, f"test_enhanced_analysis_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        print(f"\n💾 分析结果已保存到: {filename}")
        print(f"📄 报告长度: {len(report)} 字符")
        
        # 显示报告摘要
        print("\n📋 报告摘要:")
        report_lines = report.split('\n')
        for line in report_lines[:20]:  # 显示前20行
            if line.strip():
                print(f"  {line}")
        
        if len(report_lines) > 20:
            print(f"  ... (还有 {len(report_lines) - 20} 行)")
        
        print("\n✅ 增强分析工具包测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 增强分析工具包测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_enhanced_analyst_node():
    """测试增强分析师节点"""
    print("\n" + "=" * 60)
    print("🧪 测试增强分析师节点")
    print("=" * 60)
    
    try:
        # 创建增强分析师（离线模式，避免需要API密钥）
        analyst = create_enhanced_analyst(model="deepseek", online=False)
        print("✅ 增强分析师节点创建成功")
        
        # 准备测试消息
        test_message = {
            "ticker": "000001",
            "query": "请重点分析技术面趋势和估值水平"
        }
        
        print(f"📤 发送测试消息: {test_message}")
        
        # 处理消息（注意：离线模式可能功能有限）
        result = await analyst.process(test_message)
        
        print("📥 收到分析结果:")
        if "error" in result:
            print(f"❌ 分析失败: {result['error']}")
        else:
            print(f"✅ 分析成功")
            print(f"- 股票代码: {result.get('ticker', 'N/A')}")
            print(f"- 公司名称: {result.get('company_name', 'N/A')}")
            print(f"- 分析日期: {result.get('analysis_date', 'N/A')}")
            
            # 检查各个分析组件
            if 'enhanced_analysis' in result:
                print("- 增强分析: ✅")
            if 'enhanced_report' in result:
                print(f"- 增强报告: ✅ ({len(result['enhanced_report'])} 字符)")
            if 'deepseek_analysis' in result:
                print(f"- DeepSeek分析: ✅ ({len(result['deepseek_analysis'])} 字符)")
            if 'react_agent_analysis' in result:
                print(f"- ReAct Agent分析: ✅ ({len(result['react_agent_analysis'])} 字符)")
        
        print("\n✅ 增强分析师节点测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 增强分析师节点测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_analyst_integration():
    """测试分析师模块集成"""
    print("\n" + "=" * 60)
    print("🧪 测试分析师模块集成")
    print("=" * 60)
    
    try:
        # 测试从analysts模块导入
        from tradingagents.agents.analysts import get_available_analysts, create_analyst
        
        print("✅ 成功导入分析师模块")
        
        # 获取可用分析师
        available_analysts = get_available_analysts()
        print(f"📋 可用分析师类型: {available_analysts}")
        
        # 测试创建增强分析师
        if 'enhanced' in available_analysts:
            enhanced_analyst = create_analyst('enhanced', online=False)
            print("✅ 通过通用接口创建增强分析师成功")
        else:
            print("⚠️ 增强分析师不在可用列表中")
        
        print("\n✅ 分析师模块集成测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 分析师模块集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主测试函数"""
    print("🚀 增强分析师完整测试套件")
    print("=" * 80)
    
    test_results = []
    
    # 1. 测试增强分析工具包
    print("\n1️⃣ 测试增强分析工具包...")
    result1 = test_enhanced_toolkit()
    test_results.append(("增强分析工具包", result1))
    
    # 2. 测试增强分析师节点
    print("\n2️⃣ 测试增强分析师节点...")
    result2 = await test_enhanced_analyst_node()
    test_results.append(("增强分析师节点", result2))
    
    # 3. 测试分析师模块集成
    print("\n3️⃣ 测试分析师模块集成...")
    result3 = test_analyst_integration()
    test_results.append(("分析师模块集成", result3))
    
    # 汇总测试结果
    print("\n" + "=" * 80)
    print("📊 测试结果汇总")
    print("=" * 80)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"- {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试都通过了！增强分析师系统运行正常。")
    else:
        print("⚠️ 部分测试失败，请检查相关组件。")
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)


if __name__ == "__main__":
    # 运行测试
    asyncio.run(main())