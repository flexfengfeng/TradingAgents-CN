#!/usr/bin/env python3
"""
缓存管理工具
提供缓存路径和基本缓存管理功能
"""

import os
from pathlib import Path
from typing import Optional


def get_cache_path(cache_name: str = "default") -> str:
    """
    获取缓存目录路径
    
    Args:
        cache_name: 缓存名称
        
    Returns:
        缓存目录路径
    """
    # 获取项目根目录
    project_root = Path(__file__).parent.parent.parent
    
    # 创建缓存目录
    cache_dir = project_root / "cache" / cache_name
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    return str(cache_dir)


def get_data_cache_path() -> str:
    """
    获取数据缓存目录路径
    
    Returns:
        数据缓存目录路径
    """
    return get_cache_path("data")


def get_analysis_cache_path() -> str:
    """
    获取分析缓存目录路径
    
    Returns:
        分析缓存目录路径
    """
    return get_cache_path("analysis")


def get_temp_cache_path() -> str:
    """
    获取临时缓存目录路径
    
    Returns:
        临时缓存目录路径
    """
    return get_cache_path("temp")


def clear_cache(cache_name: str = "default") -> bool:
    """
    清理指定缓存目录
    
    Args:
        cache_name: 缓存名称
        
    Returns:
        是否清理成功
    """
    try:
        cache_path = Path(get_cache_path(cache_name))
        if cache_path.exists():
            import shutil
            shutil.rmtree(cache_path)
            cache_path.mkdir(parents=True, exist_ok=True)
            return True
        return True
    except Exception:
        return False


def get_cache_size(cache_name: str = "default") -> int:
    """
    获取缓存目录大小（字节）
    
    Args:
        cache_name: 缓存名称
        
    Returns:
        缓存大小（字节）
    """
    try:
        cache_path = Path(get_cache_path(cache_name))
        if not cache_path.exists():
            return 0
        
        total_size = 0
        for file_path in cache_path.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        
        return total_size
    except Exception:
        return 0


def format_cache_size(size_bytes: int) -> str:
    """
    格式化缓存大小显示
    
    Args:
        size_bytes: 字节大小
        
    Returns:
        格式化的大小字符串
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"