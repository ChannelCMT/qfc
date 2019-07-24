from vnpy.trader.utils import optimize
from doubleMaIfStrategy import DoubleMaStrategy
from datetime import datetime
import os
import json

def setConfig(root=None):
    # 设置策略类
    optimize.strategyClass = DoubleMaStrategy
    # 设置缓存路径，如果不设置则不会缓存优化结果。
    optimize.root = root
    # 设置引擎参数
    optimize.engineSetting = {
                                'dbURI': "mongodb://192.168.0.104:27017",
                                "bardbName": "VnTrader_1Min_Db_contest",
                                "timeRange": {
                                    "tradeStart": datetime(2014,6,1),
                                    "tradeEnd": datetime(2016,6,1),
                                    "historyStart": datetime(2014,3,1),
                                },
                                "contract":[{
                                            "slippage": 0.5,
                                            "rate": 0.0005,
                                            }]
                             }
    # 设置策略固定参数
    optimize.globalSetting = {
        "symbolList": ["IF88:CTP"],
        # "barPeriod": 100,
    }
    # 设置策略优化参数
    optimize.paramsSetting = {
            "fastPeriod": range(5,21,5),
            "slowPeriod": range(30,81,20)
    }
    path = os.path.split(os.path.realpath(__file__))[0]
    with open(path+"//CTA_setting.json") as f:
        globalSetting = json.load(f)[0]
    optimize.globalSetting = globalSetting
    optimize.initOpt()

# 并行优化 无缓存
def runSimpleParallel():
    start = datetime.now()
    print("run simple | start: %s -------------------------------------------" % start)
    setConfig()
    # optimize.runParallel() 并行优化，返回回测结果
    report = optimize.runParallel()
    print(report)
    report.sort_values(by = 'sharpeRatio', ascending=False, inplace=True)
    # 将结果保存成csv
    report.to_csv('opt_IF88.csv')    
    end = datetime.now()
    print("run simple | end: %s | expire: %s -----------------------------" % (end, end-start))

def main():
    runSimpleParallel()

if __name__ == '__main__':
    main()
