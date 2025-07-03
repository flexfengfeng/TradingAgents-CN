#!/usr/bin/env python3
"""
增强新闻情绪分析器
先量化计算情绪评分和影响权重，然后交给DeepSeek进行深度分析
解决DeepSeek在情绪量化上不够精确的问题
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
import re
import json
from collections import defaultdict
import math


class EnhancedSentimentAnalyzer:
    """
    增强新闻情绪分析器
    功能：先量化计算情绪评分和影响权重，再格式化为适合LLM分析的报告
    """
    
    def __init__(self):
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        self.sentiment_keywords = self._load_sentiment_keywords()
        self.impact_weights = self._load_impact_weights()
        print("📰 增强新闻情绪分析器初始化完成")
    
    def _load_sentiment_keywords(self) -> Dict[str, Dict[str, float]]:
        """加载情绪关键词词典"""
        return {
            "positive": {
                "上涨": 0.8, "涨停": 1.0, "突破": 0.7, "创新高": 0.9,
                "利好": 0.8, "盈利": 0.6, "增长": 0.7, "扩张": 0.6,
                "合作": 0.5, "签约": 0.6, "中标": 0.7, "获得": 0.5,
                "成功": 0.6, "优秀": 0.5, "强劲": 0.7, "超预期": 0.8,
                "买入": 0.6, "推荐": 0.5, "看好": 0.6, "乐观": 0.6
            },
            "negative": {
                "下跌": -0.8, "跌停": -1.0, "暴跌": -0.9, "破位": -0.7,
                "利空": -0.8, "亏损": -0.7, "下滑": -0.6, "萎缩": -0.6,
                "风险": -0.6, "警告": -0.7, "调查": -0.5, "处罚": -0.8,
                "失败": -0.6, "困难": -0.5, "疲软": -0.6, "低于预期": -0.7,
                "卖出": -0.6, "减持": -0.5, "看空": -0.6, "悲观": -0.6
            },
            "neutral": {
                "公告": 0.0, "披露": 0.0, "发布": 0.0, "召开": 0.0,
                "会议": 0.0, "讨论": 0.0, "分析": 0.0, "研究": 0.0
            }
        }
    
    def _load_impact_weights(self) -> Dict[str, float]:
        """加载影响权重配置"""
        return {
            "news_source": {
                "央视新闻": 1.0, "新华社": 1.0, "人民日报": 1.0,
                "证券时报": 0.9, "上海证券报": 0.9, "中国证券报": 0.9,
                "财经": 0.8, "第一财经": 0.8, "21世纪经济报道": 0.8,
                "新浪财经": 0.7, "腾讯财经": 0.7, "网易财经": 0.7,
                "其他": 0.5
            },
            "news_type": {
                "政策": 1.0, "监管": 0.9, "业绩": 0.9, "重组": 0.8,
                "合作": 0.7, "产品": 0.6, "人事": 0.5, "其他": 0.4
            },
            "time_decay": {
                "当日": 1.0, "1天前": 0.9, "2天前": 0.8, "3天前": 0.7,
                "1周前": 0.6, "2周前": 0.4, "1月前": 0.2, "更早": 0.1
            }
        }
    
    def analyze_news_sentiment(self, news_data: str, stock_code: str = None) -> Dict[str, Any]:
        """
        分析新闻情绪数据，计算量化指标
        
        Args:
            news_data: 新闻数据
            stock_code: 股票代码（可选）
        
        Returns:
            包含计算结果的字典
        """
        try:
            print("📰 开始增强新闻情绪分析...")
            
            # 解析新闻数据
            news_items = self._parse_news_data(news_data)
            if not news_items:
                return {"error": "无法解析新闻数据"}
            
            # 计算情绪评分
            sentiment_scores = self._calculate_sentiment_scores(news_items)
            
            # 计算影响权重
            impact_weights = self._calculate_impact_weights(news_items)
            
            # 计算时间衰减
            time_decay_factors = self._calculate_time_decay(news_items)
            
            # 计算综合情绪指标
            comprehensive_sentiment = self._calculate_comprehensive_sentiment(
                sentiment_scores, impact_weights, time_decay_factors
            )
            
            # 情绪趋势分析
            sentiment_trend = self._analyze_sentiment_trend(news_items, sentiment_scores)
            
            # 热点话题分析
            hot_topics = self._analyze_hot_topics(news_items)
            
            # 市场关注度分析
            market_attention = self._analyze_market_attention(news_items)
            
            # 风险预警
            risk_alerts = self._generate_risk_alerts(comprehensive_sentiment, sentiment_trend)
            
            return {
                "news_count": len(news_items),
                "sentiment_scores": sentiment_scores,
                "impact_weights": impact_weights,
                "time_decay_factors": time_decay_factors,
                "comprehensive_sentiment": comprehensive_sentiment,
                "sentiment_trend": sentiment_trend,
                "hot_topics": hot_topics,
                "market_attention": market_attention,
                "risk_alerts": risk_alerts,
                "analysis_date": self.current_date,
                "data_quality": self._assess_news_data_quality(news_items)
            }
            
        except Exception as e:
            print(f"❌ 新闻情绪分析失败: {e}")
            return {"error": f"新闻情绪分析失败: {str(e)}"}
    
    def _parse_news_data(self, news_data: str) -> List[Dict[str, Any]]:
        """解析新闻数据"""
        news_items = []
        
        try:
            lines = news_data.split('\n')
            current_news = {}
            
            for line in lines:
                line = line.strip()
                if not line:
                    if current_news:
                        news_items.append(current_news)
                        current_news = {}
                    continue
                
                # 解析标题
                if line.startswith('标题:') or line.startswith('Title:'):
                    current_news['title'] = line.split(':', 1)[1].strip()
                
                # 解析内容
                elif line.startswith('内容:') or line.startswith('Content:'):
                    current_news['content'] = line.split(':', 1)[1].strip()
                
                # 解析时间
                elif line.startswith('时间:') or line.startswith('Time:'):
                    current_news['time'] = line.split(':', 1)[1].strip()
                
                # 解析来源
                elif line.startswith('来源:') or line.startswith('Source:'):
                    current_news['source'] = line.split(':', 1)[1].strip()
                
                # 解析URL
                elif line.startswith('链接:') or line.startswith('URL:'):
                    current_news['url'] = line.split(':', 1)[1].strip()
                
                # 如果没有明确标识，尝试智能解析
                elif ':' in line and len(current_news) == 0:
                    # 可能是标题
                    current_news['title'] = line
                elif len(line) > 20 and 'content' not in current_news:
                    # 可能是内容
                    current_news['content'] = line
            
            # 添加最后一条新闻
            if current_news:
                news_items.append(current_news)
            
            # 为缺失字段设置默认值
            for item in news_items:
                item.setdefault('title', '未知标题')
                item.setdefault('content', '')
                item.setdefault('time', self.current_date)
                item.setdefault('source', '未知来源')
                item.setdefault('url', '')
            
            return news_items
            
        except Exception as e:
            print(f"❌ 新闻数据解析失败: {e}")
            return []
    
    def _calculate_sentiment_scores(self, news_items: List[Dict]) -> Dict[str, Any]:
        """计算情绪评分"""
        scores = {
            "individual_scores": [],
            "positive_count": 0,
            "negative_count": 0,
            "neutral_count": 0,
            "average_score": 0.0,
            "sentiment_distribution": {},
            "extreme_sentiment_ratio": 0.0
        }
        
        total_score = 0.0
        
        for item in news_items:
            text = f"{item.get('title', '')} {item.get('content', '')}"
            score = self._calculate_text_sentiment(text)
            scores["individual_scores"].append({
                "title": item.get('title', ''),
                "score": score,
                "sentiment": self._classify_sentiment(score)
            })
            
            total_score += score
            
            # 统计情绪分布
            if score > 0.1:
                scores["positive_count"] += 1
            elif score < -0.1:
                scores["negative_count"] += 1
            else:
                scores["neutral_count"] += 1
        
        if news_items:
            scores["average_score"] = total_score / len(news_items)
        
        # 计算情绪分布
        total_count = len(news_items)
        if total_count > 0:
            scores["sentiment_distribution"] = {
                "positive_ratio": scores["positive_count"] / total_count,
                "negative_ratio": scores["negative_count"] / total_count,
                "neutral_ratio": scores["neutral_count"] / total_count
            }
        
        # 计算极端情绪比例
        extreme_count = sum(1 for item in scores["individual_scores"] 
                          if abs(item["score"]) > 0.7)
        scores["extreme_sentiment_ratio"] = extreme_count / total_count if total_count > 0 else 0
        
        return scores
    
    def _calculate_text_sentiment(self, text: str) -> float:
        """计算文本情绪评分"""
        score = 0.0
        word_count = 0
        
        # 正面情绪词汇
        for word, weight in self.sentiment_keywords["positive"].items():
            count = text.count(word)
            score += count * weight
            word_count += count
        
        # 负面情绪词汇
        for word, weight in self.sentiment_keywords["negative"].items():
            count = text.count(word)
            score += count * weight  # weight已经是负数
            word_count += count
        
        # 归一化处理
        if word_count > 0:
            score = score / math.sqrt(word_count)  # 使用平方根归一化
        
        # 限制在[-1, 1]范围内
        return max(-1.0, min(1.0, score))
    
    def _classify_sentiment(self, score: float) -> str:
        """分类情绪"""
        if score > 0.3:
            return "积极"
        elif score < -0.3:
            return "消极"
        else:
            return "中性"
    
    def _calculate_impact_weights(self, news_items: List[Dict]) -> Dict[str, Any]:
        """计算影响权重"""
        weights = {
            "individual_weights": [],
            "source_weights": {},
            "average_weight": 0.0,
            "high_impact_ratio": 0.0
        }
        
        total_weight = 0.0
        high_impact_count = 0
        
        for item in news_items:
            source = item.get('source', '其他')
            title = item.get('title', '')
            
            # 基础权重（基于来源）
            base_weight = self._get_source_weight(source)
            
            # 内容权重（基于关键词）
            content_weight = self._get_content_weight(title + ' ' + item.get('content', ''))
            
            # 综合权重
            final_weight = base_weight * content_weight
            
            weights["individual_weights"].append({
                "title": title,
                "source": source,
                "base_weight": base_weight,
                "content_weight": content_weight,
                "final_weight": final_weight
            })
            
            total_weight += final_weight
            
            if final_weight > 0.7:
                high_impact_count += 1
            
            # 统计来源权重分布
            if source not in weights["source_weights"]:
                weights["source_weights"][source] = []
            weights["source_weights"][source].append(final_weight)
        
        if news_items:
            weights["average_weight"] = total_weight / len(news_items)
            weights["high_impact_ratio"] = high_impact_count / len(news_items)
        
        # 计算各来源平均权重
        for source in weights["source_weights"]:
            source_weights = weights["source_weights"][source]
            weights["source_weights"][source] = {
                "average": sum(source_weights) / len(source_weights),
                "count": len(source_weights)
            }
        
        return weights
    
    def _get_source_weight(self, source: str) -> float:
        """获取来源权重"""
        for key, weight in self.impact_weights["news_source"].items():
            if key in source:
                return weight
        return self.impact_weights["news_source"]["其他"]
    
    def _get_content_weight(self, content: str) -> float:
        """获取内容权重"""
        weight = 1.0
        
        # 基于关键词调整权重
        high_impact_keywords = ["政策", "监管", "业绩", "重组", "并购", "IPO", "退市"]
        for keyword in high_impact_keywords:
            if keyword in content:
                weight *= 1.2
        
        # 基于数字调整权重（涉及具体数据的新闻通常更重要）
        if re.search(r'\d+%|\d+亿|\d+万', content):
            weight *= 1.1
        
        return min(weight, 2.0)  # 限制最大权重
    
    def _calculate_time_decay(self, news_items: List[Dict]) -> Dict[str, Any]:
        """计算时间衰减因子"""
        decay_factors = {
            "individual_factors": [],
            "average_decay": 0.0,
            "fresh_news_ratio": 0.0
        }
        
        current_time = datetime.now()
        total_decay = 0.0
        fresh_count = 0
        
        for item in news_items:
            time_str = item.get('time', self.current_date)
            decay_factor = self._calculate_single_time_decay(time_str, current_time)
            
            decay_factors["individual_factors"].append({
                "title": item.get('title', ''),
                "time": time_str,
                "decay_factor": decay_factor
            })
            
            total_decay += decay_factor
            
            if decay_factor > 0.8:  # 认为是新鲜新闻
                fresh_count += 1
        
        if news_items:
            decay_factors["average_decay"] = total_decay / len(news_items)
            decay_factors["fresh_news_ratio"] = fresh_count / len(news_items)
        
        return decay_factors
    
    def _calculate_single_time_decay(self, time_str: str, current_time: datetime) -> float:
        """计算单条新闻的时间衰减因子"""
        try:
            # 尝试解析时间字符串
            if '小时前' in time_str:
                hours = int(re.search(r'(\d+)', time_str).group(1))
                if hours < 24:
                    return 1.0
                else:
                    return 0.9
            elif '天前' in time_str:
                days = int(re.search(r'(\d+)', time_str).group(1))
                if days == 1:
                    return 0.9
                elif days == 2:
                    return 0.8
                elif days == 3:
                    return 0.7
                elif days <= 7:
                    return 0.6
                elif days <= 14:
                    return 0.4
                elif days <= 30:
                    return 0.2
                else:
                    return 0.1
            else:
                # 默认认为是当日新闻
                return 1.0
        except:
            return 0.5  # 无法解析时间时的默认值
    
    def _calculate_comprehensive_sentiment(self, sentiment_scores: Dict, 
                                         impact_weights: Dict, 
                                         time_decay_factors: Dict) -> Dict[str, Any]:
        """计算综合情绪指标"""
        comprehensive = {
            "weighted_sentiment": 0.0,
            "confidence_score": 0.0,
            "sentiment_strength": "弱",
            "market_impact_level": "低",
            "overall_sentiment": "中性"
        }
        
        if not sentiment_scores["individual_scores"]:
            return comprehensive
        
        # 计算加权情绪分数
        total_weighted_score = 0.0
        total_weight = 0.0
        
        for i, score_item in enumerate(sentiment_scores["individual_scores"]):
            sentiment = score_item["score"]
            weight = impact_weights["individual_weights"][i]["final_weight"]
            decay = time_decay_factors["individual_factors"][i]["decay_factor"]
            
            final_weight = weight * decay
            total_weighted_score += sentiment * final_weight
            total_weight += final_weight
        
        if total_weight > 0:
            comprehensive["weighted_sentiment"] = total_weighted_score / total_weight
        
        # 计算置信度分数
        news_count = len(sentiment_scores["individual_scores"])
        avg_weight = impact_weights["average_weight"]
        avg_decay = time_decay_factors["average_decay"]
        
        confidence = min(1.0, (news_count / 10) * avg_weight * avg_decay)
        comprehensive["confidence_score"] = confidence
        
        # 判断情绪强度
        abs_sentiment = abs(comprehensive["weighted_sentiment"])
        if abs_sentiment > 0.6:
            comprehensive["sentiment_strength"] = "强"
        elif abs_sentiment > 0.3:
            comprehensive["sentiment_strength"] = "中"
        else:
            comprehensive["sentiment_strength"] = "弱"
        
        # 判断市场影响水平
        impact_score = abs_sentiment * confidence
        if impact_score > 0.7:
            comprehensive["market_impact_level"] = "高"
        elif impact_score > 0.4:
            comprehensive["market_impact_level"] = "中"
        else:
            comprehensive["market_impact_level"] = "低"
        
        # 判断总体情绪
        weighted_sentiment = comprehensive["weighted_sentiment"]
        if weighted_sentiment > 0.2:
            comprehensive["overall_sentiment"] = "积极"
        elif weighted_sentiment < -0.2:
            comprehensive["overall_sentiment"] = "消极"
        else:
            comprehensive["overall_sentiment"] = "中性"
        
        return comprehensive
    
    def _analyze_sentiment_trend(self, news_items: List[Dict], sentiment_scores: Dict) -> Dict[str, Any]:
        """分析情绪趋势"""
        trend = {
            "trend_direction": "稳定",
            "trend_strength": 0.0,
            "volatility": 0.0,
            "recent_change": 0.0,
            "trend_description": ""
        }
        
        if len(sentiment_scores["individual_scores"]) < 3:
            return trend
        
        # 按时间排序（简化处理，假设新闻已按时间排序）
        scores = [item["score"] for item in sentiment_scores["individual_scores"]]
        
        # 计算趋势方向
        recent_scores = scores[-3:]  # 最近3条新闻
        earlier_scores = scores[:-3] if len(scores) > 3 else scores[:3]
        
        recent_avg = sum(recent_scores) / len(recent_scores)
        earlier_avg = sum(earlier_scores) / len(earlier_scores)
        
        trend["recent_change"] = recent_avg - earlier_avg
        
        if trend["recent_change"] > 0.1:
            trend["trend_direction"] = "上升"
        elif trend["recent_change"] < -0.1:
            trend["trend_direction"] = "下降"
        else:
            trend["trend_direction"] = "稳定"
        
        # 计算趋势强度
        trend["trend_strength"] = abs(trend["recent_change"])
        
        # 计算波动性
        if len(scores) > 1:
            score_std = np.std(scores)
            trend["volatility"] = score_std
        
        # 生成趋势描述
        if trend["trend_strength"] > 0.3:
            strength_desc = "强烈"
        elif trend["trend_strength"] > 0.1:
            strength_desc = "明显"
        else:
            strength_desc = "轻微"
        
        trend["trend_description"] = f"情绪呈{strength_desc}{trend['trend_direction']}趋势"
        
        return trend
    
    def _analyze_hot_topics(self, news_items: List[Dict]) -> Dict[str, Any]:
        """分析热点话题"""
        topics = {
            "keyword_frequency": {},
            "hot_keywords": [],
            "topic_clusters": [],
            "emerging_topics": []
        }
        
        # 提取关键词
        all_text = ""
        for item in news_items:
            all_text += f"{item.get('title', '')} {item.get('content', '')} "
        
        # 简单的关键词提取（实际应用中可以使用更复杂的NLP技术）
        keywords = re.findall(r'[\u4e00-\u9fa5]{2,4}', all_text)
        
        # 统计词频
        keyword_count = defaultdict(int)
        for keyword in keywords:
            if len(keyword) >= 2:  # 只考虑长度>=2的词
                keyword_count[keyword] += 1
        
        # 排序并取前10个
        sorted_keywords = sorted(keyword_count.items(), key=lambda x: x[1], reverse=True)
        topics["keyword_frequency"] = dict(sorted_keywords[:20])
        topics["hot_keywords"] = [kw for kw, count in sorted_keywords[:10] if count >= 2]
        
        return topics
    
    def _analyze_market_attention(self, news_items: List[Dict]) -> Dict[str, Any]:
        """分析市场关注度"""
        attention = {
            "news_volume": len(news_items),
            "attention_level": "低",
            "peak_attention_time": None,
            "attention_distribution": {},
            "media_coverage_breadth": 0
        }
        
        # 判断关注度水平
        if attention["news_volume"] > 20:
            attention["attention_level"] = "高"
        elif attention["news_volume"] > 10:
            attention["attention_level"] = "中"
        else:
            attention["attention_level"] = "低"
        
        # 统计媒体覆盖广度
        sources = set(item.get('source', '未知') for item in news_items)
        attention["media_coverage_breadth"] = len(sources)
        
        return attention
    
    def _generate_risk_alerts(self, comprehensive_sentiment: Dict, sentiment_trend: Dict) -> List[Dict[str, Any]]:
        """生成风险预警"""
        alerts = []
        
        # 极端负面情绪预警
        if comprehensive_sentiment["weighted_sentiment"] < -0.6:
            alerts.append({
                "type": "极端负面情绪",
                "level": "高",
                "description": "检测到极端负面情绪，可能对股价产生重大负面影响",
                "recommendation": "建议密切关注市场反应，考虑风险控制措施"
            })
        
        # 情绪急剧恶化预警
        if sentiment_trend["trend_direction"] == "下降" and sentiment_trend["trend_strength"] > 0.4:
            alerts.append({
                "type": "情绪急剧恶化",
                "level": "中",
                "description": "情绪呈现急剧下降趋势，市场信心可能受到冲击",
                "recommendation": "建议关注后续新闻动态，评估影响持续性"
            })
        
        # 高波动性预警
        if sentiment_trend["volatility"] > 0.5:
            alerts.append({
                "type": "情绪高波动",
                "level": "中",
                "description": "情绪波动性较高，市场可能面临不确定性",
                "recommendation": "建议谨慎操作，注意风险管理"
            })
        
        return alerts
    
    def _assess_news_data_quality(self, news_items: List[Dict]) -> Dict[str, Any]:
        """评估新闻数据质量"""
        quality = {
            "completeness": 0,
            "timeliness": 0,
            "source_reliability": 0,
            "overall_score": 0,
            "quality_level": "未知"
        }
        
        if not news_items:
            return quality
        
        # 评估完整性
        complete_items = sum(1 for item in news_items 
                           if item.get('title') and item.get('content') and item.get('source'))
        quality["completeness"] = (complete_items / len(news_items)) * 100
        
        # 评估时效性
        fresh_items = sum(1 for item in news_items 
                         if '小时前' in item.get('time', '') or '今天' in item.get('time', ''))
        quality["timeliness"] = (fresh_items / len(news_items)) * 100
        
        # 评估来源可靠性
        reliable_sources = ['央视', '新华社', '人民日报', '证券时报', '上海证券报', '中国证券报']
        reliable_items = sum(1 for item in news_items 
                           if any(source in item.get('source', '') for source in reliable_sources))
        quality["source_reliability"] = (reliable_items / len(news_items)) * 100
        
        # 计算总体评分
        quality["overall_score"] = (
            quality["completeness"] * 0.4 +
            quality["timeliness"] * 0.3 +
            quality["source_reliability"] * 0.3
        )
        
        if quality["overall_score"] >= 80:
            quality["quality_level"] = "优秀"
        elif quality["overall_score"] >= 60:
            quality["quality_level"] = "良好"
        else:
            quality["quality_level"] = "一般"
        
        return quality
    
    def format_enhanced_report(self, analysis_result: Dict[str, Any], ticker: str, company_name: str = "未知公司") -> str:
        """
        格式化增强新闻情绪分析报告
        
        Args:
            analysis_result: 分析结果字典
            ticker: 股票代码
            company_name: 公司名称
        
        Returns:
            格式化的报告字符串
        """
        if "error" in analysis_result:
            return f"# 新闻情绪分析报告 - {ticker}\n\n❌ 分析失败: {analysis_result['error']}"
        
        sentiment = analysis_result.get("comprehensive_sentiment", {})
        trend = analysis_result.get("sentiment_trend", {})
        topics = analysis_result.get("hot_topics", {})
        attention = analysis_result.get("market_attention", {})
        alerts = analysis_result.get("risk_alerts", [])
        quality = analysis_result.get("data_quality", {})
        
        report = f"""# {ticker}（{company_name}）增强新闻情绪分析报告

