"""
展示如何执行策略回测。
"""
from vnpy.trader.app.ctaStrategy import BacktestingEngine
import pandas as pd
from vnpy.trader.utils import htmlplot
import json
import os
from datetime import datetime
from doubleMaIfStrategy import DoubleMaStrategy

# 
if __name__ == '__main__':
    # 创建回测引擎
    engine = BacktestingEngine()
    # 注意数据库端口
    engine.setDB_URI("mongodb://192.168.0.104:27017")
    # engine.setDB_URI("mongodb://localhost:27017")

    # Bar回测
    engine.setBacktestingMode(engine.BAR_MODE)
    # 注意数据库的名称
    engine.setDatabase('VnTrader_1Min_Db_contest')
    # engine.setDatabase('VnTrader_1Min_Db')


    # 设置回测用的数据起始日期
    engine.setDataRange(datetime(2014,3,1), datetime(2019,7,20), datetime(2014,1, 1))
    # 设置产品相关参数
    engine.setCapital(1000000)  # 设置起始资金，默认值是1,000,000
    contracts = [{
                    "symbol":"IF88:CTP",
                    "size" : 1, # 每点价值
                    "priceTick" : 0.01, # 最小价格变动
                    "rate" : 5/10000, # 单边手续费
                    "slippage" : 0.5 # 滑价
                    },] 

    engine.setContracts(contracts)
    engine.setLog(True, "./logIF88")
    # 获取当前绝对路径
    path = os.path.split(os.path.realpath(__file__))[0]
    with open(path+"//CTA_setting.json") as f:
        setting = json.load(f)[0]

    # Bar回测
    engine.initStrategy(DoubleMaStrategy, setting)
    
    # 开始跑回测
    engine.runBacktesting()
    
    # 显示回测结果
    engine.showBacktestingResult()
    engine.showDailyResult()
    
    ### 画图分析
    chartLog = pd.DataFrame(engine.strategy.chartLog).set_index('datetime')
    # print(chartLog)
    mp = htmlplot.getXMultiPlot(engine, freq="15m")
    mp.addLine(line=chartLog[['envMa', 'fastMa', 'slowMa']].reset_index(), colors={"envMa": "green","fastMa": "red",'slowMa':'blue'}, pos=0)
    mp.resample()
    mp.show()