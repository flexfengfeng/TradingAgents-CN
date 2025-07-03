#!/usr/bin/env python3
"""
增强分析工具包
集成所有增强分析器，提供统一的接口
实现"先精确计算，再交给DeepSeek分析"的完整解决方案
"""

import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
import json

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入增强分析器
try:
    from .analyzers.enhanced_technical_analysis import EnhancedTechnicalAnalyzer
    from .analyzers.enhanced_fundamentals_analysis import EnhancedFundamentalsAnalyzer
    from .analyzers.enhanced_sentiment_analysis import EnhancedSentimentAnalyzer
    from .analyzers.enhanced_risk_analysis import EnhancedRiskAnalyzer
except ImportError as e:
    print(f"⚠️ 导入增强分析器失败: {e}")
    print("请确保所有增强分析器文件都在analyzers目录下")


class EnhancedAnalysisToolkit:
    """
    增强分析工具包
    整合技术分析、基本面分析、情绪分析和风险评估的增强版本
    """
    
    def __init__(self):
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        
        # 初始化各个分析器
        try:
            self.technical_analyzer = EnhancedTechnicalAnalyzer()
            print("✅ 技术分析器初始化成功")
        except Exception as e:
            print(f"❌ 技术分析器初始化失败: {e}")
            self.technical_analyzer = None
        
        try:
            self.fundamentals_analyzer = EnhancedFundamentalsAnalyzer()
            print("✅ 基本面分析器初始化成功")
        except Exception as e:
            print(f"❌ 基本面分析器初始化失败: {e}")
            self.fundamentals_analyzer = None
        
        try:
            self.sentiment_analyzer = EnhancedSentimentAnalyzer()
            print("✅ 情绪分析器初始化成功")
        except Exception as e:
            print(f"❌ 情绪分析器初始化失败: {e}")
            self.sentiment_analyzer = None
        
        try:
            self.risk_analyzer = EnhancedRiskAnalyzer()
            print("✅ 风险分析器初始化成功")
        except Exception as e:
            print(f"❌ 风险分析器初始化失败: {e}")
            self.risk_analyzer = None
        
        print("🚀 增强分析工具包初始化完成")
    
    def comprehensive_analysis(self, ticker: str, stock_data: str, 
                             fundamentals_data: str = None, 
                             news_data: str = None,
                             market_data: str = None,
                             company_name: str = "未知公司") -> Dict[str, Any]:
        """
        执行综合增强分析
        
        Args:
            ticker: 股票代码
            stock_data: 股票价格数据
            fundamentals_data: 基本面数据（可选）
            news_data: 新闻数据（可选）
            market_data: 市场数据（可选）
            company_name: 公司名称
        
        Returns:
            综合分析结果字典
        """
        print(f"🔍 开始对 {ticker}（{company_name}）进行综合增强分析...")
        
        results = {
            "ticker": ticker,
            "company_name": company_name,
            "analysis_date": self.current_date,
            "technical_analysis": None,
            "fundamentals_analysis": None,
            "sentiment_analysis": None,
            "risk_analysis": None,
            "comprehensive_summary": None,
            "investment_recommendation": None,
            "analysis_quality": None
        }
        
        # 1. 技术分析
        if self.technical_analyzer and stock_data:
            try:
                print("📈 执行增强技术分析...")
                results["technical_analysis"] = self.technical_analyzer.analyze_stock_data(stock_data)
                print("✅ 技术分析完成")
            except Exception as e:
                print(f"❌ 技术分析失败: {e}")
                results["technical_analysis"] = {"error": str(e)}
        
        # 2. 基本面分析
        if self.fundamentals_analyzer:
            try:
                print("📊 执行增强基本面分析...")
                results["fundamentals_analysis"] = self.fundamentals_analyzer.analyze_fundamentals(
                    stock_data, fundamentals_data
                )
                print("✅ 基本面分析完成")
            except Exception as e:
                print(f"❌ 基本面分析失败: {e}")
                results["fundamentals_analysis"] = {"error": str(e)}
        
        # 3. 情绪分析
        if self.sentiment_analyzer and news_data:
            try:
                print("📰 执行增强情绪分析...")
                results["sentiment_analysis"] = self.sentiment_analyzer.analyze_news_sentiment(
                    news_data, ticker
                )
                print("✅ 情绪分析完成")
            except Exception as e:
                print(f"❌ 情绪分析失败: {e}")
                results["sentiment_analysis"] = {"error": str(e)}
        
        # 4. 风险评估
        if self.risk_analyzer:
            try:
                print("⚠️ 执行增强风险评估...")
                results["risk_analysis"] = self.risk_analyzer.analyze_risk_metrics(
                    stock_data, market_data, fundamentals_data
                )
                print("✅ 风险评估完成")
            except Exception as e:
                print(f"❌ 风险评估失败: {e}")
                results["risk_analysis"] = {"error": str(e)}
        
        # 5. 综合评估
        results["comprehensive_summary"] = self._generate_comprehensive_summary(results)
        results["investment_recommendation"] = self._generate_investment_recommendation(results)
        results["analysis_quality"] = self._assess_analysis_quality(results)
        
        print("🎯 综合增强分析完成")
        return results
    
    def generate_enhanced_report(self, analysis_results: Dict[str, Any]) -> str:
        """
        生成增强分析报告
        
        Args:
            analysis_results: 综合分析结果
        
        Returns:
            格式化的增强分析报告
        """
        ticker = analysis_results.get("ticker", "未知")
        company_name = analysis_results.get("company_name", "未知公司")
        
        report = f"""# {ticker}（{company_name}）增强分析综合报告

## 📋 分析概览

- **分析日期**: {analysis_results.get('analysis_date', 'N/A')}
- **股票代码**: {ticker}
- **公司名称**: {company_name}
- **分析质量**: {analysis_results.get('analysis_quality', {}).get('overall_quality', '未知')}

---

"""
        
        # 技术分析部分
        if analysis_results.get("technical_analysis") and "error" not in analysis_results["technical_analysis"]:
            if self.technical_analyzer:
                tech_report = self.technical_analyzer.format_enhanced_report(
                    analysis_results["technical_analysis"], ticker, company_name
                )
                report += tech_report + "\n\n---\n\n"
        
        # 基本面分析部分
        if analysis_results.get("fundamentals_analysis") and "error" not in analysis_results["fundamentals_analysis"]:
            if self.fundamentals_analyzer:
                fund_report = self.fundamentals_analyzer.format_enhanced_report(
                    analysis_results["fundamentals_analysis"], ticker, company_name
                )
                report += fund_report + "\n\n---\n\n"
        
        # 情绪分析部分
        if analysis_results.get("sentiment_analysis") and "error" not in analysis_results["sentiment_analysis"]:
            if self.sentiment_analyzer:
                sent_report = self.sentiment_analyzer.format_enhanced_report(
                    analysis_results["sentiment_analysis"], ticker, company_name
                )
                report += sent_report + "\n\n---\n\n"
        
        # 风险评估部分
        if analysis_results.get("risk_analysis") and "error" not in analysis_results["risk_analysis"]:
            if self.risk_analyzer:
                risk_report = self.risk_analyzer.format_enhanced_report(
                    analysis_results["risk_analysis"], ticker, company_name
                )
                report += risk_report + "\n\n---\n\n"
        
        # 综合评估部分
        summary = analysis_results.get("comprehensive_summary", {})
        recommendation = analysis_results.get("investment_recommendation", {})
        
        report += f"""## 🎯 综合评估与投资建议

### 综合评分
- **技术面评分**: {summary.get('technical_score', 'N/A')}/100
- **基本面评分**: {summary.get('fundamentals_score', 'N/A')}/100
- **情绪面评分**: {summary.get('sentiment_score', 'N/A')}/100
- **风险控制评分**: {summary.get('risk_score', 'N/A')}/100
- **综合评分**: {summary.get('overall_score', 'N/A')}/100

### 投资建议
- **投资评级**: {recommendation.get('rating', '未知')}
- **目标价位**: {recommendation.get('target_price', 'N/A')}
- **投资期限**: {recommendation.get('time_horizon', 'N/A')}
- **风险等级**: {recommendation.get('risk_level', 'N/A')}

### 关键要点
"""
        
        key_points = summary.get('key_points', [])
        for i, point in enumerate(key_points[:5], 1):
            report += f"{i}. {point}\n"
        
        report += "\n### 风险提示\n"
        risk_warnings = recommendation.get('risk_warnings', [])
        for warning in risk_warnings[:3]:
            report += f"⚠️ {warning}\n"
        
        report += f"""

---

## 📊 数据质量说明

{analysis_results.get('analysis_quality', {}).get('quality_description', '数据质量信息不可用')}

---

*本报告由增强分析工具包生成，采用"先精确计算，再AI分析"的方法*
*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return report
    
    def _generate_comprehensive_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """生成综合评估摘要"""
        summary = {
            "technical_score": 0,
            "fundamentals_score": 0,
            "sentiment_score": 0,
            "risk_score": 0,
            "overall_score": 0,
            "key_points": [],
            "strengths": [],
            "weaknesses": []
        }
        
        # 技术面评分
        tech_analysis = results.get("technical_analysis")
        if tech_analysis and "error" not in tech_analysis:
            # 基于技术指标计算评分
            signals = tech_analysis.get("signals", {})
            if signals:
                bullish_count = sum(1 for signal in signals.values() if signal == "买入" or signal == "看涨")
                total_signals = len(signals)
                summary["technical_score"] = (bullish_count / total_signals * 100) if total_signals > 0 else 50
            
            # 添加技术面要点
            trend = tech_analysis.get("trend_analysis", {}).get("overall_trend", "未知")
            if trend != "未知":
                summary["key_points"].append(f"技术面趋势: {trend}")
        
        # 基本面评分
        fund_analysis = results.get("fundamentals_analysis")
        if fund_analysis and "error" not in fund_analysis:
            # 基于估值和财务健康度计算评分
            valuation = fund_analysis.get("valuation_metrics", {}).get("valuation_level", "未知")
            health_score = fund_analysis.get("financial_health", {}).get("health_score", 50)
            
            if valuation == "低估":
                summary["fundamentals_score"] = min(100, health_score + 20)
            elif valuation == "合理":
                summary["fundamentals_score"] = health_score
            else:
                summary["fundamentals_score"] = max(0, health_score - 20)
            
            # 添加基本面要点
            if valuation != "未知":
                summary["key_points"].append(f"估值水平: {valuation}")
        
        # 情绪面评分
        sent_analysis = results.get("sentiment_analysis")
        if sent_analysis and "error" not in sent_analysis:
            # 基于综合情绪计算评分
            weighted_sentiment = sent_analysis.get("comprehensive_sentiment", {}).get("weighted_sentiment", 0)
            confidence = sent_analysis.get("comprehensive_sentiment", {}).get("confidence_score", 0.5)
            
            # 将情绪分数转换为0-100评分
            sentiment_score = (weighted_sentiment + 1) * 50  # 将[-1,1]转换为[0,100]
            summary["sentiment_score"] = sentiment_score * confidence  # 用置信度加权
            
            # 添加情绪面要点
            overall_sentiment = sent_analysis.get("comprehensive_sentiment", {}).get("overall_sentiment", "未知")
            if overall_sentiment != "未知":
                summary["key_points"].append(f"市场情绪: {overall_sentiment}")
        
        # 风险评分（风险越低评分越高）
        risk_analysis = results.get("risk_analysis")
        if risk_analysis and "error" not in risk_analysis:
            risk_score = risk_analysis.get("comprehensive_risk", {}).get("overall_risk_score", 50)
            summary["risk_score"] = 100 - risk_score  # 风险评分转换为质量评分
            
            # 添加风险要点
            risk_level = risk_analysis.get("comprehensive_risk", {}).get("risk_level", "未知")
            if risk_level != "未知":
                summary["key_points"].append(f"风险水平: {risk_level}")
        
        # 计算综合评分
        scores = [summary["technical_score"], summary["fundamentals_score"], 
                 summary["sentiment_score"], summary["risk_score"]]
        valid_scores = [s for s in scores if s > 0]
        
        if valid_scores:
            summary["overall_score"] = sum(valid_scores) / len(valid_scores)
        
        # 识别优势和劣势
        if summary["technical_score"] > 70:
            summary["strengths"].append("技术面表现强劲")
        elif summary["technical_score"] < 30:
            summary["weaknesses"].append("技术面偏弱")
        
        if summary["fundamentals_score"] > 70:
            summary["strengths"].append("基本面健康")
        elif summary["fundamentals_score"] < 30:
            summary["weaknesses"].append("基本面存在问题")
        
        if summary["sentiment_score"] > 70:
            summary["strengths"].append("市场情绪积极")
        elif summary["sentiment_score"] < 30:
            summary["weaknesses"].append("市场情绪消极")
        
        if summary["risk_score"] > 70:
            summary["strengths"].append("风险控制良好")
        elif summary["risk_score"] < 30:
            summary["weaknesses"].append("风险水平较高")
        
        return summary
    
    def _generate_investment_recommendation(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """生成投资建议"""
        recommendation = {
            "rating": "持有",
            "target_price": None,
            "time_horizon": "中期（3-6个月）",
            "risk_level": "中等",
            "position_size": "标准仓位",
            "risk_warnings": [],
            "action_items": []
        }
        
        summary = results.get("comprehensive_summary", {})
        overall_score = summary.get("overall_score", 50)
        
        # 基于综合评分确定投资评级
        if overall_score >= 80:
            recommendation["rating"] = "强烈买入"
            recommendation["position_size"] = "重仓"
        elif overall_score >= 65:
            recommendation["rating"] = "买入"
            recommendation["position_size"] = "标准仓位"
        elif overall_score >= 50:
            recommendation["rating"] = "持有"
            recommendation["position_size"] = "轻仓"
        elif overall_score >= 35:
            recommendation["rating"] = "减持"
            recommendation["position_size"] = "减仓"
        else:
            recommendation["rating"] = "卖出"
            recommendation["position_size"] = "清仓"
        
        # 基于风险分析调整建议
        risk_analysis = results.get("risk_analysis")
        if risk_analysis and "error" not in risk_analysis:
            risk_level = risk_analysis.get("comprehensive_risk", {}).get("risk_level", "中")
            recommendation["risk_level"] = risk_level
            
            if risk_level == "高":
                recommendation["risk_warnings"].append("投资风险较高，建议谨慎操作")
                if recommendation["rating"] in ["强烈买入", "买入"]:
                    recommendation["position_size"] = "轻仓"  # 降低仓位
            
            # 添加风险预警
            alerts = risk_analysis.get("risk_alerts", [])
            for alert in alerts[:2]:  # 只取前2个最重要的预警
                recommendation["risk_warnings"].append(alert.get("description", ""))
        
        # 基于技术分析调整时间期限
        tech_analysis = results.get("technical_analysis")
        if tech_analysis and "error" not in tech_analysis:
            trend = tech_analysis.get("trend_analysis", {}).get("overall_trend", "")
            if "短期" in trend:
                recommendation["time_horizon"] = "短期（1-3个月）"
            elif "长期" in trend:
                recommendation["time_horizon"] = "长期（6-12个月）"
        
        # 生成行动建议
        if recommendation["rating"] in ["强烈买入", "买入"]:
            recommendation["action_items"].extend([
                "可考虑分批建仓",
                "设置合理的止损点",
                "关注市场整体走势"
            ])
        elif recommendation["rating"] == "持有":
            recommendation["action_items"].extend([
                "继续观察基本面变化",
                "关注技术面突破信号",
                "保持现有仓位"
            ])
        else:
            recommendation["action_items"].extend([
                "考虑逐步减仓",
                "寻找更好的投资机会",
                "加强风险控制"
            ])
        
        return recommendation
    
    def _assess_analysis_quality(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """评估分析质量"""
        quality = {
            "data_completeness": 0,
            "analysis_coverage": 0,
            "overall_quality": "未知",
            "quality_description": "",
            "limitations": []
        }
        
        # 评估数据完整性
        available_analyses = 0
        total_analyses = 4  # 技术、基本面、情绪、风险
        
        if results.get("technical_analysis") and "error" not in results["technical_analysis"]:
            available_analyses += 1
        else:
            quality["limitations"].append("技术分析数据不足")
        
        if results.get("fundamentals_analysis") and "error" not in results["fundamentals_analysis"]:
            available_analyses += 1
        else:
            quality["limitations"].append("基本面数据不足")
        
        if results.get("sentiment_analysis") and "error" not in results["sentiment_analysis"]:
            available_analyses += 1
        else:
            quality["limitations"].append("新闻情绪数据不足")
        
        if results.get("risk_analysis") and "error" not in results["risk_analysis"]:
            available_analyses += 1
        else:
            quality["limitations"].append("风险评估数据不足")
        
        quality["analysis_coverage"] = (available_analyses / total_analyses) * 100
        
        # 评估总体质量
        if quality["analysis_coverage"] >= 75:
            quality["overall_quality"] = "优秀"
            quality["quality_description"] = "数据完整，分析全面，结果可信度高"
        elif quality["analysis_coverage"] >= 50:
            quality["overall_quality"] = "良好"
            quality["quality_description"] = "数据基本完整，分析较为全面，结果具有参考价值"
        else:
            quality["overall_quality"] = "一般"
            quality["quality_description"] = "数据不够完整，分析覆盖面有限，建议补充更多数据"
        
        return quality
    
    def save_analysis_results(self, results: Dict[str, Any], filename: str = None) -> str:
        """保存分析结果到文件"""
        if filename is None:
            ticker = results.get("ticker", "unknown")
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"enhanced_analysis_{ticker}_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2, default=str)
            print(f"✅ 分析结果已保存到: {filename}")
            return filename
        except Exception as e:
            print(f"❌ 保存分析结果失败: {e}")
            return None
    
    def load_analysis_results(self, filename: str) -> Optional[Dict[str, Any]]:
        """从文件加载分析结果"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                results = json.load(f)
            print(f"✅ 分析结果已从 {filename} 加载")
            return results
        except Exception as e:
            print(f"❌ 加载分析结果失败: {e}")
            return None


