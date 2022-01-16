#!/usr/bin/env python
"""This module contains code that helps generates the necessary queries that
read data from the database"""
from app.v1.database.models.base import model_dict
from typing import Dict, List, TypeVar, Any

from dateutil.parser import parse as parse_date
from sqlalchemy import desc, asc, or_, and_
from sqlalchemy.orm import Session
from sqlalchemy import func

SessionType = TypeVar('SessionType', bound=Session)
SUPPORTED_QUERY_OPERATORS = (
    '$ne', '$eq', '$in', '$nin', '$gt', '$gte', '$lt', '$lte'
)

def list_query(
        session_obj: SessionType, model_cls, params: List[Dict] = None,
        pagination_args: Dict = None, json_result=False):
    """This function is responsible for returning a list of model instances

    Arg(s):
    -------
    session_obj -> object used to interact with the database
    model_cls -> class that represents the model instances to be returned
    params (List[Dict]) -> List of parameters to used to filter the instances of
        model class instances to be returned
    pagination_args (Dict) -> parameter that indicate how many matched instances
        of the model classes to return and how many matched instances of the
        model classes to skip

    Return(s):
    ---------
    List of model class instances either a raw class instances or as a list of
    dictionaries
    """
    return query(session_obj, model_cls, params, pagination_args, json_result)


def list_query_new(
        session_obj: SessionType, model_cls, params: List[Dict] = None,
        pagination_args: Dict = None, json_result=False):
    """This function is responsible for returning a list of model instances

    Arg(s):
    -------
    session_obj -> object used to interact with the database
    model_cls -> class that represents the model instances to be returned
    params (List[Dict]) -> List of parameters to used to filter the instances of
        model class instances to be returned
    pagination_args (Dict) -> parameter that indicate how many matched instances
        of the model classes to return and how many matched instances of the
        model classes to skip

    Return(s):
    ---------
    List of model class instances either a raw class instances or as a list of
    dictionaries
    """
    tmp = query_new(
        session_obj, model_cls, params, pagination_args)
    
    if not json_result:
        return tmp

    return [row.to_dict() for row in tmp]


def query_new(
        session_obj: SessionType, model_cls,
        params: List[Dict], pagination_args: Dict):
    """This function is responsible for returning a filter list of model
    instances from the database.

    Arg(s):
    -------
    session_obj (SessionType) -> The object used to interact with the data model
    model_cls -> Model class that represents the database table to get data from
    params (List[Dict]) -> The list of filter conditions that will be used to
        filter the data that is returned
    pagination_args (Dict) -> The pagination arguments that indicates how many
        entities to be returned from the database and how many records to be
        skipped
    Return(s):
    ----------
        returns a list of instance of class passed in the model_cls param
    """
    params = params if params else []
    pagination_args = pagination_args if pagination_args else {}

    record_set = session_obj.query(model_cls)

    record_set = _apply_query_param_new(model_cls, record_set, params)

    record_set = _query_sort(
        model_cls, record_set, pagination_args.get("sort", []))

    return query_limit(record_set, pagination_args)


def query(
        session_obj: SessionType, model_cls,
        params: List[Dict], pagination_args: Dict,
        json_result=False):
    """This function is responsible for returning a filter list of model
    instances from the database.

    Arg(s):
    -------
    session_obj (SessionType) -> The object used to interact with the data model
    model_cls -> Model class that represents the database table to get data from
    params (List[Dict]) -> The list of filter condictions that will be used to
        filter the data that is returned
    pagination_args (Dict) -> The paginations arguments that indicates how many
        entities to be returned from the database and how many records to be
        skipped
    json_result (bool) -> indicates whether the data returned is a list of model
        instances or a list of dictionaries representing each model instance
        that is returned which

    Return(s):
    ----------
        returns a list of instance of class passed in the model_cls param or
        list of dictionaries representing
    """
    if not pagination_args:
        pagination_args = {}

    record_set = session_obj.query(model_cls)

    for param in params:
        record_set = _apply_query_param(model_cls, record_set, param)
    record_set = _query_sort(
        model_cls, record_set, pagination_args.get("sort", []))

    if not record_set:
        return []

    result = query_limit(record_set, pagination_args)
    if not json_result:
        return result

    try:
        return [row.to_dict() for row in result]
    except AttributeError:
        return [model_dict(row, model_cls.COLUMNS) for row in result]


