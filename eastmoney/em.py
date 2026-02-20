#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "akshare",
#     "rich",
#     "pandas",
# ]
# ///
import sys
import argparse
import akshare as ak
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from datetime import datetime

console = Console()

def get_symbol(args_list):
    """
    Extract symbol from arguments. Handles both positional and command-based arguments.
    """
    if not args_list:
        return None
    commands = ['price', 'quote', 'history', 'fundamentals', 'search', 'analyze', 'news']
    if args_list[0] in commands:
        if len(args_list) > 1:
            return args_list[1]
        return None
    return args_list[0]

def calculate_technical_indicators(df):
    """
    Calculate basic technical indicators: MA5, MA20, RSI(14), MACD
    """
    # Ensure sorted by date ascending
    df = df.sort_values('日期').reset_index(drop=True)
    close = df['收盘']
    
    # MA
    df['MA5'] = close.rolling(window=5).mean()
    df['MA20'] = close.rolling(window=20).mean()
    df['MA60'] = close.rolling(window=60).mean()
    
    # RSI (14) - Wilder's Smoothing
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).ewm(alpha=1/14, adjust=False).mean()
    loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/14, adjust=False).mean()
    rs = gain / loss
    df['RSI_14'] = 100 - (100 / (1 + rs))
    
    # MACD (12, 26, 9)
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    df['DIF'] = ema12 - ema26
    df['DEA'] = df['DIF'].ewm(span=9, adjust=False).mean()
    df['MACD'] = 2 * (df['DIF'] - df['DEA'])
    
    return df

def cmd_analyze(symbol):
    """
    Calculate basic technical indicators: MA5, MA20, RSI(14), MACD
    """
    # Ensure sorted by date ascending
    df = df.sort_values('日期').reset_index(drop=True)
    close = df['收盘']
    
    # MA
    df['MA5'] = close.rolling(window=5).mean()
    df['MA20'] = close.rolling(window=20).mean()
    df['MA60'] = close.rolling(window=60).mean()
    
    # RSI (14) - Wilder's Smoothing
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).ewm(alpha=1/14, adjust=False).mean()
    loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/14, adjust=False).mean()
    rs = gain / loss
    df['RSI_14'] = 100 - (100 / (1 + rs))
    
    # MACD (12, 26, 9)
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    df['DIF'] = ema12 - ema26
    df['DEA'] = df['DIF'].ewm(span=9, adjust=False).mean()
    df['MACD'] = 2 * (df['DIF'] - df['DEA'])
    
    return df

