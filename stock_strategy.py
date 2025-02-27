from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Tuple 
device = "cuda:0" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)
labels = ["positive", "negative", "neutral"]

def estimate_sentiment(news):
    if news:
        tokens = tokenizer(news, return_tensors="pt", padding=True).to(device)

        result = model(tokens["input_ids"], attention_mask=tokens["attention_mask"])[
            "logits"
        ]
        result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)
        probability = result[torch.argmax(result)]
        sentiment = labels[torch.argmax(result)]
        return probability, sentiment
    else:
        return 0, labels[-1]


if _name_ == "_main_":
    tensor, sentiment = estimate_sentiment(['markets responded negatively to the news!','traders were displeased!'])
    print(tensor, sentiment)
    print(torch.cuda.is_available()) # TraderBot
Build a trader bot which looks at sentiment of live news events and trades appropriately. 

## See it live and in action 📺
<img src="https://i.imgur.com/FaQH8rz.png"/>

# Startup 🚀
1. Create a virtual environment conda create -n trader python=3.10 
2. Activate it conda activate trader
3. Install initial deps pip install lumibot timedelta alpaca-trade-api==3.1.1
4. Install transformers and friends pip install torch torchvision torchaudio transformers 
5. Update the API_KEY and API_SECRET with values from your Alpaca account 
6. Run the bot python tradingbot.py

<p>N.B. Torch installation instructions will vary depending on your operating system and hardware. See here for more: 
<a href="pytorch.org/">PyTorch Installation Instructions</a></p>

If you're getting an SSL error when you attempt to call out to the Alpaca Trading api, you'll need to install the required SSL certificates into your machine.
1. Download the following intermediate SSL Certificates, these are required to communicate with Alpaca
* https://letsencrypt.org/certs/lets-encrypt-r3.pem 
* https://letsencrypt.org/certs/isrg-root-x1-cross-signed.pem 
2. Once downloaded, change the file extension of each file to .cer 
3. Double click the file and run through the wizard to install it, use all of the default selections. 

</br>
# Other References 🔗

<p>-<a href="github.com/Lumiwealth/lumibot)">Lumibot</a>:trading bot library, makes lifecycle stuff easier .</p>

# Who, When, Why?

👨🏾‍💻 Author: Nick Renotte <br />
📅 Version: 1.x<br />
📜 License: This project is licensed under the MIT License </br>
 aiodns==3.1.1
