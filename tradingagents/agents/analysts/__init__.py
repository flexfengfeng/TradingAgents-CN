#!/usr/bin/env python3
"""
分析师模块
包含各种专业的股票分析师节点
"""

# 导入基础分析师
try:
    from .market_analyst import create_market_analyst
except ImportError:
    create_market_analyst = None

try:
    from .fundamentals_analyst import create_fundamentals_analyst
except ImportError:
    create_fundamentals_analyst = None

try:
    from .news_analyst import create_news_analyst
except ImportError:
    create_news_analyst = None

# 导入增强分析师
try:
    from .enhanced_market_analyst import create_enhanced_market_analyst
except ImportError:
    create_enhanced_market_analyst = None

try:
    from .enhanced_analyst import create_enhanced_analyst
except ImportError:
    create_enhanced_analyst = None

# 导出所有可用的分析师创建函数
__all__ = []

if create_market_analyst:
    __all__.append('create_market_analyst')

if create_fundamentals_analyst:
    __all__.append('create_fundamentals_analyst')

if create_news_analyst:
    __all__.append('create_news_analyst')

if create_enhanced_market_analyst:
    __all__.append('create_enhanced_market_analyst')

if create_enhanced_analyst:
    __all__.append('create_enhanced_analyst')

# 分析师类型映射
ANALYST_TYPES = {
    'market': create_market_analyst,
    'fundamentals': create_fundamentals_analyst,
    'news': create_news_analyst,
    'enhanced_market': create_enhanced_market_analyst,
    'enhanced': create_enhanced_analyst,
}

# 过滤掉None值
ANALYST_TYPES = {k: v for k, v in ANALYST_TYPES.items() if v is not None}


def get_available_analysts():
    """获取所有可用的分析师类型"""
    return list(ANALYST_TYPES.keys())


def create_analyst(analyst_type: str, **kwargs):
    """通用分析师创建函数"""
    if analyst_type not in ANALYST_TYPES:
        available = ', '.join(get_available_analysts())
        raise ValueError(f"未知的分析师类型: {analyst_type}。可用类型: {available}")
    
    return ANALYST_TYPES[analyst_type](**kwargs)


# 打印可用的分析师
if __name__ == "__main__":
    print("可用的分析师类型:")
    for analyst_type in get_available_analysts():
        print(f"  - {analyst_type}")