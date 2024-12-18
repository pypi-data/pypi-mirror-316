# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["DateDrivenTerm"]


class DateDrivenTerm(BaseModel):
    id: str
    """The unique identifier assigned by QuickBooks to this date-driven term.

    This ID is unique across all date-driven terms but not across different
    QuickBooks object types.
    """

    created_at: str = FieldInfo(alias="createdAt")
    """
    The date and time when this date-driven term was created, in ISO 8601 format
    (YYYY-MM-DDThh:mm:ss±hh:mm). The time zone is the same as the user's time zone
    in QuickBooks.
    """

    discount_day_of_month: Optional[float] = FieldInfo(alias="discountDayOfMonth", default=None)
    """
    The day of the month within which payment must be received to qualify for the
    discount specified by `discountPercentage`.
    """

    discount_percentage: Optional[str] = FieldInfo(alias="discountPercentage", default=None)
    """
    The discount percentage applied to the payment if received on or before the
    specified `discountDayOfMonth`. The value is between 0 and 100.
    """

    due_day_of_month: float = FieldInfo(alias="dueDayOfMonth")
    """The day of the month when full payment is due without discount."""

    grace_period_days: Optional[float] = FieldInfo(alias="gracePeriodDays", default=None)
    """
    The number of days before `dueDayOfMonth` when an invoice or bill issued within
    this threshold is considered due the following month. For example, with
    `dueDayOfMonth` set to 15 and `gracePeriodDays` set to 2, an invoice issued on
    the 13th would be due on the 15th of the next month, while an invoice issued on
    the 12th would be due on the 15th of the current month.
    """

    is_active: bool = FieldInfo(alias="isActive")
    """Indicates whether this date-driven term is active.

    Inactive objects are typically hidden from views and reports in QuickBooks.
    """

    name: str
    """
    The case-insensitive unique name of this date-driven term, unique across all
    date-driven terms.

    **NOTE**: Date-driven terms do not have a `fullName` field because they are not
    hierarchical objects, which is why `name` is unique for them but not for objects
    that have parents. Maximum length: 31 characters.
    """

    object_type: Literal["qbd_date_driven_term"] = FieldInfo(alias="objectType")
    """The type of object. This value is always `"qbd_date_driven_term"`."""

    revision_number: str = FieldInfo(alias="revisionNumber")
    """
    The current revision number of this date-driven term object, which changes each
    time the object is modified. When updating this object, you must provide the
    most recent `revisionNumber` to ensure you're working with the latest data;
    otherwise, the update will return an error.
    """

    updated_at: str = FieldInfo(alias="updatedAt")
    """
    The date and time when this date-driven term was last updated, in ISO 8601
    format (YYYY-MM-DDThh:mm:ss±hh:mm). The time zone is the same as the user's time
    zone in QuickBooks.
    """
