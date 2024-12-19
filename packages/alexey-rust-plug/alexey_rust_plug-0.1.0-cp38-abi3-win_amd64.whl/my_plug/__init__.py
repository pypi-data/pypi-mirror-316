from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl
from polars.plugins import register_plugin_function

from my_plug._internal import __version__ as __version__

if TYPE_CHECKING:
    from my_plug.typing import IntoExprColumn

LIB = Path(__file__).parent

def add_suffix(expr: IntoExprColumn, *, suffix: str) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="add_suffix",
        is_elementwise=True,
        kwargs={"suffix": suffix},
    )

def my_str(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="my_str",
        is_elementwise=True,
    )

def my_str2(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="my_str2",
        is_elementwise=True,
    )

def pig_latinnify(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="pig_latinnify",
        is_elementwise=True,
    )

def my_abs2(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="my_abs2",
        is_elementwise=True,
    )

def my_abs5(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="my_abs5",
        is_elementwise=True,
    )

# def my_abs3(expr: IntoExprColumn) -> pl.Expr:
#     return register_plugin_function(
#         args=[expr],
#         plugin_path=LIB,
#         function_name="my_abs3",
#         is_elementwise=True,
#     )

# def my_abs4(expr: IntoExprColumn) -> pl.Expr:
#     return register_plugin_function(
#         args=[expr],
#         plugin_path=LIB,
#         function_name="my_abs4",
#         is_elementwise=True,
#     )

def my_sum_i64(expr: IntoExprColumn, other: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr, other],
        plugin_path=LIB,
        function_name="my_sum_i64",
        is_elementwise=True,
    )

def my_mult(expr: IntoExprColumn, other: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr, other],
        plugin_path=LIB,
        function_name="my_mult",
        is_elementwise=True,
    )

def my_rand(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="my_rand",
        is_elementwise=True,
    )

def my_rand2(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="my_rand2",
        is_elementwise=True,
    )

def max_in_list(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="max_in_list",
        is_elementwise=True,
    )



def foo3(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="foo3",
        is_elementwise=True,
    )

def list_between(expr: IntoExprColumn, expr2: IntoExprColumn, expr3: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr, expr2, expr3],
        plugin_path=LIB,
        function_name="list_between",
        is_elementwise=True,
    )

def list_between3(expr: IntoExprColumn, expr2: IntoExprColumn, expr3: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr, expr2, expr3],
        plugin_path=LIB,
        function_name="list_between3",
        is_elementwise=True,
    )

def list_between2(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="list_between2",
        is_elementwise=True,
    )

def regression(*expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=list(expr),
        plugin_path=LIB,
        function_name="regression",
        is_elementwise=True,
    )


def add(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="add",
        is_elementwise=True,
    )

def str_from_col(expr: IntoExprColumn, expr2: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr, expr2],
        plugin_path=LIB,
        function_name="str_from_col",
        is_elementwise=True,
    )

def str_from_col2(expr: IntoExprColumn, expr2: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr, expr2],
        plugin_path=LIB,
        function_name="str_from_col2",
        is_elementwise=True,
    )

def str_from_col3(expr: IntoExprColumn, expr2: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr, expr2],
        plugin_path=LIB,
        function_name="str_from_col3",
        is_elementwise=True,
    )

def max_date(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="max_date",
        is_elementwise=True,
    )

def my_sum(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="my_sum",
        is_elementwise=True,
    )

def my_sum2(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="my_sum2",
        is_elementwise=False,
    )

def my_sum3(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="my_sum3",
        is_elementwise=True,
    )

def my_sum4(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="my_sum4",
        is_elementwise=True,
    )

def my_sum5(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="my_sum5",
        is_elementwise=True,
    )

def my_sum6(expr: IntoExprColumn, expr2: IntoExprColumn, expr3: IntoExprColumn, expr4: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr, expr2, expr3, expr4],
        plugin_path=LIB,
        function_name="my_sum6",
        is_elementwise=True,
    )

def my_sum7(expr: IntoExprColumn, expr2: IntoExprColumn, expr3: IntoExprColumn, expr4: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr, expr2, expr3, expr4],
        plugin_path=LIB,
        function_name="my_sum7",
        is_elementwise=True,
    )

def my_sum8(expr: IntoExprColumn, expr2: IntoExprColumn, expr3: IntoExprColumn, expr4: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr, expr2, expr3, expr4],
        plugin_path=LIB,
        function_name="my_sum8",
        is_elementwise=True,
    )