def query_limit(record_set, pagination_args: Dict = None):
    """This function applies the pagination arguments to the record set that is
    passed to it

    Arg(s)
    ------
    record_set -> the record set object that needs the pagination arguments
        applied to it
    pagination_args (Dict) -> the pagination arguments that need to be applied
        to the record set

    Return(s)
    ---------
    record_set -> a new record set with the pagination arguments applied to it
    """
    pagination_args = pagination_args if pagination_args else {}

    if pagination_args.get("offset", 0) > 0:
        record_set = record_set.offset(pagination_args["offset"])

    if pagination_args.get("limit", 0) > 0:
        record_set = record_set.limit(pagination_args["limit"])

    return record_set


def _query_sort(model_cls, record_set, sort_params: List[List]):
    """This function is responsible for applying a sort to a particular record
    set

    Arg(s)
    ------
    model_cls -> class representing the model whose record set we to sort
    record_set -> instance of the record set that the sort must be applied to
    sort_params (List[List]) -> the list of sort that need to be applied to the
        record set

    Return(s)
    ---------
    record_set -> returns a new record set with the sort params applied to it
    """

    is_view = hasattr(model_cls, 'select') and hasattr(model_cls, 'schema')

    for sort_param in sort_params:
        (field, ordering) = sort_param
        if str(ordering).upper() == "ASC":
            order_func = asc
        elif str(ordering).upper() == "DESC":
            order_func = desc
        else:
            raise NotImplementedError(
                "{0} isn't a valid ordering functions".format(ordering))

        if is_view:
            model_field = getattr(getattr(model_cls, 'c'), field)
        else:
            model_field = getattr(model_cls, field)

        record_set = record_set.order_by(order_func(model_field))

    return record_set


def _convert_if_date(value: Any):
    """This function converts the value passed to it to a date or list of dates
    if it is annotated as containing a date. This is necessary because dates are
    not natively supported in json

    Args(s):
    --------
    value -> the value to be converted to a native date value if it's a date

    Return(s):
    ----------
    returns the same value field if it is not annotated as contains a date or
    it returns a native date or list of native date values
    """
    if hasattr(value, 'items') and hasattr(value, "fromkeys"):
        if hasattr(
                value["$date"], "append") and hasattr(value["$date"], "clear"):
            return [parse_date(date_val) for date_val in value["$date"]]
        return parse_date(value["$date"])
    return value


def resolve_condition_new(field_parent, params):

    statements = []

    for row in params:
 
        field = list(row.keys())[0]

        for operator in row[field].keys():

            operator_value = _convert_if_date(row[field][operator])
            model_field = getattr(field_parent, field)
            
            if operator == "$eq":

                if operator_value is None:
                    statements.append(model_field.is_(None))

                statements.append(model_field.__eq__(operator_value))

            elif operator == "$ne":
                statements.append(model_field.__ne__(operator_value))

            elif operator == "$lt":
                statements.append(model_field.__lt__(operator_value))

            elif operator == "$lte":
                statements.append(
                    or_(
                        model_field < operator_value,
                        model_field == operator_value
                    )
                )
            elif operator == "$gt":
                statements.append(model_field.__gt__(operator_value))

            elif operator == "$gte":
                statements.append(
                    or_(
                        model_field > operator_value,
                        model_field == operator_value
                    )
                )

            elif operator == "$nin":
                statements.append(model_field.notin_(operator_value))

            elif operator == "$in":
                statements.append(model_field.in_(operator_value))

            elif operator == "$lk":
                statements.append(model_field.like(operator_value))

            elif operator == "$ilk":
                statements.append(model_field.ilike(operator_value))

            elif operator == "$nlk":
                statements.append(model_field.notlike(operator_value))

            elif operator == "$nilk":
                statements.append(model_field.notilike(operator_value))

            elif operator == "$stw":
                statements.append(model_field.startswith(operator_value))

            elif operator == "$edw":
                statements.append(model_field.endswith(operator_value))

            elif operator == "$con":
                statements.append(
                    func.lower(model_field).contains(operator_value.lower()))

            else:
                raise ValueError(
                    f"Operator {operator} used is currently unsupported")

    return statements


