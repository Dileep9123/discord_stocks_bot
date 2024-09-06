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

![D1](https://github.com/anushayerram2025/Discord_stocks_bot/assets/106475795/eea168f3-61be-4a83-8c7a-32c980c5d275)

![D2](https://github.com/anushayerram2025/Discord_stocks_bot/assets/106475795/5f2556a6-fb48-4613-afad-4ea3c1cea66b)
![D3](https://github.com/anushayerram2025/Discord_stocks_bot/assets/106475795/73ea6098-39d2-43d8-81fb-25e111a24ee2)
![D4](https://github.com/anushayerram2025/Discord_stocks_bot/assets/106475795/cd8d495c-6557-499e-b76d-6caea1c31fe3)
![D5](https://github.com/anushayerram2025/Discord_stocks_bot/assets/106475795/121f63f5-7440-4b7e-a37e-faab34b7703d)
![D6](https://github.com/anushayerram2025/Discord_stocks_bot/assets/106475795/4768ac7a-cd7b-4287-9431-9ce9465e8349)
