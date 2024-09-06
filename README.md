# Discord StockBot

Discord StockBot is a Python-based Discord bot that provides stock-related information and statistics to users. It fetches historical stock price data from Yahoo Finance using the `yfinance` library and presents it in graphical form using `matplotlib`. The bot responds to user queries and can handle multiple stock symbols in a single query.

## Features

- Fetch historical stock prices for a specific period (e.g., 1 day, 1 week, 1 month, etc.).
- Get stock prices between specific dates.
- Retrieve stock prices for the past years.
- Plot stock price data in a graph with different colors for each stock symbol.
- Display additional stock statistics, including previous day's closing price, opening price, high price, low price, closing price, and trading volume.
- Calculate percentage change in stock price compared to the previous day's closing price.

## Requirements

- Python 3.7 or higher
- `discord.py` library
- `yfinance` library
- `matplotlib` library
- `dateutil.relativedelta` library
- `random` library
- `os` library
- `dotenv` library

## Installation

1. Clone the repository to your local machine:


2. Install the required libraries using `pip`:


3. Create a `.env` file in the project directory and add your Discord bot token:


## Usage

1. Run the Discord bot:


2. Invite the bot to your Discord server using the OAuth2 URL provided by Discord.

3. Use the bot by sending commands in the Discord server's text channels:


## Notes

- The bot's data sources are Yahoo Finance for historical stock prices and the AlphaVantage API for company code lookup.
- The provided stock symbols should be valid and listed on Yahoo Finance.
- The bot uses random colors for plotting stock price data on the graph.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The `discord.py` library for Discord bot integration.
- Yahoo Finance for providing stock data APIs.
- The open-source community for various Python libraries used in this project.

![D1](https://github.com/Dileep9123/discord_stocks_bot/blob/main/assests/Screenshot%202024-09-06%20220539.png)

![D2](https://github.com/Dileep9123/discord_stocks_bot/blob/main/assests/Screenshot%202024-09-06%20220605.png)
![D3](https://github.com/Dileep9123/discord_stocks_bot/blob/main/assests/Screenshot%202024-09-06%20220708.png)
![D4](https://github.com/Dileep9123/discord_stocks_bot/blob/main/assests/Screenshot%202024-09-06%20220838.png)
![D5](https://github.com/Dileep9123/discord_stocks_bot/blob/main/assests/Screenshot%202024-09-06%20220915.png)
