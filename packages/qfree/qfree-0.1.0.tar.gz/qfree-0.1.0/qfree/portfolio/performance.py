"""指数分类对比"""

import pandas as pd

import empyrical
from empyrical.periods import ANNUALIZATION_FACTORS


YEAR_RISKFREE = 0.027  # 年化无风险利率


def calculate_returns_performance(returns: pd.DataFrame) -> dict:
    """统计收益率表现"""
    try:
        if returns is not None and len(returns) > 1:
            # 统计日期索引中间隔天数频率最高的值作为收益率频率
            returns = returns.sort_index()
            dts = (returns.index[1:] - returns.index[:-1]).days
            diff_days = dts.value_counts().index[0]  # days
            if diff_days == 1:
                period = empyrical.DAILY
            elif diff_days == 7:
                period = empyrical.WEEKLY
            else:
                raise ValueError("Unknown period")

            returns = returns.iloc[:, 0]

            # 年化收益率
            annual_return = empyrical.annual_return(returns, period)
            # print("annual_return:\n", annual_return)

            # 年化波动率
            annual_volatility = empyrical.annual_volatility(returns, period)
            # print("annual_volatility:\n", annual_volatility)

            # 最大回撤
            max_drawdown = empyrical.max_drawdown(returns)
            # print("max_drawdown:\n", max_drawdown)

            # 夏普比率
            risk_free = (1 + YEAR_RISKFREE) ** (1 / ANNUALIZATION_FACTORS[period]) - 1
            sharpe = empyrical.sharpe_ratio(returns, risk_free, period)
            # print("sharpe:\n", sharpe)

            # 肥尾风险
            fat_risk = abs(max_drawdown / annual_volatility)

            return {
                "夏普比率": float(round(sharpe, 4)),
                "年化收益率": float(round(annual_return, 4)),
                "年化波动率": float(round(annual_volatility, 4)),
                "最大回撤": float(round(max_drawdown, 4)),
                "肥尾风险": float(round(fat_risk, 4)),
            }
    except Exception as e:
        print("calculate performance error:", e)

    return None


def calculate_equity_performance(equity: pd.DataFrame) -> dict:
    """统计收益曲线表现"""
    # 计算每日收益率
    returns = equity.pct_change().dropna()
    return calculate_returns_performance(returns)