def resolve_condition(field_parent, record_set, params):

    for field in params:

        for operator in params[field].keys():

            operator_value = _convert_if_date(params[field][operator])
            model_field = getattr(field_parent, field)
            
            if operator == "$eq":

                if operator_value is None:
                    return record_set.filter(model_field.is_(None))

                return record_set.filter(model_field == operator_value)

            elif operator == "$ne":
                return record_set.filter(model_field != operator_value)

            elif operator == "$lt":
                return record_set.filter(model_field < operator_value)

            elif operator == "$lte":
                return record_set.filter(
                    or_(
                        model_field < operator_value,
                        model_field == operator_value
                    )
                )
            elif operator == "$gt":
                return record_set.filter(model_field > operator_value)

            elif operator == "$gte":
                return record_set.filter(
                    or_(
                        model_field > operator_value,
                        model_field == operator_value
                    )
                )

            elif operator == "$nin":
                return record_set.filter(model_field.notin_(operator_value))

            elif operator == "$in":
                return record_set.filter(model_field.in_(operator_value))

            elif operator == "$lk":
                return record_set.filter(
                    model_field.like(f"%{operator_value}%"))

            elif operator == "$nlk":
                return record_set.filter(
                    model_field.notlike(f"%{operator_value}%"))


def _apply_query_param_new(model_cls, record_set, params: List[Dict]) -> bool:
    """This function is responsible for applying a filter parameter to a
    record set

    Arg(s)
    ------
    model_cls -> class representing the model that the filter parameter must be
        applied
    record_set -> record set instance that the filter parameter must be applied
    params (Dict) -> Dictionary that represents the filtering paramater that
        must be applied

    Return(s)
    ---------
    returns a new record set instance with the filtering parameter applied to it
    """

    is_view = hasattr(model_cls, 'select') and hasattr(model_cls, 'schema')
    if is_view:
        field_parent = getattr(model_cls, 'c')
    else:
        field_parent = model_cls
    
    stmt_pieces = []

    for grouping in params:

        for grouping_key in grouping.keys():

            if grouping_key not in ('$and', '$or'):
                raise ValueError(
                    f"'{grouping_key}' is not a supported joining statement. "
                    "Supported statements is $and or $or")
            
            if grouping_key == "$and":
                conjunction_stmt = and_
            else:
                conjunction_stmt = or_

            resolved_conditions = []

            # for condition in grouping[grouping_key]:
            #     record_set = resolve_condition_new(model_cls, record_set, condition)
            conditions = resolve_condition_new(model_cls, grouping[grouping_key])

            record_set = record_set.filter(conjunction_stmt(*conditions))

    return record_set


def _apply_query_param(model_cls, record_set, params: Dict):
    """This function is responsible for applying a filter parameter to a
    record set

    Arg(s)
    ------
    model_cls -> class representing the model that the filter parameter must be
        applied
    record_set -> record set instance that the filter parameter must be applied
    params (Dict) -> Dictionary that represents the filtering paramater that
        must be applied

    Return(s)
    ---------
    returns a new record set instance with the filtering parameter applied to it
    """
    is_view = hasattr(model_cls, 'select') and hasattr(model_cls, 'schema')

    for field in params:
        for operator in params[field].keys():
            operator_value = _convert_if_date(params[field][operator])

            if is_view:
                model_field = getattr(getattr(model_cls, 'c'), field)
            else:
                model_field = getattr(model_cls, field)

            if operator == "$eq":

                if operator_value is None:
                    return record_set.filter(model_field.is_(None))

                return record_set.filter(model_field == operator_value)

            elif operator == "$ne":
                return record_set.filter(model_field != operator_value)

            elif operator == "$lt":
                return record_set.filter(model_field < operator_value)

            elif operator == "$lte":
                return record_set.filter(
                    or_(
                        model_field < operator_value,
                        model_field == operator_value
                    )
                )
            elif operator == "$gt":
                return record_set.filter(model_field > operator_value)

            elif operator == "$gte":
                return record_set.filter(
                    or_(
                        model_field > operator_value,
                        model_field == operator_value
                    )
                )

            elif operator == "$nin":
                return record_set.filter(model_field.notin_(operator_value))

            elif operator == "$in":
                return record_set.filter(model_field.in_(operator_value))

            elif operator == "$lk":
                return record_set.filter(model_field.like(operator_value))

            elif operator == "$ilk":
                return record_set.filter(model_field.ilike(operator_value))

            elif operator == "$nlk":
                return record_set.filter(model_field.notlike(operator_value))

            elif operator == "$nilk":
                return record_set.filter(model_field.notilike(operator_value))

            elif operator == "$stw":
                return record_set.filter(model_field.startswith(operator_value))

            elif operator == "$edw":
                return record_set.filter(model_field.endswith(operator_value))

            elif operator == "$con":
                return record_set.filter(model_field.contains(operator_value))


