""" Helpers for date manipulation"""

from datetime import datetime, timedelta


def datetime_to_day(date: datetime) -> datetime:
    """
    Round date to day

    Args:
        date (datetime): Date as datetime

    Returns:
        datetime : Date rounded to day
    """
    return datetime(*date.timetuple()[:3])


def datetime_to_month(date: datetime) -> datetime:
    """
    Round date to month

    Args:
        date (str): Date as datetime

    Returns:
        datetime : Date rounded to month
    """
    return datetime(*date.timetuple()[:2], 1)


def datetime_to_year(date: datetime) -> datetime:
    """
    Round date to year

    Args:
        date (str): Date as datetime

    Returns:
        datetime : Date rounded to day
    """
    return datetime(date.timetuple()[0], 1, 1)


def timedelta_in_months(end: datetime, start: datetime) -> datetime:
    """
    Compute the time delta between two dates.

    Args:
        end (datetime): End datetime
        start (datetime): Start datetime

    Returns:
        datetime : Time delta computed
    """
    return 12 * (end.year - start.year) + (end.month - start.month)


def date_merge_semester(fulldate: datetime) -> str:
    """
    Reduce a datetime to semesters
    Output must still be sortable in ascending order.

    Args:
        fulldate (datetime): Full date as a datetime object

    Returns:
        str: Date as Years-Month format
    """

    re_month = 12
    if fulldate.month <= 6:
        re_month = 6
    date_semester = datetime(year=fulldate.year, month=re_month, day=1)
    return date_semester.strftime("%Y-%m")


def timedelta_merge(full_age: timedelta) -> str:
    """
    Reduce date to age categories

    Args:
        full_age (timedelta): Age of the author on the repository

    Returns:
        age (str): Age interval as a string
    """
    age_month = full_age.days / 30

    age = " 0-3 months"
    if age_month > 3:
        age = " 3-6 months"
    if age_month > 6:
        age = " 6-9 months"
    if age_month > 9:
        age = " 9-12 months"
    if age_month > 12:
        age = "12-15 months"
    if age_month > 15:
        age = "15-18 months"
    if age_month > 18:
        age = "18-21 months"
    if age_month > 21:
        age = "21-24 months"
    if age_month > 24:
        age = ">2years"
    return age
