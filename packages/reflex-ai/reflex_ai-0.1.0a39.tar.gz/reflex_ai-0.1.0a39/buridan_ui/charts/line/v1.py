import reflex as rx
from ..style import tooltip_styles

from typing import Any

def linechart_v1(
    data: rx.Var[list[dict[str, Any]]],
    x: rx.Var[str],
    y: str | list[str] | rx.Var[str] | rx.Var[list[str]],
    x_label: rx.Var[str] | None = None,
    y_label: rx.Var[str] | None = None,
    color: str | list | rx.Var[str] | rx.Var[list[str]] | None = None,
    # height: rx.Var[int] = rx.Var.create(250), # Need reflex change to bring this in...
) -> rx.Component:
    """Graph data in a line chart.

    Example usage:
    class State(rx.State):
        # INCLUDE FULL TYPE ANNOTATION!
        data: list[dict[str, Any]] = [
            {"name": "John", "age": 30, "city": "New York"},
        ]
    ...

    # Always prefer to hook up to state!
    linechart_v1(data=State.data, x="name", y=["age"], x_label="Name")
    """
    # Convert y to a list[Var]
    if isinstance(y, str):
        y = [y]

    if isinstance(y, rx.vars.StringVar):
        y = rx.Var.create([y])

    if not isinstance(y, rx.Var):
        y = rx.Var.create(y)

    # Convert color to a list[Var]
    if isinstance(color, str):
        color = [color]

    if isinstance(color, rx.vars.StringVar):
        color = rx.Var.create([color])

    if color is not None and not isinstance(color, rx.Var):
        color = rx.Var.create(color)

    return rx.center(
        rx.vstack(
            rx.recharts.line_chart(
                rx.recharts.graphing_tooltip(**vars(tooltip_styles)),
                rx.recharts.cartesian_grid(),
                rx.foreach(
                    y,
                    lambda name, index: rx.recharts.line(
                        data_key=name,
                        stroke=(
                            color[index]
                            if color is not None
                            else rx.color("accent", 8 + index)
                        ),
                        fill=(
                            color[index]
                            if color is not None
                            else rx.color("accent", 8 + index)
                        ),
                        stroke_width=3,
                        dot=False,
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
                custom_attrs={
                    "overflow": "visible",
                },
            ),
            width="100%",
        ),
        width="100%",
    )
