
"""
Validation rules for the shop pipeline.
"""
import pandas as pd
import pandera.pandas as pa
from pandera.pandas import Column, Check


def date_not_in_future(series):
    today = pd.Timestamp.now().normalize()
    return (series.dropna() <= today).all()


clean_orders_rules = pa.DataFrameSchema({
    "order_id": Column(
        str, unique=True, nullable=False,
        checks=Check.str_matches(r"^[A-Z]\d{3}$")
    ),
    "customer_id": Column(str, nullable=False),
    "category": Column(
        str, Check.isin(["Accessories", "Electronics"])
    ),
    "quantity": Column(float, nullable=True),
    "unit_price": Column(float, Check.ge(0), nullable=True),
    "order_date": Column(
        pa.DateTime,
        nullable=True,
        checks=Check(date_not_in_future, element_wise=False)
    ),
    "source_file": Column(
        str,
        nullable=False,
        checks=Check.str_matches(r".*\S.*")
    ),
})

clean_customers_rules = pa.DataFrameSchema({
    "customer_id": Column(
        str, unique=True, nullable=False,
        checks=Check.str_matches(r"^C\d{3}$")
    ),
    "customer_name": Column(
        str,
        nullable=False,
        checks=Check.str_matches(r".*\S.*")
    ),
    "city": Column(str, nullable=False),
    "email": Column(
        str, nullable=True,
        checks=Check.str_matches(
            r"^$|^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$"
        )
    ),
    "country": Column(
        str, Check.isin(["Germany", "Austria", "Switzerland"])
    ),
})
