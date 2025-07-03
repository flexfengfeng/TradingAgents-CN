# LLM Adapters for TradingAgents

# 尝试导入各个适配器，如果依赖缺失则跳过
__all__ = []

try:
    from .dashscope_adapter import ChatDashScope
    __all__.append("ChatDashScope")
except ImportError as e:
    print(f"Warning: DashScope adapter not available: {e}")

try:
    from .deepseek_adapter import DeepSeekLLM, create_deepseek_llm
    __all__.extend(["DeepSeekLLM", "create_deepseek_llm"])
except ImportError as e:
    print(f"Warning: DeepSeek adapter not available: {e}")