def find_by_id(session_obj: SessionType, model_cls, _id, json_result=False):
    """This function is responsible for finding the instance of the model that
    is identified by value in the _id argument

    Arg(s)
    ------
    session_obj -> object used to interact with the database
    model_cls -> class representing instance of the model to be found
    _id -> id of the model to be found
    json_result -> indicates whether the found object used b returned as a
        dictionary or a raw instance

    Return(s)
    ---------
    returns raw instance or dictionary representing the raw instance based on
    json_result's value
    """
    return find_by_params(
        session_obj, model_cls, [{"id": {"$eq": _id}}], json_result)


def find_by_params(
        session_obj, model_cls, params: List[Dict], json_result=False):
    """This function is responsible for finding the instance of the model that
    is identified by filter parameters in params

    Arg(s)
    ------
    session_obj -> object used to interact with the database
    model_cls -> class representing instance of the model to be found
    params -> list of parameters to find a instance of the model class by
    json_result -> indicates whether the found object used b returned as a
        dictionary or a raw instance

    Return(s)
    ---------
    returns raw instance or dictionary representing the raw instance based on
    json_result's value
    """
    result = list_query(
        session_obj, model_cls, params, {"offset": 0, "limit": 1}, json_result)
    for row in result:
        return row


# def _apply_query_param_new(model_cls, record_set, params: Dict) -> bool:
#     """This function is responsible for applying a filter parameter to a
#     record set

#     Arg(s)
#     ------
#     model_cls -> class representing the model that the filter parameter must be
#         applied
#     record_set -> record set instance that the filter parameter must be applied
#     params (Dict) -> Dictionary that represents the filtering paramater that
#         must be applied

#     Return(s)
#     ---------
#     returns a new record set instance with the filtering parameter applied to it
#     """
#     is_view = hasattr(model_cls, 'select') and hasattr(model_cls, 'schema')
#     if is_view:
#         field_parent = getattr(model_cls, 'c')
#     else:
#         field_parent = model_cls

#     for field in params:
#         print(f"field => {field}")
#         for operator in params[field].keys():
#             operator_value = _convert_if_date(params[field][operator])
#             model_field = getattr(field_parent, field)
            
#             if operator == "$eq":

#                 if operator_value is None:
#                     return record_set.filter(model_field.is_(None))

#                 return record_set.filter(model_field == operator_value)

#             elif operator == "$ne":
#                 return record_set.filter(model_field != operator_value)

#             elif operator == "$lt":
#                 return record_set.filter(model_field < operator_value)

#             elif operator == "$lte":
#                 return record_set.filter(
#                     or_(
#                         model_field < operator_value,
#                         model_field == operator_value
#                     )
#                 )
#             elif operator == "$gt":
#                 return record_set.filter(model_field > operator_value)

#             elif operator == "$gte":
#                 return record_set.filter(
#                     or_(
#                         model_field > operator_value,
#                         model_field == operator_value
#                     )
#                 )

#             elif operator == "$nin":
#                 return record_set.filter(model_field.notin_(operator_value))

#             elif operator == "$in":
#                 return record_set.filter(model_field.in_(operator_value))

#             elif operator == "$lk":
#                 return record_set.filter(
#                     model_field.like(f"%{operator_value}%"))

#             elif operator == "$nlk":
#                 return record_set.filter(
#                     model_field.notlike(f"%{operator_value}%"))


def count(session_obj: SessionType, model_cls, params: List[Dict]=None):
    """This function is responsible for returning the number of instances of a 
    model match a list of filter parameters

    Arg(s):
    ------
    session_obj -> object used to interact with the database
    model_cls -> model classes whose instances we want to count
    params (List[Dict]) -> parameter to used to filter the instances to be
        counted

    Return(s):
    ----------
    dictionary representing the count of the instances that matched params
    """
    result = query(session_obj, model_cls, params, {})

    count_ = 0
    if result:
        count_ = result.count()

    return {'count': count_}
