# -*- coding: utf-8 -*-

"""
模块名称：价格验证工具.py
模块功能：验证价格合理性，计算折扣率

职责：
- 验证基础包价格合理性
- 验证扩展包价格合理性
- 计算折扣率和日均价格
- 生成价格分析报告

使用方式：
- python 价格验证工具.py
"""

from typing import List, Dict, Tuple


class PriceValidator:
    """价格验证工具"""
    
    def __init__(self, daily_price: float = 3.0):
        """
        初始化价格验证工具
        
        参数:
            daily_price: 日卡价格（基准价格）
        """
        self.daily_price = daily_price
        self.basic_packages = [
            ("日卡", 1, 3),
            ("周卡", 7, 18),
            ("月卡", 30, 50),
            ("季卡", 90, 120),
            ("年卡", 365, 300),
        ]
        self.extension_packages = [
            ("15次", 15, 20),
            ("30次", 30, 36),
            ("60次", 60, 66),
            ("120次", 120, 120),
            ("240次", 240, 216),
        ]
    
    def validate_basic_prices(self) -> List[Dict]:
        """
        验证基础包价格合理性
        
        返回:
            价格验证结果列表
        """
        results = []
        
        for name, days, price in self.basic_packages:
            base_price = self.daily_price * days
            discount = (1 - price / base_price) * 100 if base_price > 0 else 0
            daily_avg = price / days if days > 0 else 0
            
            result = {
                "套餐名称": name,
                "天数": days,
                "实际价格": price,
                "基准价格": round(base_price, 2),
                "折扣率": f"{discount:.1f}%",
                "日均价格": f"{daily_avg:.2f}元",
                "价格合理性": self._check_price_reasonable(discount, days),
            }
            results.append(result)
        
        return results
    
    def validate_extension_prices(self) -> List[Dict]:
        """
        验证扩展包价格合理性
        
        返回:
            价格验证结果列表
        """
        results = []
        
        base_unit_price = self.extension_packages[0][2] / self.extension_packages[0][1] if self.extension_packages else 0
        
        for name, times, price in self.extension_packages:
            unit_price = price / times if times > 0 else 0
            discount = (1 - unit_price / base_unit_price) * 100 if base_unit_price > 0 else 0
            
            result = {
                "套餐名称": name,
                "次数": times,
                "实际价格": price,
                "单次价格": f"{unit_price:.2f}元",
                "折扣率": f"{discount:.1f}%",
                "价格合理性": self._check_extension_price_reasonable(discount, times),
            }
            results.append(result)
        
        return results
    
    def _check_price_reasonable(self, discount: float, days: int) -> str:
        """
        检查价格是否合理
        
        参数:
            discount: 折扣率
            days: 天数
        
        返回:
            合理性评价
        """
        if days == 1:
            return "基准价格"
        
        if discount < 0:
            return "⚠️ 价格高于基准价格"
        elif discount < 10:
            return "✅ 折扣较小"
        elif discount < 30:
            return "✅ 折扣适中"
        elif discount < 50:
            return "✅ 折扣较大"
        elif discount < 70:
            return "✅ 折扣很大"
        else:
            return "⚠️ 折扣过大，请确认"
    
    def _check_extension_price_reasonable(self, discount: float, times: int) -> str:
        """
        检查扩展包价格是否合理
        
        参数:
            discount: 折扣率
            times: 次数
        
        返回:
            合理性评价
        """
        if times == 15:
            return "基准价格"
        
        if discount < 0:
            return "⚠️ 价格高于基准价格"
        elif discount < 10:
            return "✅ 折扣较小"
        elif discount < 20:
            return "✅ 折扣适中"
        elif discount < 30:
            return "✅ 折扣较大"
        else:
            return "⚠️ 折扣过大，请确认"
    
    def generate_report(self) -> str:
        """
        生成价格分析报告
        
        返回:
            格式化的报告文本
        """
        report = []
        report.append("=" * 60)
        report.append("价格验证报告")
        report.append("=" * 60)
        report.append("")
        
        report.append("【基础包价格分析】")
        report.append("-" * 60)
        report.append(f"{'套餐':<8} {'天数':<6} {'价格':<8} {'基准价':<10} {'折扣率':<10} {'日均':<10} {'评价'}")
        report.append("-" * 60)
        
        basic_results = self.validate_basic_prices()
        for result in basic_results:
            report.append(
                f"{result['套餐名称']:<8} "
                f"{result['天数']:<6} "
                f"{result['实际价格']:<8} "
                f"{result['基准价格']:<10} "
                f"{result['折扣率']:<10} "
                f"{result['日均价格']:<10} "
                f"{result['价格合理性']}"
            )
        
        report.append("")
        report.append("【扩展包价格分析】")
        report.append("-" * 60)
        report.append(f"{'套餐':<8} {'次数':<6} {'价格':<8} {'单次价':<10} {'折扣率':<10} {'评价'}")
        report.append("-" * 60)
        
        extension_results = self.validate_extension_prices()
        for result in extension_results:
            report.append(
                f"{result['套餐名称']:<8} "
                f"{result['次数']:<6} "
                f"{result['实际价格']:<8} "
                f"{result['单次价格']:<10} "
                f"{result['折扣率']:<10} "
                f"{result['价格合理性']}"
            )
        
        report.append("")
        report.append("=" * 60)
        report.append("价格验证完成")
        report.append("=" * 60)
        
        return "\n".join(report)