## 📰 量化情绪指标

### 综合情绪评估
- **加权情绪分数**: {sentiment.get('weighted_sentiment', 0):.3f}
- **置信度**: {sentiment.get('confidence_score', 0):.3f}
- **情绪强度**: {sentiment.get('sentiment_strength', '未知')}
- **市场影响水平**: {sentiment.get('market_impact_level', '未知')}
- **总体情绪**: {sentiment.get('overall_sentiment', '未知')}

### 情绪趋势分析
- **趋势方向**: {trend.get('trend_direction', '未知')}
- **趋势强度**: {trend.get('trend_strength', 0):.3f}
- **情绪波动性**: {trend.get('volatility', 0):.3f}
- **近期变化**: {trend.get('recent_change', 0):.3f}
- **趋势描述**: {trend.get('trend_description', '无')}

### 市场关注度
- **新闻数量**: {analysis_result.get('news_count', 0)}条
- **关注度水平**: {attention.get('attention_level', '未知')}
- **媒体覆盖广度**: {attention.get('media_coverage_breadth', 0)}家媒体

### 热点话题
- **热门关键词**: {', '.join(topics.get('hot_keywords', [])[:5])}
- **关键词频次**: {dict(list(topics.get('keyword_frequency', {}).items())[:5])}

### 风险预警
"""
        
        if alerts:
            for alert in alerts:
                report += f"- **{alert['type']}** ({alert['level']}风险): {alert['description']}\n"
        else:
            report += "- 暂无风险预警\n"
        
        report += f"""

### 数据质量评估
- **数据完整性**: {quality.get('completeness', 0):.1f}%
- **数据时效性**: {quality.get('timeliness', 0):.1f}%
- **来源可靠性**: {quality.get('source_reliability', 0):.1f}%
- **总体质量**: {quality.get('quality_level', '未知')}

---
*报告生成时间: {analysis_result.get('analysis_date', 'N/A')}*
*数据来源: 增强新闻情绪分析器*
"""
        
        return report


if __name__ == "__main__":
    print("📰 增强新闻情绪分析器模块")
    print("功能: 先量化计算情绪评分和影响权重，然后交给LLM进行深度分析")
    print("适用: 解决DeepSeek等LLM在情绪量化上不够精确的问题")