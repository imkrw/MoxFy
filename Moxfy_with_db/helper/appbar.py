from flet import *


def create_text_with_span(text, on_click):
    return Text(
        size=15,
        spans=[
            TextSpan(
                text,
                TextStyle(
                    decoration=TextDecoration.NONE,
                    font_family="poppins",
                    weight="w400",
                    size=15,
                ),
                on_enter=highlight,
                on_exit=unhighlight,
                on_click=on_click,
            )
        ],
    )


def create_app_bar(page, nameView, custom_text, destination, on_custom_text_click):
    custom = [create_text_with_span(custom_text, on_custom_text_click)]
    if destination:
        custom.append(create_text_with_span("Back", lambda e: page.go(destination)))

    return ResponsiveRow(
        [
            WindowDragArea(
                Container(
                    width=page.width,
                    height=45,
                    padding=5,
                    content=Row(
                        [
                            Text(f"You are viewing: {nameView}", size=15),
                            Container(
                                content=Row(
                                    [
                                        *custom,
                                    ]
                                )
                            ),
                        ],
                        alignment="spaceBetween",
                    ),
                ),
                maximizable=False,
            )
        ]
    )


def appbarLoginView(nameView, destination, page: Page, custom_text):
    return create_app_bar(
        page, nameView, custom_text, False, lambda e: page.go(destination)
    )


def appBarMainView(page: Page):
    return ResponsiveRow(
        [
            WindowDragArea(
                Container(
                    width=page.width,
                    height=45,
                    content=Row(
                        [
                            IconButton(
                                icon=icons.DARK_MODE_SHARP
                                if page.theme_mode == "LIGHT"
                                else icons.LIGHT_MODE_SHARP,
                                on_click=lambda e: toggletheme(page, e),
                                tooltip="Toggle theme",
                            ),
                            Text("Moxfy", weight="bold", size=18),
                            Container(
                                alignment=alignment.center_right,
                                content=Row(
                                    [
                                        Container(
                                            alignment=alignment.center_right,
                                            content=Row(
                                                [
                                                    PopupMenuButton(
                                                        items=[
                                                            PopupMenuItem(
                                                                icon=icons.PEOPLE,
                                                                text="Information",
                                                                on_click=lambda e: page.go(
                                                                    "/information"
                                                                ),
                                                            ),
                                                            PopupMenuItem(
                                                                icon=icons.AUTO_AWESOME,
                                                                text="Utilities",
                                                                on_click=lambda e: page.go(
                                                                    "/utils"
                                                                ),
                                                            ),
                                                            PopupMenuItem(
                                                                icon=icons.BUG_REPORT,
                                                                text="Report a bug",
                                                                on_click=lambda e: page.go(
                                                                    "/report"
                                                                ),
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ],
                        alignment="spaceBetween",
                    ),
                ),
                maximizable=False,
            )
        ]
    )


def appBarGeneralView(destination, page: Page, nameView):
    return create_app_bar(page, nameView, None, destination, None)


def highlight(e):
    e.control.style.color = colors.PINK_100
    e.control.update()


def unhighlight(e):
    e.control.style.color = None
    e.control.update()


def minimize(page: Page):
    page.window_minimized = True
    page.update()


def toggletheme(page: Page, e):
    if page.theme_mode == "dark":
        page.theme_mode = "light"
    else:
        page.theme_mode = "dark"
    page.update()
