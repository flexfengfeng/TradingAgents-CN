# DeepSeek 集成指南

本文档介绍如何在 TradingAgents 中集成和使用 DeepSeek AI 模型。

## 概述

DeepSeek 是一个强大的大语言模型，特别擅长推理和代码生成。本集成为 TradingAgents 提供了 DeepSeek API 的完整支持。

## 功能特性

- ✅ **完整的 LangChain 兼容性**: 支持标准的 LangChain 接口
- ✅ **多模型支持**: 支持 deepseek-chat 和 deepseek-coder
- ✅ **成本追踪**: 内置使用量和成本监控
- ✅ **配置管理**: 集成到统一的配置系统
- ✅ **错误处理**: 完善的异常处理和日志记录
- ⚠️ **工具调用限制**: DeepSeek 暂不支持工具调用功能

## 快速开始

### 1. 获取 API 密钥

1. 访问 [DeepSeek 官网](https://www.deepseek.com/)
2. 注册账户并获取 API 密钥
3. 设置环境变量：

```bash
# Windows
set DEEPSEEK_API_KEY=your_api_key_here

# Linux/Mac
export DEEPSEEK_API_KEY=your_api_key_here
```

### 2. 基本使用

```python
from tradingagents.llm_adapters.deepseek_adapter import create_deepseek_llm

# 创建 DeepSeek LLM 实例
llm = create_deepseek_llm(
    model_name="deepseek-chat",
    max_tokens=4000,
    temperature=0.7
)

# 基本对话
response = llm._call("请分析一下当前的股市趋势")
print(response)
```

### 3. 在 TradingAgents 中使用

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph

# 配置 DeepSeek
config = {
    "llm_provider": "deepseek",
    "deep_think_llm": "deepseek-chat",
    "quick_think_llm": "deepseek-chat",
    "project_dir": "/path/to/project"
}

# 创建交易图
graph = TradingAgentsGraph(
    selected_analysts=["market", "fundamentals", "news"],
    config=config
)
```

## 配置选项

### 模型配置

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `model_name` | str | "deepseek-chat" | 模型名称 |
| `api_key` | str | "" | API 密钥 |
| `base_url` | str | "https://api.deepseek.com" | API 基础 URL |
| `max_tokens` | int | 4000 | 最大 token 数 |
| `temperature` | float | 0.7 | 温度参数 |
| `top_p` | float | 0.95 | Top-p 参数 |
| `stream` | bool | False | 是否启用流式输出 |

### 支持的模型

| 模型名称 | 描述 | 适用场景 |
|----------|------|----------|
| `deepseek-chat` | 通用对话模型 | 股票分析、市场解读 |
| `deepseek-coder` | 代码专用模型 | 策略编写、数据处理 |

## 定价信息

| 模型 | 输入价格 | 输出价格 | 货币 |
|------|----------|----------|------|
| deepseek-chat | ¥0.001/1k tokens | ¥0.002/1k tokens | CNY |
| deepseek-coder | ¥0.001/1k tokens | ¥0.002/1k tokens | CNY |

## 高级用法

### 1. 使用 LangChain 消息格式

```python
from langchain_core.messages import SystemMessage, HumanMessage

messages = [
    SystemMessage(content="你是一个专业的金融分析师"),
    HumanMessage(content="请分析苹果公司的投资价值")
]

response = llm.chat_with_messages(messages)
print(response)
```

### 2. 成本追踪

```python
from tradingagents.config.config_manager import ConfigManager, TokenTracker

config_manager = ConfigManager()
token_tracker = TokenTracker(config_manager)

# 追踪使用量
token_tracker.track_usage(
    provider="deepseek",
    model_name="deepseek-chat",
    input_tokens=100,
    output_tokens=200,
    session_id="analysis_001"
)

# 查看成本统计
stats = config_manager.get_usage_statistics(days=30)
print(f"本月成本: {stats['total_cost']} {stats['currency']}")
```

### 3. 配置管理

```python
from tradingagents.config.config_manager import ConfigManager, ModelConfig

config_manager = ConfigManager()

# 添加自定义模型配置
custom_model = ModelConfig(
    provider="deepseek",
    model_name="deepseek-chat",
    api_key="your_api_key",
    max_tokens=8000,
    temperature=0.5,
    enabled=True
)

models = config_manager.load_models()
models.append(custom_model)
config_manager.save_models(models)
```

## 测试和验证

### 运行集成测试

```bash
# 运行完整测试套件
python test_deepseek_integration.py

# 运行配置示例
python examples/deepseek_config_example.py
```

### 验证 API 连接

```python
from tradingagents.llm_adapters.deepseek_adapter import DeepSeekLLM

llm = DeepSeekLLM()
is_valid = llm.validate_api_key()
print(f"API 密钥有效: {is_valid}")
```

## 限制和注意事项

### 功能限制

1. **工具调用**: DeepSeek 暂不支持工具调用功能
   - 影响：部分 ReAct Agent 功能受限
   - 解决方案：使用基础 LLM 进行文本生成和分析

2. **流式输出**: 当前版本不支持流式输出
   - 影响：无法实时显示生成过程
   - 计划：后续版本将添加支持

### 性能建议

1. **Token 管理**: 合理设置 `max_tokens` 以控制成本
2. **温度参数**: 金融分析建议使用较低温度（0.1-0.3）
3. **批量处理**: 对于大量请求，考虑批量处理以提高效率

### 错误处理

常见错误及解决方案：

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| API 密钥无效 | 密钥错误或过期 | 检查并更新 `DEEPSEEK_API_KEY` |
| 请求超时 | 网络问题 | 检查网络连接，增加超时时间 |
| Token 超限 | 输入过长 | 减少输入长度或增加 `max_tokens` |
| 模型不存在 | 模型名称错误 | 使用正确的模型名称 |

## 最佳实践

### 1. 配置管理

```python
# 推荐的配置结构
deepseek_config = {
    "llm_provider": "deepseek",
    "models": {
        "analysis": "deepseek-chat",
        "coding": "deepseek-coder"
    },
    "parameters": {
        "temperature": 0.2,  # 金融分析用较低温度
        "max_tokens": 4000,
        "top_p": 0.9
    }
}
```

### 2. 成本控制

```python
# 设置成本警告
settings = {
    "cost_alert_threshold": 100.0,  # 100元警告
    "enable_cost_tracking": True,
    "currency_preference": "CNY"
}
```

### 3. 错误重试

```python
import time
from functools import wraps

def retry_on_error(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(delay * (2 ** attempt))
            return None
        return wrapper
    return decorator

@retry_on_error(max_retries=3)
def safe_llm_call(llm, prompt):
    return llm._call(prompt)
```

## 故障排除

### 常见问题

**Q: 为什么 DeepSeek 不支持工具调用？**
A: DeepSeek API 当前版本不支持 Function Calling。我们正在关注官方更新，一旦支持将立即集成。

**Q: 如何优化 DeepSeek 的响应速度？**
A: 
1. 减少 `max_tokens` 设置
2. 使用更简洁的提示词
3. 考虑使用缓存机制

**Q: DeepSeek 适合哪些分析任务？**
A: 
- ✅ 市场趋势分析
- ✅ 财务报表解读
- ✅ 新闻情感分析
- ✅ 投资建议生成
- ❌ 实时数据查询（需要工具调用）

### 调试技巧

1. **启用调试日志**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **检查 API 响应**:
```python
response = llm._make_request(messages)
print(f"API 响应: {response}")
```

3. **验证配置**:
```python
config_manager = ConfigManager()
status = config_manager.get_env_config_status()
print(f"配置状态: {status}")
```

## 更新日志

### v1.0.0 (2024-01-XX)
- ✅ 初始版本发布
- ✅ 支持 deepseek-chat 和 deepseek-coder
- ✅ 集成配置管理系统
- ✅ 添加成本追踪功能
- ✅ 完整的测试套件

### 计划功能
- 🔄 流式输出支持
- 🔄 工具调用支持（等待官方 API 更新）
- 🔄 批量处理优化
- 🔄 缓存机制

## 支持和反馈

如果您在使用 DeepSeek 集成时遇到问题，请：

1. 查看本文档的故障排除部分
2. 运行测试脚本进行诊断
3. 在项目 GitHub 上提交 Issue
4. 联系技术支持团队

---

**注意**: DeepSeek 集成仍在持续优化中，建议定期更新到最新版本以获得最佳体验。