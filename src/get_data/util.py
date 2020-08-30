import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from typing import List, Tuple


# TODO: Add as methods to models, refactor repeating code


def build_model(model: Model, df: pd.DataFrame) -> None:
    """
    Create or update instances of given model with data in dataframe.
    Implemented using batches of SQL queries.

    Args:
        model: The Django ORM model to add or update data to.
        df: The Pandas dataframe with the data to add or update.

    Raises:
        NotImplementedError: If unknown model is passed in args.
    """

    # Change NaN to None for database NULL compatibility
    df = df.where(df.notnull(), None)

    update_list: List[model] = []
    create_list: List[model] = []

    currency = df["currency"].iloc[0] if "currency" in df else ""
    region = df["region"].iloc[0] if "region" in df else ""

    for index, row in df.iterrows():
        row_dict = row.to_dict()
        new_instance = model(interval=row.name, **row_dict)
        try:
            if "Factor" in model.__name__:
                instance = model.objects.get(
                    interval=row.name, currency=row["currency"], region=row["region"],
                )
            elif "RiskFreeRate" in model.__name__:
                instance = model.objects.get(interval=row.name, currency=row["currency"])
            elif "ExchangeRate" in model.__name__:
                instance = model.objects.get(interval=row.name)
            else:
                raise NotImplementedError(
                    "Unknown model. Please add query pattern to build_model function."
                )
            if not instance == new_instance:
                update_list.append(new_instance)
        except ObjectDoesNotExist:
            create_list.append(new_instance)

    # Only update database if there is something to update
    if update_list:
        model.objects.bulk_update(update_list, df.columns.values.to_list())
    if create_list:
        model.objects.bulk_create(create_list)

    # Print result
    if currency and region:
        print(
            f"{len(create_list)} created, {len(update_list)} updated, {len(df.index) - len(create_list) - len(update_list)} unchanged in {model.__name__} for region {region} and currency {currency}."
        )
    elif currency:
        print(
            f"{len(create_list)} created, {len(update_list)} updated, {len(df.index) - len(create_list) - len(update_list)} unchanged in {model.__name__} for currency {currency}."
        )
    else:
        print(
            f"{len(create_list)} created, {len(update_list)} updated, {len(df.index) - len(create_list) - len(update_list)} unchanged in {model.__name__}."
        )


def build_base_dataframes(
    df_factors: pd.DataFrame, df_mom: pd.DataFrame, region: str, with_rf: bool = False,
) -> Tuple[pd.DataFrame, None]:
    """
    Clean and parse raw factor return dataframes from Kenneth French's data library.

    Args:
        df_factors: The Pandas dataframe with the raw data.
        df_mom: The Pandas dataframe with the momentum factor return data.
        region: The region the factor returns are for.
        with_rf: True if rf should be returned as separate dataframe, False if rf should be dropped.

    Returns:
        A tuple with the cleaned and with momentum merged dataframe with factor returns and the rf dataframe if with_rf is true (else None).
    """

    # Merge with momentum factor
    df_factors["MOM"] = df_mom["MOM"]
    df_factors["currency"] = "USD"
    df_factors["region"] = region

    if with_rf:
        df_rf = df_factors[["RF"]]
        df_rf["currency"] = "USD"
        df_factors.drop(["RF"], axis=1, inplace=True)
        return df_factors, df_rf

    # If rf is not needed, drop data
    df_factors.drop(["RF"], axis=1, inplace=True)

    return df_factors, None