def demo_enhanced_analysis():
    """演示增强分析工具包的使用"""
    print("🚀 增强分析工具包演示")
    print("=" * 50)
    
    # 初始化工具包
    toolkit = EnhancedAnalysisToolkit()
    
    # 模拟数据
    ticker = "000001"
    company_name = "平安银行"
    
    # 模拟股票数据
    stock_data = """
    日期,开盘价,最高价,最低价,收盘价,成交量
    2024-01-01,10.50,10.80,10.30,10.75,1500000
    2024-01-02,10.75,11.00,10.60,10.90,1800000
    2024-01-03,10.90,11.20,10.85,11.10,2000000
    2024-01-04,11.10,11.30,10.95,11.25,1700000
    2024-01-05,11.25,11.50,11.15,11.40,1900000
    """
    
    # 模拟基本面数据
    fundamentals_data = """
    市盈率: 8.5
    市净率: 0.85
    净资产收益率: 12.3%
    负债权益比: 0.45
    流动比率: 1.8
    """
    
    # 模拟新闻数据
    news_data = """
    标题: 平安银行发布三季度业绩报告，净利润同比增长15%
    内容: 平安银行今日发布三季度财报，实现净利润同比增长15%，超出市场预期。
    时间: 2小时前
    来源: 证券时报
    
    标题: 央行降准释放流动性，银行股集体上涨
    内容: 央行宣布降准0.5个百分点，为市场释放长期流动性，银行股普遍受益。
    时间: 1天前
    来源: 新华社
    """
    
    # 执行综合分析
    results = toolkit.comprehensive_analysis(
        ticker=ticker,
        stock_data=stock_data,
        fundamentals_data=fundamentals_data,
        news_data=news_data,
        company_name=company_name
    )
    
    # 生成报告
    report = toolkit.generate_enhanced_report(results)
    
    # 保存结果
    filename = toolkit.save_analysis_results(results)
    
    # 输出报告
    print("\n" + "=" * 80)
    print("📊 增强分析报告")
    print("=" * 80)
    print(report)
    
    return results, report


if __name__ == "__main__":
    # 运行演示
    demo_enhanced_analysis()