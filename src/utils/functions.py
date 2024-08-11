import csv
from tempfile import NamedTemporaryFile
from contextlib import contextmanager

import matplotlib.pyplot as plt

from config import LOCALE
from db.base_database import Period


@contextmanager
def get_csv(data: list) -> NamedTemporaryFile:
    csvfile = NamedTemporaryFile("r+", newline="")
    csvfile.name = "data.csv"
    try:
        writer = csv.writer(csvfile)
        writer.writerow(["Created", "IsIncome", "Category", "Amount"])
        writer.writerows(data)
        csvfile.seek(0)

        yield csvfile
    finally:
        csvfile.close()

@contextmanager
def get_image(data: list, is_income: bool, period: Period) -> NamedTemporaryFile:
    image = NamedTemporaryFile("rb+")
    image.name = "data.jpg"
    try:
        values = [i[1] for i in data]
        labels = [i[0] for i in data]

        _, ax = plt.subplots(figsize=(9, 16), subplot_kw=dict(aspect="equal"))
        ax.pie(values, wedgeprops=dict(width=0.3), startangle=-40)

        title = str()

        if is_income:
            title += LOCALE["plot_title_income"]
        else:
            title += LOCALE["plot_title_expenses"]

        if period == Period.DAY:
            title += LOCALE["plot_title_today"]
        elif period == Period.WEEK:
            title += LOCALE["plot_title_week"]
        elif period == Period.MONTH:
            title += LOCALE["plot_title_month"]

        ax.set_title(title, fontsize=30)

        ax.legend(labels=labels, loc="center", fontsize=30, bbox_to_anchor=(0.5, -0.2))
        ax.text(
            0, 0, f"{sum(values):,.2f}{LOCALE['currency']}".replace(",", " "),
            fontsize=30, horizontalalignment="center")

        plt.savefig(image, format="jpg")
        image.seek(0)

        yield image
    finally:
        image.close()