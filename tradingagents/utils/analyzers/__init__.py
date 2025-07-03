#!/usr/bin/env python3
"""
增强分析器模块
包含各种专业的增强分析器
"""

# 导入各种增强分析器
try:
    from .enhanced_technical_analysis import EnhancedTechnicalAnalyzer
except ImportError:
    EnhancedTechnicalAnalyzer = None

try:
    from .enhanced_fundamentals_analysis import EnhancedFundamentalsAnalyzer
except ImportError:
    EnhancedFundamentalsAnalyzer = None

try:
    from .enhanced_sentiment_analysis import EnhancedSentimentAnalyzer
except ImportError:
    EnhancedSentimentAnalyzer = None

try:
    from .enhanced_risk_analysis import EnhancedRiskAnalyzer
except ImportError:
    EnhancedRiskAnalyzer = None

# 导出所有可用的分析器
__all__ = []

if EnhancedTechnicalAnalyzer:
    __all__.append('EnhancedTechnicalAnalyzer')

if EnhancedFundamentalsAnalyzer:
    __all__.append('EnhancedFundamentalsAnalyzer')

if EnhancedSentimentAnalyzer:
    __all__.append('EnhancedSentimentAnalyzer')

if EnhancedRiskAnalyzer:
    __all__.append('EnhancedRiskAnalyzer')

# 分析器类型映射
ANALYZER_TYPES = {
    'technical': EnhancedTechnicalAnalyzer,
    'fundamentals': EnhancedFundamentalsAnalyzer,
    'sentiment': EnhancedSentimentAnalyzer,
    'risk': EnhancedRiskAnalyzer,
}

# 过滤掉None值
ANALYZER_TYPES = {k: v for k, v in ANALYZER_TYPES.items() if v is not None}


def get_available_analyzers():
    """获取所有可用的分析器类型"""
    return list(ANALYZER_TYPES.keys())


def create_analyzer(analyzer_type: str, **kwargs):
    """通用分析器创建函数"""
    if analyzer_type not in ANALYZER_TYPES:
        available = ', '.join(get_available_analyzers())
        raise ValueError(f"未知的分析器类型: {analyzer_type}。可用类型: {available}")
    
    return ANALYZER_TYPES[analyzer_type](**kwargs)


# 版本信息
__version__ = '1.0.0'