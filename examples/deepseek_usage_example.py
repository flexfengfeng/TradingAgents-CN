#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek使用示例

本示例展示如何在TradingAgents中使用DeepSeek AI模型进行股票分析。

使用前请确保：
1. 已获取DeepSeek API密钥
2. 设置环境变量: set DEEPSEEK_API_KEY=your_api_key
3. 或在.env文件中添加: DEEPSEEK_API_KEY=your_api_key
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tradingagents.llm_adapters import DeepSeekLLM, create_deepseek_llm
from tradingagents.config.config_manager import ConfigManager
from tradingagents.graph.trading_graph import TradingAgentsGraph

def check_api_key():
    """检查API密钥是否已设置"""
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        print("❌ 未找到DEEPSEEK_API_KEY环境变量")
        print("请设置环境变量: set DEEPSEEK_API_KEY=your_api_key")
        print("或在.env文件中添加: DEEPSEEK_API_KEY=your_api_key")
        return False
    print(f"✅ 找到API密钥: {api_key[:8]}...")
    return True

def example_basic_usage():
    """基本使用示例"""
    print("\n🔧 基本使用示例")
    print("-" * 30)
    
    try:
        # 创建DeepSeek LLM实例
        llm = create_deepseek_llm(
            model_name="deepseek-chat",
            temperature=0.7,
            max_tokens=2000
        )
        
        print(f"✅ 成功创建DeepSeek LLM: {llm.model_name}")
        print(f"   - 温度: {llm.temperature}")
        print(f"   - 最大tokens: {llm.max_tokens}")
        print(f"   - API地址: {llm.base_url}")
        
        # 测试简单对话
        if check_api_key():
            print("\n💬 测试对话...")
            response = llm.invoke("你好，请简单介绍一下你自己。")
            print(f"🤖 DeepSeek回复: {response.content}")
        
    except Exception as e:
        print(f"❌ 基本使用测试失败: {e}")

def example_config_manager():
    """配置管理器示例"""
    print("\n🔧 配置管理器示例")
    print("-" * 30)
    
    try:
        # 创建配置管理器
        config_manager = ConfigManager()
        
        # 获取DeepSeek模型配置
        models = config_manager.load_models()
        deepseek_models = [m for m in models if m.provider == 'deepseek']
        
        print(f"✅ 找到{len(deepseek_models)}个DeepSeek模型:")
        for model in deepseek_models:
            print(f"   - {model.model_name} (启用: {model.enabled})")
        
        # 获取定价信息
        pricing = config_manager.load_pricing()
        deepseek_pricing = [p for p in pricing if p.provider == 'deepseek']
        
        print(f"\n💰 DeepSeek定价信息:")
        for price in deepseek_pricing:
            print(f"   - {price.model_name}: 输入{price.input_price_per_1k} {price.currency}/1k, 输出{price.output_price_per_1k} {price.currency}/1k")
        
        # 计算成本示例
        if deepseek_pricing:
            cost = config_manager.calculate_cost('deepseek', 'deepseek-chat', 1000, 500)
            print(f"\n📊 成本计算示例 (1000输入+500输出tokens): {cost:.4f} CNY")
        
    except Exception as e:
        print(f"❌ 配置管理器测试失败: {e}")

def example_trading_graph():
    """交易图示例"""
    print("\n🔧 交易图集成示例")
    print("-" * 30)
    
    if not check_api_key():
        print("⚠️  跳过交易图测试（缺少API密钥）")
        return
    
    try:
        # 创建交易配置
        config = {
            'llm_provider': 'deepseek',
            'llm_model': 'deepseek-chat',
            'enable_cost_tracking': True,
            'max_cost_threshold': 10.0
        }
        
        # 创建交易图
        graph = TradingAgentsGraph(config)
        print("✅ 成功创建TradingGraph with DeepSeek")
        print(f"   - 深度思考LLM: {graph.deep_thinking_llm.model_name}")
        print(f"   - 快速思考LLM: {graph.quick_thinking_llm.model_name}")
        print(f"   - React LLM: {graph.react_llm.model_name}")
        
        # 测试股票分析
        print("\n📈 测试股票分析...")
        analysis_request = {
            'stock_symbol': 'AAPL',
            'analysis_type': 'technical',
            'time_frame': '1d'
        }
        
        # 注意：这里只是演示结构，实际分析需要完整的数据流
        print(f"📊 分析请求: {analysis_request}")
        print("💡 提示: 完整的股票分析需要配置数据源和完整的工作流")
        
    except Exception as e:
        print(f"❌ 交易图测试失败: {e}")

def example_cost_tracking():
    """成本追踪示例"""
    print("\n🔧 成本追踪示例")
    print("-" * 30)
    
    try:
        from tradingagents.config.config_manager import token_tracker
        
        # 模拟使用记录
        token_tracker.track_usage(
            provider='deepseek',
            model_name='deepseek-chat',
            input_tokens=1000,
            output_tokens=500,
            session_id='demo_session',
            analysis_type='stock_analysis'
        )
        
        print("✅ 成功记录使用情况")
        
        # 获取统计信息
        stats = token_tracker.config_manager.get_usage_statistics(days=1)
        print(f"📊 使用统计: {stats}")
        
    except Exception as e:
        print(f"❌ 成本追踪测试失败: {e}")

def main():
    """主函数"""
    print("🚀 DeepSeek使用示例")
    print("=" * 50)
    
    # 运行各种示例
    example_basic_usage()
    example_config_manager()
    example_trading_graph()
    example_cost_tracking()
    
    print("\n" + "=" * 50)
    print("🎯 示例运行完成！")
    print("\n💡 使用提示:")
    print("   1. 设置DEEPSEEK_API_KEY环境变量以启用API调用")
    print("   2. 查看 deepseek_integration.md 获取详细文档")
    print("   3. 运行 test_deepseek_integration.py 进行完整测试")
    print("   4. 参考 deepseek_config_example.py 了解高级配置")

if __name__ == "__main__":
    main()