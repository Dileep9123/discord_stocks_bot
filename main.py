import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import discord
from discord.ext import commands
from dateutil.relativedelta import relativedelta
import random
import os
from dotenv import load_dotenv
from lists import compy, colors, periods, companies
import re

bot = commands.Bot(command_prefix="$")
client = discord.Client()
COLORS=colors
@client.event
async def on_ready():
    print(f"We logged in as {client.user}")

def company_period(company, period):
    i = 0
    for com in company:
        col = random.choice(colors)
        historical_data = yf.download(com, progress=False, period=period)
        print(historical_data,"great")
        plt.plot(historical_data['Close'], color=col, label=com)
        plt.xlabel('Datetime')
        plt.ylabel('closing price')
        plt.legend()
        i = i + 1
    plt.gcf().autofmt_xdate()
    plt.savefig('image.png')
    chart = discord.File('image.png', filename='image.png')
    plt.close()
    return chart

async def help_command(ctx):
    help_message = """
    **StockBot Help**
    To get stock information, use one of the following formats:

    1. To get stock prices for a specific period (e.g., 1 year), use:
       `$stock period company_code1 company_code2 ...`
       Example: `1yr MSFT AAPL`

    2. To get stock prices between specific dates, use:
       `$stock start_date end_date company_code1 company_code2 ...`
       Dates should be in the format 'yyyy-mm-dd'.
       Example: `2022-01-01 2022-12-31 MSFT AAPL`

    3. To get stock prices for the past years, use:
       `$stock years company_code1 company_code2 ...`
       Example: `5yr MSFT AAPL`

    For more information, feel free to ask!
    """
    await ctx.send(help_message)

def p(company, start, end):
    yy_start, mm_start, dd_start = str(start).split('-')
    yy_end, mm_end, dd_end = str(end).split('-')
    i = 0
    colors=COLORS
    nt = []
    for com in company:
        col = random.choice(colors)

        start1 = datetime.datetime(int(yy_start), int(mm_start), int(dd_start))
        end1 = datetime.datetime(int(yy_end), int(mm_end), int(dd_end))
        historical_data = yf.download(com, start=start1, end=end1, progress=False)
        print(historical_data)
        plt.plot(historical_data['Close'], color=col, label=com)
        plt.xlabel('Datetime')
        plt.ylabel('closing price')
        plt.legend()
        i = i + 1
        colors.remove(col)

    plt.gcf().autofmt_xdate()
    plt.savefig('image.png')
    chart = discord.File('image.png', filename='image.png')
    plt.close()
    return chart
async def get_stock_statistics(stock_symbol):
    stock_data = yf.Ticker(stock_symbol)
    stock_info = stock_data.history(period="1d")

    if stock_info.empty:
        return None

    previous_close = stock_info['Close'][0]
    opening_price = stock_info['Open'][0]
    high_price = stock_info['High'][0]
    low_price = stock_info['Low'][0]
    closing_price = stock_info['Close'][0]
    trading_volume = stock_info['Volume'][0]

    return {
        'Previous Close': previous_close,
        'Opening Price': opening_price,
        'High Price': high_price,
        'Low Price': low_price,
        'Closing Price': closing_price,
        'Trading Volume': trading_volume
    }
@client.event
async def on_message(message):
    ppp = False
    msg = message.content
    com = []
    list_msg = msg.split(' ')
    end = datetime.date.today()
    start = datetime.date.today() - relativedelta(year=datetime.date.today().year - 1)
    per = '3d'
    is_company = False

    if client.user == message.author:
        return
    elif msg.startswith("$stock") or msg.startswith("help") or "help" in msg:
        await help_command(message.channel) # Call the help function

    else:
        for word in list_msg:
            word = word.upper()
            if word == '\0':
                break
            elif word.upper() in compy:
                com.append(word)
                is_company = True
            elif word.endswith('YR') and word[:-2].isdigit():
                ppp = False
                end = datetime.date.today()
                start = datetime.date.today() - relativedelta(years=int(word[:-2]))

            elif word.endswith('HR') and word[:-2].isdigit():
                ppp = True
                end = datetime.datetime.now()
                start = datetime.datetime.now() - relativedelta(hours=int(word[:-2]))

            elif word.endswith('D') and word[:-1].isdigit():
                ppp = True
                end = datetime.date.today()
                start = datetime.date.today() - relativedelta(days=int(word[:-1]))
            else:
                for key in companies:
                    if key.startswith(word.upper()):
                        l = key.split(" ")
                        if l[0] == word.upper().split()[0]:
                            is_company = True
                            com.append(companies[key])
                            break
                        else:
                            break
                try:
                    date_obj = datetime.datetime.strptime(word, '%Y-%m-%d').date()
                    if date_obj <= datetime.date.today():
                        if start == datetime.date.today() - relativedelta(years=1):
                            start = date_obj
                        else:
                            end = date_obj
                except ValueError:
                    pass

        if not is_company:
            await message.channel.send("ENTER A VALID COMPANY CODE")

    if ppp:
        await message.channel.send(file=company_period(com, per))

    elif not ppp and is_company:
        await message.channel.send(file=p(com, start, end))
    if com:
        message.channel.send("PREVIOUS DAY CLOSING AND CURRENT DAY OPENING AND RELEVANT INFO")
    for c in com:
        stock_statistics = await get_stock_statistics(c)
        if stock_statistics is not None:
            await message.channel.send(f"Stock: {c}")
            await message.channel.send(f"Previous Close: ${stock_statistics['Previous Close']:.2f}")
            await message.channel.send(f"Opening Price: ${stock_statistics['Opening Price']:.2f}")
            await message.channel.send(f"High Price: ${stock_statistics['High Price']:.2f}")
            await message.channel.send(f"Low Price: ${stock_statistics['Low Price']:.2f}")
            await message.channel.send(f"Closing Price: ${stock_statistics['Closing Price']:.2f}")
            await message.channel.send(f"Trading Volume: {stock_statistics['Trading Volume']:,} shares")
            await message.channel.send("---------------")
        else:
            await message.channel.send(f"Stock data not available for {c}")


load_dotenv()
TOKEN = os.getenv("token_key")

client.run(TOKEN)
