---
name: eastmoney-finance
description: 获取中国 A 股、港股、美股等实时行情和历史数据，基于 AkShare (东方财富接口)。
---

# East Money CLI (based on AkShare)

A Python CLI for fetching stock data from East Money (东方财富网) using AkShare.

## Usage

```bash
python .trae/skills/eastmoney/em.py <command> [symbol] [options]
```

## Commands

### Price (Real-time Spot)
```bash
python .trae/skills/eastmoney/em.py price 600519
# Shorthand:
python .trae/skills/eastmoney/em.py 600519
```
Displays: Latest price, change, volume, turnover for A-share stocks.

### Quote (Detailed Info)
```bash
python .trae/skills/eastmoney/em.py quote 000001
```
Displays: Detailed quote information including open, high, low, pe, market cap.

### History (K-Line)
```bash
python .trae/skills/eastmoney/em.py history 600519 daily
python .trae/skills/eastmoney/em.py history 00700 weekly
```
Supported periods: daily, weekly, monthly.

### Fundamentals (Financial Indicators)
```bash
python .trae/skills/eastmoney/em.py fundamentals 600519
```
Shows: Key financial indicators (PE, PB, ROE, etc.)

### Analyze (Technical Indicators & Decision Support)
```bash
python .trae/skills/eastmoney/em.py analyze 600519
```
Displays: MA5/20/60, RSI, MACD signals, Buy/Sell/Hold recommendation score, **and recent news headlines**.

### Search
```bash
python .trae/skills/eastmoney/em.py search "茅台"
python .trae/skills/eastmoney/em.py search "腾讯"
```
Search for stock codes by name.

### News
```bash
python .trae/skills/eastmoney/em.py news 600519
```
Fetch recent news for a stock.

## Symbol Format

- A-share: 6-digit code (e.g., `600519`, `000001`)
- AkShare usually auto-detects market for A-shares.
