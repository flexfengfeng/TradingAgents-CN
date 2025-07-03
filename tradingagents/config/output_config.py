#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
输出路径配置模块
统一管理所有生成文件的输出路径
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Optional


class OutputConfig:
    """
    输出路径配置类
    """
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        初始化输出配置
        
        Args:
            base_dir: 基础目录，默认为项目根目录
        """
        if base_dir is None:
            # 获取项目根目录
            current_file = Path(__file__)
            self.base_dir = current_file.parent.parent.parent
        else:
            self.base_dir = Path(base_dir)
    
    @property
    def reports_dir(self) -> Path:
        """报告输出目录"""
        return self.base_dir / "data" / "reports"
    
    @property
    def logs_dir(self) -> Path:
        """日志输出目录"""
        return self.base_dir / "data" / "logs"
    
    @property
    def cache_dir(self) -> Path:
        """缓存目录"""
        return self.base_dir / "data" / "cache"
    
    @property
    def temp_dir(self) -> Path:
        """临时文件目录"""
        return self.base_dir / "data" / "temp"
    
    def ensure_dirs(self):
        """确保所有必要的目录存在"""
        for dir_path in [self.reports_dir, self.logs_dir, self.cache_dir, self.temp_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def get_report_path(self, filename: str, subdir: Optional[str] = None) -> Path:
        """
        获取报告文件路径
        
        Args:
            filename: 文件名
            subdir: 子目录名（可选）
        
        Returns:
            完整的文件路径
        """
        if subdir:
            report_path = self.reports_dir / subdir
            report_path.mkdir(parents=True, exist_ok=True)
            return report_path / filename
        else:
            self.reports_dir.mkdir(parents=True, exist_ok=True)
            return self.reports_dir / filename
    
    def get_timestamped_filename(self, prefix: str, suffix: str = ".md") -> str:
        """
        生成带时间戳的文件名
        
        Args:
            prefix: 文件名前缀
            suffix: 文件扩展名
        
        Returns:
            带时间戳的文件名
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{prefix}_{timestamp}{suffix}"
    
    def get_analysis_report_path(self, symbol: str, analysis_type: str = "enhanced_analysis") -> Path:
        """
        获取分析报告路径
        
        Args:
            symbol: 股票代码
            analysis_type: 分析类型
        
        Returns:
            分析报告文件路径
        """
        filename = self.get_timestamped_filename(f"{symbol}_{analysis_type}")
        return self.get_report_path(filename)
    
    def get_data_report_path(self, symbol: str, data_type: str = "enhanced_data") -> Path:
        """
        获取数据报告路径
        
        Args:
            symbol: 股票代码
            data_type: 数据类型
        
        Returns:
            数据报告文件路径
        """
        filename = self.get_timestamped_filename(f"{data_type}_{symbol}")
        return self.get_report_path(filename)
    
    def get_comparison_report_path(self, symbol: str) -> Path:
        """
        获取对比报告路径
        
        Args:
            symbol: 股票代码
        
        Returns:
            对比报告文件路径
        """
        filename = self.get_timestamped_filename(f"comparison_analysis_{symbol}")
        return self.get_report_path(filename)
    
    def cleanup_old_files(self, days: int = 7):
        """
        清理旧文件
        
        Args:
            days: 保留天数，超过此天数的文件将被删除
        """
        import time
        
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        
        for dir_path in [self.reports_dir, self.logs_dir, self.temp_dir]:
            if dir_path.exists():
                for file_path in dir_path.rglob("*"):
                    if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                        try:
                            file_path.unlink()
                            print(f"🗑️ 已删除旧文件: {file_path}")
                        except Exception as e:
                            print(f"❌ 删除文件失败 {file_path}: {e}")


# 全局配置实例
output_config = OutputConfig()


def get_output_config() -> OutputConfig:
    """获取输出配置实例"""
    return output_config


def ensure_output_dirs():
    """确保输出目录存在"""
    output_config.ensure_dirs()


def get_report_path(filename: str, subdir: Optional[str] = None) -> Path:
    """获取报告文件路径的便捷函数"""
    return output_config.get_report_path(filename, subdir)


def get_analysis_report_path(symbol: str, analysis_type: str = "enhanced_analysis") -> Path:
    """获取分析报告路径的便捷函数"""
    return output_config.get_analysis_report_path(symbol, analysis_type)


def get_data_report_path(symbol: str, data_type: str = "enhanced_data") -> Path:
    """获取数据报告路径的便捷函数"""
    return output_config.get_data_report_path(symbol, data_type)


def get_comparison_report_path(symbol: str) -> Path:
    """获取对比报告路径的便捷函数"""
    return output_config.get_comparison_report_path(symbol)