#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的DeepSeek集成测试

避免复杂依赖，直接测试DeepSeek适配器的核心功能
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_deepseek_adapter():
    """测试DeepSeek适配器"""
    print("🧪 测试DeepSeek适配器")
    print("-" * 30)
    
    try:
        # 直接导入DeepSeek适配器
        from tradingagents.llm_adapters.deepseek_adapter import DeepSeekLLM, create_deepseek_llm
        
        # 创建DeepSeek实例
        llm = DeepSeekLLM(
            model_name="deepseek-chat",
            api_key="test_key",
            temperature=0.7,
            max_tokens=2000
        )
        
        print(f"✅ 成功创建DeepSeek LLM实例")
        print(f"   - 模型: {llm.model_name}")
        print(f"   - 温度: {llm.temperature}")
        print(f"   - 最大tokens: {llm.max_tokens}")
        print(f"   - API地址: {llm.base_url}")
        print(f"   - 流式输出: {llm.enable_stream}")
        
        # 测试消息转换
        from langchain_core.messages import HumanMessage, SystemMessage
        
        messages = [
            SystemMessage(content="你是一个专业的股票分析师。"),
            HumanMessage(content="请分析一下苹果公司的股票。")
        ]
        
        deepseek_messages = llm.convert_langchain_messages(messages)
        print(f"\n✅ 消息转换测试通过")
        print(f"   - 原始消息数: {len(messages)}")
        print(f"   - 转换后消息数: {len(deepseek_messages)}")
        print(f"   - 转换后格式: {[msg['role'] for msg in deepseek_messages]}")
        
        # 测试token计数
        text = "这是一个测试文本，用于验证token计数功能。"
        token_count = llm.get_num_tokens(text)
        print(f"\n✅ Token计数测试通过")
        print(f"   - 测试文本: {text}")
        print(f"   - Token数量: {token_count}")
        
        # 测试create函数
        llm2 = create_deepseek_llm(model_name="deepseek-coder")
        print(f"\n✅ create_deepseek_llm函数测试通过")
        print(f"   - 模型: {llm2.model_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ DeepSeek适配器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_manager():
    """测试配置管理器"""
    print("\n🧪 测试配置管理器")
    print("-" * 30)
    
    try:
        from tradingagents.config.config_manager import ConfigManager
        
        # 创建配置管理器
        config_manager = ConfigManager()
        
        # 测试模型配置
        models = config_manager.load_models()
        deepseek_models = [m for m in models if m.provider == 'deepseek']
        
        print(f"✅ 模型配置测试通过")
        print(f"   - 总模型数: {len(models)}")
        print(f"   - DeepSeek模型数: {len(deepseek_models)}")
        
        for model in deepseek_models:
            print(f"   - {model.model_name}: {model.base_url}")
        
        # 测试定价配置
        pricing = config_manager.load_pricing()
        deepseek_pricing = [p for p in pricing if p.provider == 'deepseek']
        
        print(f"\n✅ 定价配置测试通过")
        print(f"   - DeepSeek定价配置数: {len(deepseek_pricing)}")
        
        for price in deepseek_pricing:
            print(f"   - {price.model_name}: {price.input_price_per_1k}/{price.output_price_per_1k} {price.currency}")
        
        # 测试成本计算
        if deepseek_pricing:
            cost = config_manager.calculate_cost('deepseek', 'deepseek-chat', 1000, 500)
            print(f"\n✅ 成本计算测试通过")
            print(f"   - 1000输入+500输出tokens成本: {cost:.4f} CNY")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置管理器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_import():
    """测试导入"""
    print("\n🧪 测试模块导入")
    print("-" * 30)
    
    try:
        # 测试从__init__.py导入
        from tradingagents.llm_adapters import DeepSeekLLM, create_deepseek_llm
        print("✅ 从llm_adapters.__init__导入成功")
        
        # 测试直接导入
        from tradingagents.llm_adapters.deepseek_adapter import DeepSeekLLM as DirectDeepSeekLLM
        print("✅ 直接从deepseek_adapter导入成功")
        
        # 验证是同一个类
        assert DeepSeekLLM is DirectDeepSeekLLM
        print("✅ 导入的类一致性验证通过")
        
        return True
        
    except Exception as e:
        print(f"❌ 导入测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🚀 简单DeepSeek集成测试")
    print("=" * 50)
    
    results = []
    
    # 运行测试
    results.append(("模块导入", test_import()))
    results.append(("DeepSeek适配器", test_deepseek_adapter()))
    results.append(("配置管理器", test_config_manager()))
    
    # 汇总结果
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
        print("⚠️  部分测试失败，请检查错误信息")
    
    print("\n💡 下一步:")
    print("   1. 设置DEEPSEEK_API_KEY环境变量")
    print("   2. 运行完整的API调用测试")
    print("   3. 在TradingAgents中使用DeepSeek进行股票分析")

if __name__ == "__main__":
    main()