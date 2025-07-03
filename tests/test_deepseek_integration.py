#!/usr/bin/env python3
"""
DeepSeek集成测试脚本
验证DeepSeek LLM适配器的功能
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tradingagents.llm_adapters.deepseek_adapter import DeepSeekLLM, create_deepseek_llm
from tradingagents.config.config_manager import ConfigManager
from langchain_core.messages import HumanMessage, SystemMessage


def test_deepseek_adapter():
    """
    测试DeepSeek适配器基本功能
    """
    print("🧪 开始测试DeepSeek适配器...")
    
    # 检查API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ 未找到DEEPSEEK_API_KEY环境变量")
        print("请设置环境变量: set DEEPSEEK_API_KEY=your_api_key")
        return False
    
    print(f"✅ 找到API密钥: {api_key[:10]}...")
    
    try:
        # 创建DeepSeek LLM实例
        llm = create_deepseek_llm(
            model_name="deepseek-chat",
            api_key=api_key,
            max_tokens=100,
            temperature=0.7
        )
        
        print(f"✅ 成功创建DeepSeek LLM实例: {llm.model_name}")
        
        # 测试API密钥验证
        print("🔑 验证API密钥...")
        is_valid = llm.validate_api_key()
        if is_valid:
            print("✅ API密钥验证成功")
        else:
            print("❌ API密钥验证失败")
            return False
        
        # 测试基本对话
        print("💬 测试基本对话...")
        response = llm._call("你好，请简单介绍一下你自己。")
        print(f"🤖 DeepSeek回复: {response[:100]}...")
        
        # 测试LangChain消息格式
        print("📨 测试LangChain消息格式...")
        messages = [
            SystemMessage(content="你是一个专业的金融分析师。"),
            HumanMessage(content="请简要分析一下当前股市的趋势。")
        ]
        
        response = llm.chat_with_messages(messages)
        print(f"📈 金融分析回复: {response[:100]}...")
        
        # 测试token计数
        print("🔢 测试token计数...")
        test_text = "这是一个测试文本，用于计算token数量。"
        token_count = llm.get_token_count(test_text)
        print(f"📊 文本'{test_text}'的token数量: {token_count}")
        
        print("✅ DeepSeek适配器测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ DeepSeek适配器测试失败: {e}")
        return False


def test_config_integration():
    """
    测试配置管理器集成
    """
    print("\n🔧 测试配置管理器集成...")
    
    try:
        config_manager = ConfigManager()
        
        # 加载模型配置
        models = config_manager.load_models()
        deepseek_models = [m for m in models if m.provider == "deepseek"]
        
        if deepseek_models:
            print(f"✅ 找到{len(deepseek_models)}个DeepSeek模型配置:")
            for model in deepseek_models:
                print(f"   - {model.model_name} (启用: {model.enabled})")
        else:
            print("❌ 未找到DeepSeek模型配置")
            return False
        
        # 加载定价配置
        pricing = config_manager.load_pricing()
        deepseek_pricing = [p for p in pricing if p.provider == "deepseek"]
        
        if deepseek_pricing:
            print(f"✅ 找到{len(deepseek_pricing)}个DeepSeek定价配置:")
            for price in deepseek_pricing:
                print(f"   - {price.model_name}: 输入{price.input_price_per_1k} {price.currency}/1k, 输出{price.output_price_per_1k} {price.currency}/1k")
        else:
            print("❌ 未找到DeepSeek定价配置")
            return False
        
        print("✅ 配置管理器集成测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 配置管理器集成测试失败: {e}")
        return False


def test_trading_graph_integration():
    """
    测试TradingGraph集成（需要完整配置）
    """
    print("\n🎯 测试TradingGraph集成...")
    
    try:
        # 创建测试配置
        test_config = {
            "llm_provider": "deepseek",
            "deep_think_llm": "deepseek-chat",
            "quick_think_llm": "deepseek-chat",
            "project_dir": str(project_root),
            "memory_enabled": False,  # 简化测试
        }
        
        # 检查API密钥
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            print("⚠️  跳过TradingGraph集成测试（缺少API密钥）")
            return True
        
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        
        # 创建TradingGraph实例
        graph = TradingAgentsGraph(
            selected_analysts=["market"],  # 只选择一个分析师简化测试
            debug=True,
            config=test_config
        )
        
        print("✅ 成功创建TradingGraph实例")
        print(f"📊 深度思考LLM: {type(graph.deep_thinking_llm).__name__}")
        print(f"⚡ 快速思考LLM: {type(graph.quick_thinking_llm).__name__}")
        
        print("✅ TradingGraph集成测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ TradingGraph集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """
    主测试函数
    """
    print("🚀 DeepSeek集成测试开始")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        ("DeepSeek适配器", test_deepseek_adapter),
        ("配置管理器集成", test_config_integration),
        ("TradingGraph集成", test_trading_graph_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 运行测试: {test_name}")
        print("-" * 30)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            results.append((test_name, False))
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总计: {passed}/{len(results)} 个测试通过")
    
    if passed == len(results):
        print("🎉 所有测试通过！DeepSeek集成成功！")
    else:
        print("⚠️  部分测试失败，请检查配置和API密钥")
    
    return passed == len(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)