def cmd_analyze(symbol):
    try:
        current_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - pd.DateOffset(months=6)).strftime("%Y%m%d")
        
        rprint(f"Fetching history for {symbol} to analyze...")
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, end_date=current_date, adjust="qfq")
        
        if df.empty:
            rprint(f"[red]No history found for {symbol}.[/red]")
            return
            
        df = calculate_technical_indicators(df)
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # Display Analysis
        console.rule(f"[bold blue]Technical Analysis for {symbol} ({latest['日期']})[/bold blue]")
        
        # 1. Price Trend
        price = latest['收盘']
        ma5 = latest['MA5']
        ma20 = latest['MA20']
        ma60 = latest['MA60']
        
        trend_color = "green" if price > ma20 else "red"
        trend_str = "BULLISH" if price > ma20 else "BEARISH"
        
        table = Table(title="Trend Indicators")
        table.add_column("Indicator")
        table.add_column("Value")
        table.add_column("Signal")
        
        table.add_row("Close Price", f"{price:.2f}", f"[{trend_color}]{trend_str}[/{trend_color}] (vs MA20)")
        table.add_row("MA5", f"{ma5:.2f}", "Support/Resistance (Short)")
        table.add_row("MA20", f"{ma20:.2f}", "Support/Resistance (Mid)")
        table.add_row("MA60", f"{ma60:.2f}", "Support/Resistance (Long)")
        
        console.print(table)
        
        # 2. Momentum (RSI)
        rsi = latest['RSI_14']
        rsi_signal = "NEUTRAL"
        rsi_color = "white"
        if rsi > 70:
            rsi_signal = "OVERBOUGHT (Risk of Pullback)"
            rsi_color = "red"
        elif rsi < 30:
            rsi_signal = "OVERSOLD (Potential Bounce)"
            rsi_color = "green"
            
        console.print(f"\n[bold]RSI (14):[/bold] {rsi:.2f} -> [{rsi_color}]{rsi_signal}[/{rsi_color}]")
        
        # 3. MACD
        dif = latest['DIF']
        dea = latest['DEA']
        macd = latest['MACD']
        
        macd_signal = "NEUTRAL"
        macd_color = "white"
        
        # Golden Cross check
        if dif > dea and prev['DIF'] <= prev['DEA']:
             macd_signal = "GOLDEN CROSS (Buy Signal)"
             macd_color = "green"
        elif dif < dea and prev['DIF'] >= prev['DEA']:
             macd_signal = "DEATH CROSS (Sell Signal)"
             macd_color = "red"
        elif dif > dea:
             macd_signal = "BULLISH MOMENTUM"
             macd_color = "green"
        else:
             macd_signal = "BEARISH MOMENTUM"
             macd_color = "red"
             
        console.print(f"[bold]MACD (12,26,9):[/bold] DIF={dif:.2f}, DEA={dea:.2f}, MACD={macd:.2f}")
        console.print(f"Signal: [{macd_color}]{macd_signal}[/{macd_color}]")
        
        # Summary
        console.rule("[bold]Summary[/bold]")
        score = 0
        if price > ma20: score += 1
        if price > ma60: score += 1
        if rsi < 30: score += 1 # Oversold is good for buy
        if rsi > 70: score -= 1 # Overbought is bad for buy
        if dif > dea: score += 1
        
        recommendation = "HOLD"
        rec_color = "yellow"
        if score >= 3:
            recommendation = "BUY / ACCUMULATE"
            rec_color = "green"
        elif score <= 0:
            recommendation = "SELL / AVOID"
            rec_color = "red"
            
        console.print(f"Technical Score: {score}/4 (Simple Model)")
        console.print(f"Recommendation: [bold {rec_color}]{recommendation}[/bold {rec_color}]")
        console.print("[dim]Disclaimer: This is for reference only. Not financial advice.[/dim]")

    except Exception as e:
        console.print(f"[red]Error analyzing: {e}[/red]")

    # Fetch and show news
    cmd_news(symbol, limit=3)

def format_number(num):
    if num is None:
        return "N/A"
    try:
        num = float(num)
        if abs(num) >= 1e12:
            return f"{num/1e12:.2f}万亿"
        if abs(num) >= 1e8:
            return f"{num/1e8:.2f}亿"
        if abs(num) >= 1e4:
            return f"{num/1e4:.2f}万"
        return f"{num:.2f}"
    except:
        return str(num)

def cmd_price(symbol):
    """
    Display real-time price using ak.stock_zh_a_spot_em() filtering.
    Note: fetching all spots is slow (~2-3s), but robust for searching by code.
    For optimization, we could use individual stock APIs if available.
    """
    try:
        # Check if symbol is 6 digits
        if not symbol.isdigit() or len(symbol) != 6:
            rprint(f"[yellow]Assuming '{symbol}' is a name or requires search...[/yellow]")
            cmd_search(symbol)
            return

        df = ak.stock_zh_a_spot_em()
        row = df[df['代码'] == symbol]
        
        if row.empty:
            rprint(f"[red]Symbol {symbol} not found in A-share list.[/red]")
            return
            
        row = row.iloc[0]
        price = row['最新价']
        change_pct = row['涨跌幅']
        change_amt = row['涨跌额']
        name = row['名称']
        
        color = "red" if change_pct >= 0 else "green" # A-share: Red is up, Green is down
        
        rprint(f"[bold]{name} ({symbol})[/bold]: {price} [{color}]{change_amt:+.2f} ({change_pct:+.2f}%)[/{color}]")
        rprint(f"Volume: {format_number(row['成交量'])}  Turnover: {format_number(row['成交额'])}")
        
    except Exception as e:
        console.print(f"[red]Error fetching price: {e}[/red]")

