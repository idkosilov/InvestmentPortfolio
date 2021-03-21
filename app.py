"""Developer: Kosilov I.
Рассчет оптимального инвестиционного портфеля по показателю ROI при заданном бюджете инвестиций
"""
from collections import namedtuple, Counter
from typing import List, Dict
import csv

Stock = namedtuple("Stock", ["name", "ROI", "price"])


def get_stocks(file: str) -> List[Stock]:
    """
    Парсит информацию об акциях из csv-файла, полученную с сайта YahooFinance.
    Возразает массив акций с параметрами ROI и цены акции.

    ROI (Return On Investment) = Доход/Сумму инвестиций
    """
    stocks = []
    with open(file) as stocks_file:
        for row in csv.reader(stocks_file, delimiter=';'):
            stocks.append(Stock(name=row[0], ROI=float(row[1]), price=round(float(row[2]))))
    return stocks


def update_portfolio(portfolio: Dict, stock: Stock) -> Dict:
    """
    Вычисляет инвестиционный портфель из предыдущего, путем добавления предыдущему новой акции
    :param portfolio:
    :param stock:
    :return:
    """
    new_portfolio = dict()
    new_portfolio["stocks"] = []
    for old_stock in portfolio["stocks"]:
        new_portfolio["stocks"].append(old_stock)
    new_portfolio["stocks"].append(stock)
    new_portfolio["price"] = portfolio["price"] + stock.price
    new_portfolio["ROI"] = sum(stock.price * stock.ROI for stock in new_portfolio["stocks"]) / new_portfolio["price"]
    return new_portfolio


def get_income(portfolio: Dict) -> float:
    return portfolio["price"] * portfolio["ROI"]


def optimal_portfolio(stocks, budget_of_investment, diversification_ratio):
    """
    Функция вычисляющая оптимальный портфель.
    !!!Для ускорения вычислений стоимость акций округляется до целого!!!

    :param stocks: информация об акциях
    :param budget_of_investment: бюджет
    :param diversification_ratio: количество различных акций в портфеле
    :return:
    """
    portfolios = [{"price": 0, "ROI": 0, "stocks": []} for _ in range(budget_of_investment + 1)]
    for budget in range(len(portfolios)):
        for stock in stocks:
            if stock.price <= budget:
                new_portfolio = update_portfolio(portfolios[budget - stock.price], stock)
                best_portfolio = max(portfolios[budget], new_portfolio, key=get_income)
                counter_stocks = Counter(best_portfolio["stocks"])
                if not(counter_stocks[stock] > 1 and len(set(best_portfolio["stocks"])) < diversification_ratio):
                    portfolios[budget] = best_portfolio
    return portfolios[-1]


def text_info(portfolio: Dict, budget: int, diversification_ratio: int):
    stocks = Counter(portfolio["stocks"])
    stocks_info = ""
    for stock_info, number in stocks.items():
        stocks_info += f"Акции {stock_info.name} в количестве {number}\n" \
                       f"Показатели акции:\n" \
                       f"Рентабельность инвестиций = {stock_info.ROI} %\n" \
                       f"Стоимость = {stock_info.price} $\n\n"

    print(f"Оптимальный портфель для бюджета {budget} $ c коэффициентов диверсификации = {diversification_ratio}\n"
          f"Рентабельности инвестиций = {round(portfolio['ROI'], 2)} %\n"
          f"Стоимость портфеля = {portfolio['price']} $\n", stocks_info, sep="\n")


def main():
    stocks = get_stocks("stocks.csv")
    budget_of_investment = 750  # Бюджет инвестиций в долларах
    diversification_ratio = 5  # Число компаний
    portfolio = optimal_portfolio(stocks, budget_of_investment, diversification_ratio)
    text_info(portfolio, budget_of_investment, diversification_ratio)


if __name__ == "__main__":
    main()
