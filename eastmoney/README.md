# East Money Skill (OpenClaw)

基于 AkShare (东方财富接口) 的股票数据查询和分析工具，支持 A 股实时行情、K 线、基本面及技术指标分析。

## 目录结构

```
eastmoney/
├── em.py         # 核心脚本 (支持 python em.py 直接运行)
├── SKILL.md      # Skill 定义文件 (OpenClaw 规范)
├── README.md     # 说明文档
└── requirements.txt
```

## 功能特性

- **Price**: 实时股价查询
- **Quote**: 详细盘口数据 (五档、量比、换手等)
- **History**: 历史 K 线数据 (日/周/月)
- **Fundamentals**: 基本面指标 (PE, PB, 市值等)
- **Analyze**: 技术面分析 (MA, RSI, MACD, 趋势评分)
- **Search**: 股票代码模糊搜索

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行脚本

```bash
# 查询实时股价
python em.py price 600519

# 技术面分析
python em.py analyze 603993
```

## 命令详解

### Analyze (技术分析)
```bash
python em.py analyze <symbol>
```
输出包含：
- 趋势信号 (MA20/MA60)
- RSI (相对强弱指标)
- MACD (平滑异同移动平均线)
- 综合买卖建议 (BUY/SELL/HOLD)

### Price (实时价格)
```bash
python em.py price <symbol>
```

### Search (搜索)
```bash
python em.py search "股票名称"
```

## 贡献

欢迎提交 PR 或 Issue！
