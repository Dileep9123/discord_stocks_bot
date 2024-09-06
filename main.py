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

# Initialize Discord bot with necessary intents
intents = discord.Intents.default()
intents.messages = True  # Enable intents for messages
intents.message_content=True  # Enable intents for messages content
intents.guilds = True     # Enable intents for guilds (servers)

bot = commands.Bot(command_prefix="$", intents=intents)
client = discord.Client(intents=intents)

COLORS = colors  # Set available colors

@client.event
async def on_ready():
    """Event triggered when the bot is ready and connected to Discord."""
    print(f"We logged in as {client.user}")

def company_period(company, period):
    """
    Fetch stock data for a list of companies for a given period and plot it.

    Args:
        company (list): List of company symbols.
        period (str): Period to fetch stock data for.

    Returns:
        discord.File: A file object containing the chart image.
    """
    for com in company:
        col = random.choice(colors)  # Choose random color
        historical_data = yf.download(com, progress=False, period=period)  # Download historical data
        plt.plot(historical_data['Close'], color=col, label=com)  # Plot data
        plt.xlabel('Datetime')
        plt.ylabel('Closing price')
        plt.legend()
    
    plt.gcf().autofmt_xdate()
    plt.savefig('image.png')  # Save the chart as an image
    chart = discord.File('image.png', filename='image.png')  # Prepare the image for sending
    plt.close()
    
    return chart

async def help_command(ctx):
    """Sends a help message with instructions on how to use the bot."""
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
    """
    await ctx.send(help_message)

def p(company, start, end):
    """
    Fetch and plot stock data for a list of companies between two dates.

    Args:
        company (list): List of company symbols.
        start (str): Start date (YYYY-MM-DD).
        end (str): End date (YYYY-MM-DD).

    Returns:
        discord.File: A file object containing the chart image.
    """
    yy_start, mm_start, dd_start = str(start).split('-')
    yy_end, mm_end, dd_end = str(end).split('-')
    
    for com in company:
        col = random.choice(COLORS)
        start_date = datetime.datetime(int(yy_start), int(mm_start), int(dd_start))
        end_date = datetime.datetime(int(yy_end), int(mm_end), int(dd_end))
        historical_data = yf.download(com, start=start_date, end=end_date, progress=False)
        plt.plot(historical_data['Close'], color=col, label=com)
        plt.xlabel('Datetime')
        plt.ylabel('Closing price')
        plt.legend()
    
    plt.gcf().autofmt_xdate()
    plt.savefig('image.png')
    chart = discord.File('image.png', filename='image.png')
    plt.close()

    return chart

async def get_stock_statistics(stock_symbol):
    """
    Fetch daily stock statistics for a specific company.

    Args:
        stock_symbol (str): The stock symbol of the company.

    Returns:
        dict: A dictionary containing stock statistics (e.g., closing price, high, low).
    """
    stock_data = yf.Ticker(stock_symbol)
    stock_info = stock_data.history(period="1d")

    if stock_info.empty:
        return None

    return {
        'Previous Close': stock_info['Close'][0],
        'Opening Price': stock_info['Open'][0],
        'High Price': stock_info['High'][0],
        'Low Price': stock_info['Low'][0],
        'Closing Price': stock_info['Close'][0],
        'Trading Volume': stock_info['Volume'][0]
    }

@client.event
async def on_message(message):
    """
    Event triggered when a new message is sent in a Discord channel.
    Processes stock-related commands.
    """
    ppp = False
    msg = message.content
    com = []
    list_msg = msg.split(' ')
    end = datetime.date.today()
    start = datetime.date.today() - relativedelta(year=datetime.date.today().year - 1)
    per = '3d'
    is_company = False

    if client.user == message.author:
        return  # Ignore messages sent by the bot itself

    if msg.startswith("$stock") or msg.startswith("help") or "help" in msg:
        await help_command(message.channel)  # Send help message

    else:
        # Process each word in the message
        for word in list_msg:
            word = word.upper()

            if word == '\0':
                break
            elif word.upper() in compy:  # Check if the word matches a known company code
                com.append(word)
                is_company = True

            elif word.endswith('YR') and word[:-2].isdigit():  # Handle year-based period
                ppp = False
                end = datetime.date.today()
                start = datetime.date.today() - relativedelta(years=int(word[:-2]))

            elif word.endswith('HR') and word[:-2].isdigit():  # Handle hour-based period
                ppp = True
                end = datetime.datetime.now()
                start = datetime.datetime.now() - relativedelta(hours=int(word[:-2]))

            elif word.endswith('D') and word[:-1].isdigit():  # Handle day-based period
                ppp = True
                end = datetime.date.today()
                start = datetime.date.today() - relativedelta(days=int(word[:-1]))

            else:
                # Match against known company codes in the companies dictionary
                for key in companies:
                    if key.startswith(word.upper()):
                        l = key.split(" ")
                        if len(l) > 0 and len(word.upper().split()) > 0:  # Ensure non-empty split
                            if l[0] == word.upper().split()[0]:
                                is_company = True
                                com.append(companies[key])
                                break

                # Handle date format checking
                try:
                    date_obj = datetime.datetime.strptime(word, '%Y-%m-%d').date()
                    if date_obj <= datetime.date.today():
                        if start == datetime.date.today() - relativedelta(years=1):
                            start = date_obj
                        else:
                            end = date_obj
                except ValueError:
                    pass

        # Notify if no valid company is found
        if not is_company:
            await message.channel.send("ENTER A VALID COMPANY CODE")

    # If ppp is True, plot period-based data
    if ppp:
        await message.channel.send(file=company_period(com, per))

    # If ppp is False and company codes are valid, plot date-based data
    elif not ppp and is_company:
        await message.channel.send(file=p(com, start, end))

    # Send stock statistics if companies are provided
    if com:
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

# Load environment variables and run the bot
load_dotenv()
TOKEN = os.getenv("token_key")
client.run(TOKEN)
