# 数据目录说明

本目录用于存储项目运行过程中生成的各种数据文件，包括报告、日志、缓存等。

## 📁 目录结构

```
data/
├── README.md           # 本文件
├── reports/            # 分析报告和生成的文档
│   ├── enhanced_data_*.md      # 增强数据报告
│   ├── *_enhanced_analysis_*.md # 增强分析报告
│   └── comparison_*.md         # 对比分析报告
├── logs/               # 日志文件
├── cache/              # 缓存数据
└── temp/               # 临时文件
```

## 📋 文件类型说明

### 📊 reports/ - 分析报告
- **enhanced_data_*.md**: 增强技术数据报告，包含精确计算的技术指标
- ***_enhanced_analysis_*.md**: DeepSeek增强分析报告，包含深度市场分析
- **comparison_*.md**: 传统分析与增强分析的对比报告
- **deepseek_enhanced_analysis_*.md**: DeepSeek专项增强分析报告

### 📝 logs/ - 日志文件
- 系统运行日志
- 错误日志
- 调试日志

### 💾 cache/ - 缓存数据
- API调用缓存
- 数据处理缓存
- 计算结果缓存

### 🗂️ temp/ - 临时文件
- 临时处理文件
- 中间计算结果

## 🔧 配置管理

项目使用 `tradingagents.config.output_config` 模块统一管理输出路径：

```python
from tradingagents.config.output_config import (
    get_analysis_report_path,
    get_data_report_path,
    get_comparison_report_path
)

# 获取分析报告路径
report_path = get_analysis_report_path("000001", "enhanced_analysis")

# 获取数据报告路径
data_path = get_data_report_path("000001")

# 获取对比报告路径
comparison_path = get_comparison_report_path("000001")
```

## 🧹 文件清理

### 自动清理
配置模块提供自动清理功能：

```python
from tradingagents.config.output_config import get_output_config

# 清理7天前的文件
get_output_config().cleanup_old_files(days=7)
```

### 手动清理
可以手动删除不需要的文件：

```bash
# 清理所有报告文件
rm -rf data/reports/*

# 清理临时文件
rm -rf data/temp/*

# 清理日志文件
rm -rf data/logs/*
```

## 📝 最佳实践

### ✅ 推荐做法
1. **使用配置模块**: 始终使用 `output_config` 模块获取文件路径
2. **分类存储**: 根据文件类型存储到对应的子目录
3. **定期清理**: 定期清理旧的临时文件和日志
4. **命名规范**: 使用有意义的文件名和时间戳

### ❌ 避免做法
1. **硬编码路径**: 不要在代码中硬编码文件路径
2. **根目录存储**: 不要将生成的文件直接放在项目根目录
3. **混乱命名**: 避免使用无意义的文件名
4. **无限累积**: 不要让临时文件无限累积

## 🔒 版本控制

本目录下的文件已通过 `.gitignore` 配置排除在版本控制之外：

```gitignore
# 生成的报告和数据文件
data/reports/
*.md
!README*.md
!docs/**/*.md
```

这确保了：
- 生成的报告文件不会被提交到代码仓库
- 保持代码仓库的整洁
- 避免敏感数据泄露

## 🚀 快速开始

1. **确保目录存在**:
   ```python
   from tradingagents.config.output_config import ensure_output_dirs
   ensure_output_dirs()
   ```

2. **生成报告**:
   ```python
   from tradingagents.config.output_config import get_analysis_report_path
   
   report_path = get_analysis_report_path("000001")
   with open(report_path, 'w', encoding='utf-8') as f:
       f.write("分析报告内容")
   ```

3. **清理旧文件**:
   ```python
   from tradingagents.config.output_config import get_output_config
   get_output_config().cleanup_old_files(days=7)
   ```

## 📞 支持

如果您在使用过程中遇到问题，请：
1. 查看项目文档
2. 检查配置是否正确
3. 提交 Issue 或联系开发团队