class PriceCalculator:
    """价格计算辅助工具"""
    
    def __init__(self, daily_price: float = 3.0):
        """
        初始化价格计算工具
        
        参数:
            daily_price: 日卡价格（基准价格）
        """
        self.daily_price = daily_price
    
    def calculate_package_price(self, days: int, discount_rate: float) -> Tuple[float, float]:
        """
        根据天数和折扣率计算套餐价格
        
        参数:
            days: 天数
            discount_rate: 折扣率（百分比，如14.3表示14.3%）
        
        返回:
            (套餐价格, 日均价格)
        """
        base_price = self.daily_price * days
        discounted_price = base_price * (1 - discount_rate / 100)
        daily_avg = discounted_price / days if days > 0 else 0
        
        return round(discounted_price, 2), round(daily_avg, 2)
    
    def suggest_discount_rate(self, days: int) -> float:
        """
        根据天数建议折扣率
        
        参数:
            days: 天数
        
        返回:
            建议的折扣率（百分比）
        """
        if days <= 1:
            return 0
        elif days <= 7:
            return 14.3
        elif days <= 30:
            return 44.4
        elif days <= 90:
            return 55.6
        else:
            return 72.6
    
    def generate_price_table(self, days_list: List[int] = None) -> str:
        """
        生成价格表
        
        参数:
            days_list: 天数列表，如果为None则使用默认值
        
        返回:
            格式化的价格表
        """
        if days_list is None:
            days_list = [1, 7, 30, 90, 365]
        
        table = []
        table.append("=" * 70)
        table.append(f"价格表（基准价格：{self.daily_price}元/天）")
        table.append("=" * 70)
        table.append(f"{'天数':<10} {'基准价格':<15} {'建议折扣':<15} {'建议价格':<15} {'日均价格'}")
        table.append("-" * 70)
        
        for days in days_list:
            base_price = self.daily_price * days
            discount = self.suggest_discount_rate(days)
            price, daily_avg = self.calculate_package_price(days, discount)
            
            table.append(
                f"{days:<10} "
                f"{base_price:<15.2f} "
                f"{discount:<15.1f}% "
                f"{price:<15.2f} "
                f"{daily_avg:.2f}元"
            )
        
        table.append("=" * 70)
        
        return "\n".join(table)


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("价格验证和计算工具")
    print("=" * 60)
    print()
    
    validator = PriceValidator(daily_price=3.0)
    print(validator.generate_report())
    
    print("\n")
    
    calculator = PriceCalculator(daily_price=3.0)
    print(calculator.generate_price_table())
    
    print("\n" + "=" * 60)
    print("使用说明：")
    print("1. PriceValidator: 验证价格合理性")
    print("2. PriceCalculator: 计算套餐价格")
    print("3. 修改 daily_price 参数可以调整基准价格")
    print("=" * 60)


if __name__ == "__main__":
    main()
