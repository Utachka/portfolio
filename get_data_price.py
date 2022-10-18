import requests

class Price:
    def __init__(self):
        self.price_dict = {} # Словарь с данными по ценам

    def get_api_binance(self):
        """Подключаемся к api Binance"""
        self.base = 'https://fapi.binance.com'
        self.path = '/fapi/v1/premiumIndex'
        self.url = self.base + self.path
        self.param = {"symbol" : "BTCUSDT"}  # параметр, которых необходимо передавать по данному api
        """Вызываем api с параметром"""
        self.req = requests.get(self.url, params = self.param)
        """Ключ для словаря"""
        self.symb = "BTC(Binance)"
        """Проверяем, если пришел положительный ответ от сервера, то заходим в блок"""
        if self.req.status_code == 200:
            """Получаем значение для нашего ключа"""
            self.price = self.req.json()['markPrice']
            """Вносим значение в словарь, предварительно округлив полученное значение по api"""
            self.price_dict[self.symb] = round(float(self.price), 1)
        else:
            """Если значения по переданному параметру не будет, то получим в значение словаря надпись с ошибкой"""
            self.price_dict[self.symb] = "err"


    def get_api_gate(self):
        """Подключаемся к апи Gate"""
        self.url = "https://data.gateapi.io/api2/1/tickers"
        """Вызываем api"""
        self.req = requests.get(self.url)
        """Ключ для словаря"""
        self.symb = "BTC(GateIO)"
        """Проверяем, если пришел положительный ответ от сервера, то заходим в блок"""
        if self.req.status_code == 200:
            """Получаем значение для нашего ключа"""
            self.price = self.req.json()["btc_usdt"]["last"]
            """Вносим значение в словарь, предварительно округлив полученное значение по api"""
            self.price_dict[self.symb] = round(float(self.price), 1)
        else:
            """Если значения по переданному параметру не будет, то получим в значение словаря надпись с ошибкой"""
            self.price_dict[self.symb] = "err"

    def get_api_ftx(self):
        """Подключаемся к api FTX"""
        self.base = "https://ftx.com/api"
        self.path = '/markets'
        self.url = self.base + self.path
        """Вызываем api"""
        self.req = requests.get(self.url)
        """Ключ для словаря"""
        self.symb = "BTC(FTX)"
        """Проверяем, если пришел положительный ответ от сервера, то заходим в блок"""
        if self.req.status_code == 200:
            """Здесь мы получили список, по этому перебираем все элементы и если находим нужное значение по ключу = name у следующего элемента списка, то забираем от туда цену"""
            for i in range(len(self.req.json()["result"])):
                if self.req.json()["result"][i]["name"] == "BTC/USDT":
                    self.price_dict[self.symb] = round(float(self.req.json()["result"][i]["price"]), 1)
        else:
            """Если значения по переданному параметру не будет, то получим в значение словаря надпись с ошибкой"""
            self.price_dict[self.symb] = "err"

    """Функция, в которой запускаются все блоки, которые заполняют справочик и возвращаем справочник"""
    def get_data(self):
        self.get_api_binance()
        self.get_api_gate()
        self.get_api_ftx()
        return self.price_dict


