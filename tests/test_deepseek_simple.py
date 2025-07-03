#!/usr/bin/env python3
"""
简化的DeepSeek测试脚本
验证calculate_cost方法修复
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tradingagents.config.config_manager import ConfigManager
from tradingagents.llm_adapters.deepseek_adapter import create_deepseek_llm

def test_calculate_cost_fix():
    """测试calculate_cost方法修复"""
    print("🧪 测试ConfigManager.calculate_cost方法")
    
    try:
        config_manager = ConfigManager()
        
        # 测试calculate_cost方法
        cost = config_manager.calculate_cost(
            provider="deepseek",
            model_name="deepseek-chat",
            input_tokens=1000,
            output_tokens=500
        )
        
        print(f"✅ calculate_cost方法调用成功")
        print(f"💰 计算成本: {cost:.6f} CNY")
        print(f"📊 输入tokens: 1000, 输出tokens: 500")
        
        return True
        
    except Exception as e:
        print(f"❌ calculate_cost方法测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_deepseek_basic():
    """测试DeepSeek基本功能"""
    print("\n🤖 测试DeepSeek基本功能")
    
    # 检查API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("⚠️  未设置DEEPSEEK_API_KEY环境变量")
        return False
    
    print(f"✅ API密钥已配置 (前缀: {api_key[:10]}...)")
    
    try:
        # 创建DeepSeek LLM
        deepseek_llm = create_deepseek_llm(
            model_name="deepseek-chat",
            temperature=0.1,
            max_tokens=100
        )
        
        print("✅ DeepSeek LLM创建成功")
        
        # 简单测试
        response = deepseek_llm.invoke("请用一句话介绍苹果公司。")
        print(f"📝 DeepSeek响应: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ DeepSeek测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 DeepSeek简化测试套件")
    print("=" * 40)
    
    # 测试1: calculate_cost方法修复
    success1 = test_calculate_cost_fix()
    
    # 测试2: DeepSeek基本功能
    success2 = test_deepseek_basic()
    
    # 总结
    print("\n📊 测试结果:")
    print(f"   calculate_cost修复: {'✅ 通过' if success1 else '❌ 失败'}")
    print(f"   DeepSeek基本功能: {'✅ 通过' if success2 else '❌ 失败'}")
    
    if success1 and success2:
        print("\n🎉 所有测试通过！DeepSeek集成正常工作！")
    elif success1:
        print("\n✅ calculate_cost方法修复成功！")
    else:
        print("\n❌ 测试失败，请检查配置")