aiohttp==3.8.2
aiosignal==1.3.1
alpaca-py==0.14.0
alpaca-trade-api==3.1.1
alpha-vantage==2.3.1
annotated-types==0.6.0
anyio==4.2.0
appdirs==1.4.4
APScheduler==3.10.4
argon2-cffi==23.1.0
argon2-cffi-bindings==21.2.0
arrow==1.3.0
asttokens==2.4.1
async-lru==2.0.4
async-timeout==4.0.3
asyncio-nats-client==0.11.5
attrs==23.2.0
Babel==2.14.0
bcrypt==4.1.2
beautifulsoup4==4.12.2
bidict==0.22.1
bleach==6.1.0
blinker==1.7.0
ccxt==4.2.22
certifi==2023.11.17
cffi==1.16.0
charset-normalizer==2.1.1
click==8.1.7
colorama==0.4.6
comm==0.2.1
contourpy==1.2.0
cryptography==42.0.2
cycler==0.12.1
debugpy==1.8.0
decorator==5.1.1
defusedxml==0.7.1
deprecation==2.1.0
dnspython==2.5.0
email-validator==2.1.0.post1
exceptiongroup==1.2.0
exchange_calendars==4.5.2
executing==2.0.1
fastjsonschema==2.19.1
filelock==3.13.1
Flask==3.0.1
Flask-BabelEx==0.9.4
Flask-Login==0.6.3
Flask-Mail==0.9.1
flask-marshmallow==1.1.0
Flask-Principal==0.4.0
Flask-Security==3.0.0
Flask-SocketIO==5.3.6
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.1
fonttools==4.47.0
fqdn==1.5.1
frozendict==2.4.0
frozenlist==1.4.1
fsspec==2023.12.2
gitdb==4.0.11
GitPython==3.1.41
greenlet==3.0.3
h11==0.14.0
html5lib==1.1
huggingface-hub==0.20.3
ibapi==9.81.1.post1
idna==3.6
inflection==0.5.1
iniconfig==2.0.0
ipykernel==6.28.0
ipython==8.20.0
isoduration==20.11.0
itsdangerous==2.1.2
jedi==0.19.1
Jinja2==3.1.2
joblib==1.3.2
json5==0.9.14
jsonpickle==3.0.2
jsonpointer==2.4
jsonschema==4.20.0
jsonschema-specifications==2023.12.1
jupyter-events==0.9.0
jupyter-lsp==2.2.1
jupyter-server-mathjax==0.2.6
jupyter_client==8.6.0
jupyter_core==5.7.1
jupyter_server==2.12.3
jupyter_server_terminals==0.5.1
jupyterlab==4.0.10
jupyterlab_git==0.50.0
jupyterlab_pygments==0.3.0
jupyterlab_server==2.25.2
kiwisolver==1.4.5
korean-lunar-calendar==0.3.1
lumibot==3.0.6
lumiwealth-tradier==0.1.5
lxml==5.1.0
MarkupSafe==2.1.3
marshmallow==3.20.2
marshmallow-sqlalchemy==1.0.0
matplotlib==3.8.2
matplotlib-inline==0.1.6
mistune==3.0.2
more-itertools==10.2.0
mpmath==1.3.0
msgpack==1.0.3
multidict==5.2.0
multitasking==0.0.11
nbclient==0.9.0
nbconvert==7.14.0
nbdime==4.0.1
nbformat==5.9.2
nest-asyncio==1.5.8
networkx==3.2.1
notebook_shim==0.2.3
numpy==1.26.3
nvidia-cublas-cu12==12.1.3.1
nvidia-cuda-cupti-cu12==12.1.105
nvidia-cuda-nvrtc-cu12==12.1.105
nvidia-cuda-runtime-cu12==12.1.105
nvidia-cudnn-cu12==8.9.2.26
nvidia-cufft-cu12==11.0.2.54
nvidia-curand-cu12==10.3.2.106
nvidia-cusolver-cu12==11.4.5.107
nvidia-cusparse-cu12==12.1.0.106
nvidia-nccl-cu12==2.19.3
nvidia-nvjitlink-cu12==12.3.101
nvidia-nvtx-cu12==12.1.105
overrides==7.4.0
packaging==23.2
pandas==2.0.3
pandas-datareader==0.10.0
pandas-market-calendars==4.3.2
pandocfilters==1.5.0
parso==0.8.3
passlib==1.7.4
peewee==3.17.0
pexpect==4.9.0
pillow==10.2.0
platformdirs==4.1.0
plotly==5.18.0
pluggy==1.4.0
polygon-api-client==1.13.4
prometheus-client==0.19.0
prompt-toolkit==3.0.43
psutil==5.9.7
ptyprocess==0.7.0
pure-eval==0.2.2
pyarrow==15.0.0
pycares==4.4.0
pycparser==2.21
pydantic==2.6.0
pydantic_core==2.16.1
Pygments==2.17.2
pyluach==2.2.0
pyparsing==3.1.1
pytest==8.0.0
python-dateutil==2.8.2
python-dotenv==1.0.1
python-engineio==4.8.2
python-json-logger==2.0.7
python-socketio==5.11.0
pytz==2023.3.post1
PyYAML==6.0.1
pyzmq==25.1.2
Quandl==3.7.0
quantstats-lumi==0.1.0
referencing==0.32.1
regex==2023.12.25
requests==2.31.0
rfc3339-validator==0.1.4
rfc3986-validator==0.1.1
rpds-py==0.16.2
safetensors==0.4.2
scikit-learn==1.3.2
scipy==1.10.1
seaborn==0.13.1
Send2Trash==1.8.2
simple-websocket==1.0.0
six==1.16.0
smmap==5.0.1
sniffio==1.3.0
soupsieve==2.5
speaklater==1.3
SQLAlchemy==2.0.25
sseclient-py==1.8.0
stack-data==0.6.3
sympy==1.12
tabulate==0.9.0
tenacity==8.2.3
termcolor==2.4.0
terminado==0.18.0
threadpoolctl==3.2.0
timedelta==2020.12.3
tinycss2==1.2.1
tokenizers==0.15.1
tomli==2.0.1
toolz==0.12.1
torch==2.2.0
torchaudio==2.2.0
torchvision==0.17.0
tornado==6.4
tqdm==4.66.1
traitlets==5.14.1
transformers==4.37.2
triton==2.2.0
types-python-dateutil==2.8.19.20240106
typing_extensions==4.9.0
tzdata==2023.4
tzlocal==5.2
uri-template==1.3.0
urllib3==1.26.18
wcwidth==0.2.13
webcolors==1.13
webencodings==0.5.1
websocket-client==1.7.0
websockets==10.4
Werkzeug==3.0.1
wsproto==1.2.0
WTForms==3.1.2
yarl==1.9.4
yfinance==0.2.36
 from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime 