def cmd_quote(symbol):
    try:
        df = ak.stock_zh_a_spot_em()
        row = df[df['代码'] == symbol]
        
        if row.empty:
            rprint(f"[red]Symbol {symbol} not found.[/red]")
            return
            
        row = row.iloc[0]
        
        table = Table(title=f"Quote for {row['名称']} ({symbol})")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="magenta")
        
        fields = [
            ('Latest Price', '最新价'),
            ('Change %', '涨跌幅'),
            ('Change Amount', '涨跌额'),
            ('Open', '今开'),
            ('High', '最高'),
            ('Low', '最低'),
            ('Previous Close', '昨收'),
            ('Volume', '成交量'),
            ('Turnover', '成交额'),
            ('PE (Dynamic)', '市盈率-动态'),
            ('PB', '市净率'),
            ('Market Cap', '总市值'),
            ('Circulating Cap', '流通市值'),
        ]
        
        for label, key in fields:
            val = row.get(key)
            if key in ['成交量', '成交额', '总市值', '流通市值']:
                val = format_number(val)
            table.add_row(label, str(val))
            
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error fetching quote: {e}[/red]")

def cmd_history(symbol, period="daily"):
    """
    period: daily, weekly, monthly
    """
    try:
        # Map period to AkShare args if needed. default is daily.
        start_date = "20240101" # Default to recent year or adjust logic
        current_date = datetime.now().strftime("%Y%m%d")
        
        # Adjust start date based on period roughly? 
        # For CLI simplicity, let's just fetch recent data (last 365 days).
        
        df = ak.stock_zh_a_hist(symbol=symbol, period=period, start_date="20230101", end_date=current_date, adjust="qfq")
        
        if df.empty:
            rprint(f"[red]No history found for {symbol}.[/red]")
            return

        table = Table(title=f"History for {symbol} ({period})")
        table.add_column("Date")
        table.add_column("Open")
        table.add_column("Close")
        table.add_column("High")
        table.add_column("Low")
        table.add_column("Volume")
        table.add_column("Change %")
        
        # Show last 20 rows
        subset = df.tail(20)
        for _, row in subset.iterrows():
            table.add_row(
                str(row['日期']),
                f"{row['开盘']:.2f}",
                f"{row['收盘']:.2f}",
                f"{row['最高']:.2f}",
                f"{row['最低']:.2f}",
                format_number(row['成交量']),
                f"{row['涨跌幅']:.2f}"
            )
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error fetching history: {e}[/red]")

def cmd_fundamentals(symbol):
    try:
        # Use abstract or daily indicators
        # stock_a_indicator_lg (legu) or similar
        # Let's use stock_zh_a_spot_em extra columns for basic fundamentals first as it's reliable
        # Or fetch specific financial reports which is complex.
        # Let's stick to spot data extended info for now.
        
        df = ak.stock_zh_a_spot_em()
        row = df[df['代码'] == symbol]
        
        if row.empty:
            rprint(f"[red]Symbol {symbol} not found.[/red]")
            return
        
        row = row.iloc[0]
        
        table = Table(title=f"Fundamentals (Snapshot) for {row['名称']} ({symbol})")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        metrics = [
            ('PE (Dynamic)', '市盈率-动态'),
            ('PB', '市净率'),
            ('Turnover Rate', '换手率'),
            ('Volume Ratio', '量比'),
            ('Market Cap', '总市值'),
            ('Circulating Cap', '流通市值'),
            ('YTD Change', '涨速'), # Not exactly YTD but available
            ('5-min Change', '5分钟涨跌'),
            ('60-day Change', '60日涨跌幅'),
            ('YTD Change %', '年初至今涨跌幅')
        ]
        
        for label, key in metrics:
            val = row.get(key)
            if '市值' in key:
                 val = format_number(val)
            table.add_row(label, str(val))
            
        console.print(table)

    except Exception as e:
        console.print(f"[red]Error fetching fundamentals: {e}[/red]")

