#!/usr/bin/env python3
"""
DeepSeek配置示例
演示如何配置和使用DeepSeek LLM
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tradingagents.config.config_manager import ConfigManager, ModelConfig
from tradingagents.llm_adapters.deepseek_adapter import create_deepseek_llm
from tradingagents.graph.trading_graph import TradingAgentsGraph


def setup_deepseek_config():
    """
    设置DeepSeek配置
    """
    print("🔧 设置DeepSeek配置...")
    
    # 创建配置管理器
    config_manager = ConfigManager()
    
    # 获取当前模型配置
    models = config_manager.load_models()
    
    # 启用DeepSeek模型（如果有API密钥）
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if api_key:
        for model in models:
            if model.provider == "deepseek":
                model.enabled = True
                model.api_key = api_key
                print(f"✅ 启用DeepSeek模型: {model.model_name}")
    else:
        print("⚠️  未找到DEEPSEEK_API_KEY环境变量")
        print("请设置环境变量: set DEEPSEEK_API_KEY=your_api_key")
    
    # 保存配置
    config_manager.save_models(models)
    
    # 更新默认设置
    settings = config_manager.load_settings()
    if api_key:
        settings["default_provider"] = "deepseek"
        settings["default_model"] = "deepseek-chat"
        config_manager.save_settings(settings)
        print("✅ 设置DeepSeek为默认提供商")
    
    return config_manager


def create_deepseek_trading_config():
    """
    创建DeepSeek交易配置
    """
    print("📊 创建DeepSeek交易配置...")
    
    config = {
        # LLM配置
        "llm_provider": "deepseek",
        "deep_think_llm": "deepseek-chat",
        "quick_think_llm": "deepseek-chat",
        
        # 项目配置
        "project_dir": str(project_root),
        
        # 功能配置
        "memory_enabled": True,
        "enable_cost_tracking": True,
        
        # 数据源配置
        "data_sources": {
            "yahoo_finance": True,
            "china_stocks": True,
            "news": True,
            "social_media": False  # 可选
        },
        
        # 分析师配置
        "analysts": {
            "market": True,
            "fundamentals": True,
            "news": True,
            "china_market": True,  # 中国市场专用
            "social": False  # 可选
        },
        
        # 风险管理
        "risk_management": {
            "enabled": True,
            "max_position_size": 0.1,  # 最大仓位10%
            "stop_loss": 0.05,  # 止损5%
            "take_profit": 0.15  # 止盈15%
        },
        
        # DeepSeek特定配置
        "deepseek_config": {
            "base_url": "https://api.deepseek.com",
            "max_tokens": 4000,
            "temperature": 0.7,
            "top_p": 0.95,
            "stream": False
        }
    }
    
    return config


def test_deepseek_llm():
    """
    测试DeepSeek LLM基本功能
    """
    print("\n🧪 测试DeepSeek LLM...")
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ 需要DEEPSEEK_API_KEY环境变量")
        return False
    
    try:
        # 创建LLM实例
        llm = create_deepseek_llm(
            model_name="deepseek-chat",
            api_key=api_key,
            max_tokens=200,
            temperature=0.7
        )
        
        # 测试基本对话
        prompt = "请简要介绍DeepSeek AI的特点和优势。"
        response = llm._call(prompt)
        
        print(f"✅ DeepSeek回复: {response}")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def create_trading_graph_with_deepseek():
    """
    使用DeepSeek创建交易图
    """
    print("\n🎯 创建DeepSeek交易图...")
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ 需要DEEPSEEK_API_KEY环境变量")
        return None
    
    try:
        # 创建配置
        config = create_deepseek_trading_config()
        
        # 创建交易图
        graph = TradingAgentsGraph(
            selected_analysts=["market", "fundamentals", "news"],
            debug=True,
            config=config
        )
        
        print("✅ 成功创建DeepSeek交易图")
        print(f"📊 深度思考模型: {graph.deep_thinking_llm.model_name}")
        print(f"⚡ 快速思考模型: {graph.quick_thinking_llm.model_name}")
        
        return graph
        
    except Exception as e:
        print(f"❌ 创建交易图失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def demo_stock_analysis():
    """
    演示股票分析功能
    """
    print("\n📈 演示股票分析...")
    
    # 创建交易图
    graph = create_trading_graph_with_deepseek()
    if not graph:
        print("❌ 无法创建交易图，跳过演示")
        return
    
    try:
        # 示例：分析苹果股票
        ticker = "AAPL"
        print(f"🍎 分析股票: {ticker}")
        
        # 这里可以添加具体的分析逻辑
        # 由于完整的分析需要更多配置，这里只是演示框架
        print("✅ 交易图已准备就绪，可以进行股票分析")
        print("💡 提示: 使用graph.run()方法开始分析")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")


def show_usage_examples():
    """
    显示使用示例
    """
    print("\n📚 DeepSeek使用示例:")
    print("=" * 50)
    
    print("\n1. 设置环境变量:")
    print("   set DEEPSEEK_API_KEY=your_api_key_here")
    
    print("\n2. 基本使用:")
    print("   from tradingagents.llm_adapters.deepseek_adapter import create_deepseek_llm")
    print("   llm = create_deepseek_llm(model_name='deepseek-chat')")
    print("   response = llm._call('你好，DeepSeek!')")
    
    print("\n3. 配置交易系统:")
    print("   config = {")
    print("       'llm_provider': 'deepseek',")
    print("       'deep_think_llm': 'deepseek-chat',")
    print("       'quick_think_llm': 'deepseek-chat'")
    print("   }")
    print("   graph = TradingAgentsGraph(config=config)")
    
    print("\n4. 支持的模型:")
    print("   - deepseek-chat: 通用对话模型")
    print("   - deepseek-coder: 代码专用模型")
    
    print("\n5. 定价信息:")
    print("   - 输入: ¥0.001/1k tokens")
    print("   - 输出: ¥0.002/1k tokens")
    
    print("\n6. 注意事项:")
    print("   - DeepSeek暂不支持工具调用")
    print("   - 部分ReAct功能可能受限")
    print("   - 建议用于文本生成和分析任务")


def main():
    """
    主函数
    """
    print("🚀 DeepSeek配置示例")
    print("=" * 50)
    
    # 显示使用示例
    show_usage_examples()
    
    # 设置配置
    config_manager = setup_deepseek_config()
    
    # 测试LLM
    test_deepseek_llm()
    
    # 创建交易图
    create_trading_graph_with_deepseek()
    
    # 演示分析
    demo_stock_analysis()
    
    print("\n✅ DeepSeek配置示例完成！")
    print("💡 现在可以使用DeepSeek进行股票分析了")


if __name__ == "__main__":
    main()