#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事件预测模型
基于三层验证法（静态星盘 + Dasha激活 + 过境触发）预测事件
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EventType(Enum):
    """事件类型"""
    MARRIAGE = "婚姻"
    CAREER = "职业"
    WEALTH = "财富"
    HEALTH = "健康"
    EDUCATION = "教育"
    CHILDREN = "子女"
    TRAVEL = "旅行"
    SPIRITUAL = "灵性"


class RiskLevel(Enum):
    """风险等级"""
    LOW = "低"
    MEDIUM = "中"
    HIGH = "高"
    CRITICAL = "极高"


@dataclass
class Prediction:
    """预测结果"""
    event_type: EventType
    description: str
    probability: float  # 0-100
    risk_level: RiskLevel
    timing: Optional[str]
    key_factors: List[str]
    recommendations: List[str]


class EventPredictionModel:
    """事件预测模型"""
    
    def __init__(self, chart_data: Dict, dasha_data: Optional[Dict] = None, 
                 transit_data: Optional[Dict] = None):
        """
        初始化事件预测模型
        
        Args:
            chart_data: 星盘数据
            dasha_data: 大运周期数据
            transit_data: 过境数据
        """
        self.chart = chart_data
        self.dasha = dasha_data
        self.transit = transit_data
        self.predictions = []
    
    def predict_all_events(self) -> List[Prediction]:
        """预测所有类型的事件"""
        predictions = []
        
        # 1. 婚姻预测
        marriage_pred = self.predict_marriage()
        if marriage_pred:
            predictions.append(marriage_pred)
        
        # 2. 职业预测
        career_pred = self.predict_career()
        if career_pred:
            predictions.append(career_pred)
        
        # 3. 财富预测
        wealth_pred = self.predict_wealth()
        if wealth_pred:
            predictions.append(wealth_pred)
        
        # 4. 健康预测
        health_pred = self.predict_health()
        if health_pred:
            predictions.append(health_pred)
        
        self.predictions = predictions
        return predictions
    
    def predict_marriage(self) -> Optional[Prediction]:
        """
        婚姻预测（三层验证法）
        
        第一层：静态星盘分析
        - 7宫状态
        - 金星状态
        - 婚姻相关Yoga
        
        第二层：Dasha激活
        - 当前Dasha主星是否掌管7宫或金星
        - 当前Antardasha主星是否掌管7宫或金星
        
        第三层：过境触发
        - 木星过境7宫
        - 土星过境7宫
        """
        # 第一层：静态分析
        static_factors = self._analyze_marriage_static()
        
        # 第二层：Dasha激活
        dasha_activation = self._analyze_marriage_dasha()
        
        # 第三层：过境触发
        transit_trigger = self._analyze_marriage_transit()
        
        # 综合判断
        probability = self._calculate_marriage_probability(
            static_factors, dasha_activation, transit_trigger
        )
        
        risk_level = self._assess_marriage_risk(static_factors)
        
        timing = self._predict_marriage_timing(dasha_activation, transit_trigger)
        
        key_factors = []
        if static_factors.get('7th_house_afflicted'):
            key_factors.append("7宫受克")
        if static_factors.get('venus_weak'):
            key_factors.append("金星弱势")
        if static_factors.get('marriage_yoga'):
            key_factors.append("婚姻Yoga")
        
        recommendations = []
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            recommendations.append("建议进行详细合婚分析")
            recommendations.append("考虑补救措施")
        else:
            recommendations.append("婚姻前景良好")
        
        return Prediction(
            event_type=EventType.MARRIAGE,
            description="婚姻预测",
            probability=probability,
            risk_level=risk_level,
            timing=timing,
            key_factors=key_factors,
            recommendations=recommendations
        )
    
    def predict_career(self) -> Optional[Prediction]:
        """职业预测"""
        # 第一层：静态分析
        static_factors = self._analyze_career_static()
        
        # 第二层：Dasha激活
        dasha_activation = self._analyze_career_dasha()
        
        # 第三层：过境触发
        transit_trigger = self._analyze_career_transit()
        
        probability = self._calculate_career_probability(
            static_factors, dasha_activation, transit_trigger
        )
        
        risk_level = self._assess_career_risk(static_factors)
        timing = self._predict_career_timing(dasha_activation, transit_trigger)
        
        key_factors = []
        if static_factors.get('10th_house_strong'):
            key_factors.append("10宫强")
        if static_factors.get('career_yoga'):
            key_factors.append("职业Yoga")
        
        recommendations = []
        if risk_level == RiskLevel.LOW:
            recommendations.append("职业前景良好")
        else:
            recommendations.append("需要努力和规划")
        
        return Prediction(
            event_type=EventType.CAREER,
            description="职业预测",
            probability=probability,
            risk_level=risk_level,
            timing=timing,
            key_factors=key_factors,
            recommendations=recommendations
        )
    
    def predict_wealth(self) -> Optional[Prediction]:
        """财富预测"""
        static_factors = self._analyze_wealth_static()
        dasha_activation = self._analyze_wealth_dasha()
        transit_trigger = self._analyze_wealth_transit()
        
        probability = self._calculate_wealth_probability(
            static_factors, dasha_activation, transit_trigger
        )
        
        risk_level = self._assess_wealth_risk(static_factors)
        timing = self._predict_wealth_timing(dasha_activation, transit_trigger)
        
        key_factors = []
        if static_factors.get('2nd_house_strong'):
            key_factors.append("2宫强")
        if static_factors.get('dhana_yoga'):
            key_factors.append("财富Yoga")
        
        recommendations = ["注意财务管理"]
        
        return Prediction(
            event_type=EventType.WEALTH,
            description="财富预测",
            probability=probability,
            risk_level=risk_level,
            timing=timing,
            key_factors=key_factors,
            recommendations=recommendations
        )
    
    def predict_health(self) -> Optional[Prediction]:
        """健康预测"""
        static_factors = self._analyze_health_static()
        dasha_activation = self._analyze_health_dasha()
        transit_trigger = self._analyze_health_transit()
        
        probability = self._calculate_health_probability(
            static_factors, dasha_activation, transit_trigger
        )
        
        risk_level = self._assess_health_risk(static_factors)
        timing = self._predict_health_timing(dasha_activation, transit_trigger)
        
        key_factors = []
        if static_factors.get('6th_house_afflicted'):
            key_factors.append("6宫受克")
        if static_factors.get('moon_weak'):
            key_factors.append("月亮弱势")
        
        recommendations = []
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            recommendations.append("建议定期体检")
            recommendations.append("注意健康生活方式")
        
        return Prediction(
            event_type=EventType.HEALTH,
            description="健康预测",
            probability=probability,
            risk_level=risk_level,
            timing=timing,
            key_factors=key_factors,
            recommendations=recommendations
        )
    
    # ===== 静态分析方法 =====
    
    def _analyze_marriage_static(self) -> Dict:
        """婚姻静态分析"""
        factors = {}
        
        if 'planets' in self.chart:
            # 检查7宫
            factors['7th_house_afflicted'] = False  # 简化版
            factors['venus_weak'] = False
            
            # 检查金星
            venus = self.chart['planets'].get('Venus')
            if venus and venus.get('status') == 'debilitated':
                factors['venus_weak'] = True
            
            # 检查婚姻Yoga
            factors['marriage_yoga'] = False
        
        return factors
    
    def _analyze_career_static(self) -> Dict:
        """职业静态分析"""
        factors = {}
        
        if 'planets' in self.chart:
            factors['10th_house_strong'] = False
            factors['career_yoga'] = False
            
            # 检查10宫
            for planet, data in self.chart['planets'].items():
                if data.get('house') == 10 and data.get('status') in ['exalted', 'own_sign']:
                    factors['10th_house_strong'] = True
        
        return factors
    
    def _analyze_wealth_static(self) -> Dict:
        """财富静态分析"""
        factors = {}
        
        if 'planets' in self.chart:
            factors['2nd_house_strong'] = False
            factors['dhana_yoga'] = False
            
            # 检查2宫
            for planet, data in self.chart['planets'].items():
                if data.get('house') == 2 and planet in ['Jupiter', 'Venus']:
                    factors['2nd_house_strong'] = True
        
        return factors
    
    def _analyze_health_static(self) -> Dict:
        """健康静态分析"""
        factors = {}
        
        if 'planets' in self.chart:
            factors['6th_house_afflicted'] = False
            factors['moon_weak'] = False
            
            # 检查月亮
            moon = self.chart['planets'].get('Moon')
            if moon and moon.get('status') == 'debilitated':
                factors['moon_weak'] = True
        
        return factors
    
    # ===== Dasha激活分析 =====
    
    def _analyze_marriage_dasha(self) -> Dict:
        """婚姻Dasha激活分析"""
        if not self.dasha:
            return {'status': '缺失Dasha信息'}
        
        # 检查当前Dasha主星是否掌管7宫或金星
        return {'activated': False}
    
    def _analyze_career_dasha(self) -> Dict:
        """职业Dasha激活分析"""
        if not self.dasha:
            return {'status': '缺失Dasha信息'}
        
        return {'activated': False}
    
    def _analyze_wealth_dasha(self) -> Dict:
        """财富Dasha激活分析"""
        if not self.dasha:
            return {'status': '缺失Dasha信息'}
        
        return {'activated': False}
    
    def _analyze_health_dasha(self) -> Dict:
        """健康Dasha激活分析"""
        if not self.dasha:
            return {'status': '缺失Dasha信息'}
        
        return {'activated': False}
    
    # ===== 过境触发分析 =====
    
    def _analyze_marriage_transit(self) -> Dict:
        """婚姻过境触发分析"""
        if not self.transit:
            return {'status': '缺失过境信息'}
        
        # 检查木星是否过境7宫
        return {'triggered': False}
    
    def _analyze_career_transit(self) -> Dict:
        """职业过境触发分析"""
        if not self.transit:
            return {'status': '缺失过境信息'}
        
        return {'triggered': False}
    
    def _analyze_wealth_transit(self) -> Dict:
        """财富过境触发分析"""
        if not self.transit:
            return {'status': '缺失过境信息'}
        
        return {'triggered': False}
    
    def _analyze_health_transit(self) -> Dict:
        """健康过境触发分析"""
        if not self.transit:
            return {'status': '缺失过境信息'}
        
        return {'triggered': False}
    
    # ===== 概率计算 =====
    
    def _calculate_marriage_probability(self, static: Dict, dasha: Dict, transit: Dict) -> float:
        """计算婚姻概率"""
        base_prob = 50.0
        
        if static.get('marriage_yoga'):
            base_prob += 20
        if static.get('7th_house_afflicted'):
            base_prob -= 15
        if static.get('venus_weak'):
            base_prob -= 10
        
        if dasha.get('activated'):
            base_prob += 15
        
        if transit.get('triggered'):
            base_prob += 10
        
        return min(100, max(0, base_prob))
    
    def _calculate_career_probability(self, static: Dict, dasha: Dict, transit: Dict) -> float:
        """计算职业概率"""
        base_prob = 50.0
        
        if static.get('10th_house_strong'):
            base_prob += 20
        if static.get('career_yoga'):
            base_prob += 15
        
        if dasha.get('activated'):
            base_prob += 15
        
        if transit.get('triggered'):
            base_prob += 10
        
        return min(100, max(0, base_prob))
    
    def _calculate_wealth_probability(self, static: Dict, dasha: Dict, transit: Dict) -> float:
        """计算财富概率"""
        base_prob = 50.0
        
        if static.get('2nd_house_strong'):
            base_prob += 20
        if static.get('dhana_yoga'):
            base_prob += 15
        
        if dasha.get('activated'):
            base_prob += 15
        
        if transit.get('triggered'):
            base_prob += 10
        
        return min(100, max(0, base_prob))
    
    def _calculate_health_probability(self, static: Dict, dasha: Dict, transit: Dict) -> float:
        """计算健康概率"""
        base_prob = 70.0  # 基础健康概率
        
        if static.get('6th_house_afflicted'):
            base_prob -= 20
        if static.get('moon_weak'):
            base_prob -= 15
        
        if dasha.get('activated'):
            base_prob -= 10
        
        if transit.get('triggered'):
            base_prob -= 5
        
        return min(100, max(0, base_prob))
    
    # ===== 风险评估 =====
    
    def _assess_marriage_risk(self, static: Dict) -> RiskLevel:
        """评估婚姻风险"""
        if static.get('7th_house_afflicted') and static.get('venus_weak'):
            return RiskLevel.HIGH
        elif static.get('7th_house_afflicted') or static.get('venus_weak'):
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _assess_career_risk(self, static: Dict) -> RiskLevel:
        """评估职业风险"""
        if static.get('10th_house_strong'):
            return RiskLevel.LOW
        else:
            return RiskLevel.MEDIUM
    
    def _assess_wealth_risk(self, static: Dict) -> RiskLevel:
        """评估财富风险"""
        if static.get('2nd_house_strong'):
            return RiskLevel.LOW
        else:
            return RiskLevel.MEDIUM
    
    def _assess_health_risk(self, static: Dict) -> RiskLevel:
        """评估健康风险"""
        if static.get('6th_house_afflicted') and static.get('moon_weak'):
            return RiskLevel.HIGH
        elif static.get('6th_house_afflicted') or static.get('moon_weak'):
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    # ===== 时间预测 =====
    
    def _predict_marriage_timing(self, dasha: Dict, transit: Dict) -> Optional[str]:
        """预测婚姻时间"""
        if dasha.get('activated') and transit.get('triggered'):
            return "近期可能"
        elif dasha.get('activated'):
            return "等待过境触发"
        else:
            return "需要等待Dasha激活"
    
    def _predict_career_timing(self, dasha: Dict, transit: Dict) -> Optional[str]:
        """预测职业时间"""
        if dasha.get('activated'):
            return "当前阶段"
        else:
            return "需要等待Dasha激活"
    
    def _predict_wealth_timing(self, dasha: Dict, transit: Dict) -> Optional[str]:
        """预测财富时间"""
        if dasha.get('activated'):
            return "当前阶段"
        else:
            return "需要等待Dasha激活"
    
    def _predict_health_timing(self, dasha: Dict, transit: Dict) -> Optional[str]:
        """预测健康时间"""
        if dasha.get('activated'):
            return "当前需要注意"
        else:
            return "总体稳定"
    
    def generate_report(self) -> str:
        """生成预测报告"""
        if not self.predictions:
            self.predict_all_events()
        
        lines = []
        lines.append("=" * 60)
        lines.append("事件预测报告")
        lines.append("=" * 60)
        lines.append("")
        
        for pred in self.predictions:
            lines.append(f"【{pred.event_type.value}】")
            lines.append(f"  概率：{pred.probability:.1f}%")
            lines.append(f"  风险等级：{pred.risk_level.value}")
            if pred.timing:
                lines.append(f"  时间预测：{pred.timing}")
            lines.append("  关键因素：")
            for factor in pred.key_factors:
                lines.append(f"    - {factor}")
            lines.append("  建议：")
            for rec in pred.recommendations:
                lines.append(f"    - {rec}")
            lines.append("")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # 测试示例
    test_chart = {
        'planets': {
            'Sun': {'house': 9, 'sign': 'Aries', 'status': 'exalted'},
            'Moon': {'house': 1, 'sign': 'Leo', 'status': 'own_sign'},
            'Mars': {'house': 1, 'sign': 'Aries', 'status': 'exalted'},
            'Mercury': {'house': 9, 'sign': 'Aries', 'status': ''},
            'Jupiter': {'house': 1, 'sign': 'Sagittarius', 'status': 'own_sign'},
            'Venus': {'house': 8, 'sign': 'Pisces', 'status': 'exalted'},
            'Saturn': {'house': 7, 'sign': 'Aquarius', 'status': 'own_sign'},
        }
    }
    
    model = EventPredictionModel(test_chart)
    predictions = model.predict_all_events()
    print(model.generate_report())