def cmd_search(query):
    try:
        rprint(f"Searching for '{query}' in A-share list...")
        df = ak.stock_zh_a_spot_em()
        # Search in Name or Code
        # Ensure Code is string
        df['代码'] = df['代码'].astype(str)
        
        mask = df['名称'].str.contains(query) | df['代码'].str.contains(query)
        results = df[mask]
        
        if results.empty:
            rprint(f"[red]No results found for '{query}'.[/red]")
            return
            
        table = Table(title=f"Search Results for '{query}'")
        table.add_column("Code")
        table.add_column("Name")
        table.add_column("Latest Price")
        table.add_column("Change %")
        
        # Limit to top 10
        for _, row in results.head(10).iterrows():
            change_pct = row['涨跌幅']
            color = "red" if change_pct >= 0 else "green"
            table.add_row(
                row['代码'],
                row['名称'],
                str(row['最新价']),
                f"[{color}]{change_pct:+.2f}%[/{color}]"
            )
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error searching: {e}[/red]")

def cmd_news(symbol, limit=5):
    """
    Fetch and display recent news for the stock symbol.
    """
    try:
        rprint(f"Fetching news for {symbol}...")
        news_df = ak.stock_news_em(symbol=symbol)
        
        if news_df.empty:
            rprint(f"[yellow]No news found for {symbol}.[/yellow]")
            return
            
        # Select top N news
        recent_news = news_df.head(limit)
        
        table = Table(title=f"Recent News for {symbol}")
        table.add_column("Date", style="cyan")
        table.add_column("Title", style="white")
        # table.add_column("Link", style="blue") # Link might be too long
        
        for _, row in recent_news.iterrows():
            # stock_news_em columns: 关键词, 新闻标题, 新闻内容, 发布时间, 文章来源, 新闻链接
            date = row.get('发布时间', 'N/A')
            title = row.get('新闻标题', 'N/A')
            # link = row.get('新闻链接', '')
            
            # Simple keyword highlighting
            title_colored = title
            if any(x in title for x in ['涨', '利好', '增', '高', '红']):
                title_colored = f"[green]{title}[/green]"
            elif any(x in title for x in ['跌', '利空', '减', '低', '亏', '查']):
                title_colored = f"[red]{title}[/red]"
                
            table.add_row(str(date), title_colored)
            
        console.print(table)
        return recent_news # Return for potential use in analyze
        
    except Exception as e:
        console.print(f"[red]Error fetching news: {e}[/red]")
        return pd.DataFrame()

def main():
    if len(sys.argv) < 2:
        console.print("[red]Usage: em.py <command> [symbol][/red]")
        sys.exit(1)
        
    command = sys.argv[1]
    
    # Handle shorthand: if command is likely a symbol (6 digits), treat as price check
    if command.isdigit() and len(command) == 6:
        cmd_price(command)
        return
        
    known_commands = ['price', 'quote', 'history', 'fundamentals', 'search', 'analyze']
    
    if command not in known_commands:
        console.print(f"[red]Unknown command: {command}[/red]")
        return

    if len(sys.argv) < 3:
         console.print(f"[red]Missing argument for command {command}[/red]")
         sys.exit(1)
         
    arg = sys.argv[2]
    
    if command == 'price':
        cmd_price(arg)
    elif command == 'quote':
        cmd_quote(arg)
    elif command == 'history':
        period = sys.argv[3] if len(sys.argv) > 3 else "daily"
        cmd_history(arg, period)
    elif command == 'fundamentals':
        cmd_fundamentals(arg)
    elif command == 'search':
        cmd_search(arg)
    elif command == 'analyze':
        cmd_analyze(arg)
    elif command == 'news':
        cmd_news(arg)

if __name__ == "__main__":
    main()
