import reflex as rx

from ..style import tooltip_styles
from typing import Any

def barchart_v1(
    data: rx.Var[list[dict[str, Any]]],
    x: rx.Var[str],
    y: str | list[str] | rx.Var[str] | rx.Var[list[str]],
    x_label: rx.Var[str] | None = None,
    y_label: rx.Var[str] | None = None,
    color: str | list | rx.Var[str] | rx.Var[list[str]] | None = None,
    # height: rx.Var[int] = rx.Var.create(250),
):
    """Graph data in a bar chart.

    Example usage:
    class State(rx.State):
        # INCLUDE FULL TYPE ANNOTATION!
        data: list[dict[str, Any]] = [
            {"name": "John", "age": 30, "city": "New York"},
        ]
    ...

    # Always prefer to hook up to state!
    barchart_v1(data=State.data, x="name", y=["age"], x_label="Name")
    """

    return rx.center(
        rx.vstack(
            rx.recharts.bar_chart(
                rx.recharts.graphing_tooltip(**vars(tooltip_styles)),
                rx.recharts.cartesian_grid(),
                rx.foreach(
                    y,
                    lambda name, index: rx.recharts.bar(
                        data_key=name,
                        fill=(
                            color[index]
                            if color is not None
                            else rx.color("accent", 8 + index)
                        ),
                    ),
                ),
                rx.recharts.x_axis(
                    rx.recharts.label(
                        position="bottom",
                        value=rx.cond(x_label, x_label, x),
                    ),
                    data_key=x,
                    tick_line=False,
                ),
                rx.recharts.y_axis(
                    rx.recharts.label(
                        value=rx.cond(y_label, y_label, y[0]),
                        position="left",
                        custom_attrs={
                            "angle": -90,
                        },
                    ),
                    tick_line=False,
                ),
                data=data,
                width="100%",
                min_height=250,
                max_bar_size=50,
                bar_gap=2,
                custom_attrs={
                    "overflow": "visible",
                },
            ),
            width="100%",
        ),
        width="100%",
    )