from alpaca_trade_api import REST 
from timedelta import Timedelta 
from finbert_utils import estimate_sentiment

API_KEY = "YOUR API KEY" 
API_SECRET = "YOUR API SECRET" 
BASE_URL = "https://paper-api.alpaca.markets"

ALPACA_CREDS = {
    "API_KEY":API_KEY, 
    "API_SECRET": API_SECRET, 
    "PAPER": True
}

class MLTrader(Strategy): 
    def initialize(self, symbol:str="SPY", cash_at_risk:float=.5): 
        self.symbol = symbol
        self.sleeptime = "24H" 
        self.last_trade = None 
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)

    def position_sizing(self): 
        cash = self.get_cash() 
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price,0)
        return cash, last_price, quantity

    def get_dates(self): 
        today = self.get_datetime()
        three_days_prior = today - Timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')

    def get_sentiment(self): 
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, 
                                 start=three_days_prior, 
                                 end=today) 
        news = [ev._dict_["_raw"]["headline"] for ev in news]
        probability, sentiment = estimate_sentiment(news)
        return probability, sentiment 

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing() 
        probability, sentiment = self.get_sentiment()

        if cash > last_price: 
            if sentiment == "positive" and probability > .999: 
                if self.last_trade == "sell": 
                    self.sell_all() 
                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    "buy", 
                    type="bracket", 
                    take_profit_price=last_price*1.20, 
                    stop_loss_price=last_price*.95
                )
                self.submit_order(order) 
                self.last_trade = "buy"
            elif sentiment == "negative" and probability > .999: 
                if self.last_trade == "buy": 
                    self.sell_all() 
                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    "sell", 
                    type="bracket", 
                    take_profit_price=last_price*.8, 
                    stop_loss_price=last_price*1.05
                )
                self.submit_order(order) 
                self.last_trade = "sell"

start_date = datetime(2020,1,1)
end_date = datetime(2023,12,31) 
broker = Alpaca(ALPACA_CREDS) 
strategy = MLTrader(name='mlstrat', broker=broker, 
                    parameters={"symbol":"SPY", 
                                "cash_at_risk":.5})
strategy.backtest(
    YahooDataBacktesting, 
    start_date, 
    end_date, 
    parameters={"symbol":"SPY", "cash_at_risk":.5}
)
# trader = Trader()
# trader.add_strategy(strategy)
# trader.run_all()
