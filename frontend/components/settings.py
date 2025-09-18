import reflex as rx
from reflex.style import set_color_mode, color_mode
from frontend.state import SettingsState
from frontend.components.hint import hint


def color_item(color: str) -> rx.Component:
    return rx.box(
        rx.box(
            rx.cond(
                SettingsState.color == color,
                rx.icon(tag="check", size=13, stroke_width="2.5", color="white"),
                rx.fragment(),
            ),
            class_name="flex justify-center items-center rounded-full w-5 h-5 shrink-0",
            style={
                "background": rx.color(color, 9),
            },
        ),
        rx.text(color.capitalize(), class_name="font-medium text-slate-12 text-sm"),
        class_name="box-border flex items-center gap-2 bg-slate-1 hover:bg-slate-3 shadow-sm px-3 rounded-md h-8 transition-bg cursor-pointer",
        outline=rx.cond(
            SettingsState.color == color,
            f"2px solid {rx.color('slate', 12)}",
            f"1px solid {rx.color('slate', 6)}",
        ),
        on_click=SettingsState.set_color(color),
    )


def font_item(font: str) -> rx.Component:
    return rx.box(
        rx.text(
            font,
            class_name="font-medium text-slate-12 text-sm truncate",
            title=font,
            font_family=font,
        ),
        class_name="box-border flex items-center gap-2 bg-slate-1 hover:bg-slate-3 shadow-sm px-3 rounded-md h-8 transition-bg cursor-pointer",
        outline=rx.cond(
            SettingsState.font_family == font,
            f"2px solid {rx.color('slate', 12)}",
            f"1px solid {rx.color('slate', 6)}",
        ),
        on_click=SettingsState.set_font_family(font),
    )


def settings_icon() -> rx.Component:
    colors = ["violet", "amber", "green", "blue", "orange", "red"]
    fonts = ["Instrument Sans", "Poppins", "Inter", "Lato", "Roboto", "Open Sans"]

    return rx.popover.root(
        rx.popover.trigger(
            rx.box(
                hint(
                    text="Settings",
                    content=rx.box(
                        rx.icon(
                            tag="settings",
                            size=22,
                            stroke_width="1.5",
                            class_name="!text-slate-10",
                        ),
                        class_name="group-data-[state=open]:bg-slate-3 group-hover:bg-slate-3 p-2 rounded-xl transition-colors cursor-pointer",
                    ),
                    side="bottom",
                ),
                class_name="group",
            ),
        ),
        rx.popover.content(
            rx.box(
                # Accent Color
                rx.box(
                    rx.text(
                        "Accent Color",
                        class_name="font-medium text-base text-slate-12",
                    ),
                    rx.box(
                        *[color_item(color) for color in colors],
                        class_name="gap-3 grid grid-cols-2",
                    ),
                    class_name="flex flex-col gap-2",
                ),
                # Font Family
                rx.box(
                    rx.text(
                        "Font Family",
                        class_name="font-medium text-base text-slate-12",
                    ),
                    rx.box(
                        *[font_item(font) for font in fonts],
                        class_name="gap-3 grid grid-cols-2",
                    ),
                    class_name="flex flex-col gap-2",
                ),
                # Theme
                rx.box(
                    rx.text(
                        "Theme",
                        class_name="font-medium text-base text-slate-12",
                    ),
                    rx.segmented_control.root(
                        rx.segmented_control.item(
                            rx.icon(tag="monitor", size=20),
                            value="system",
                            class_name="cursor-pointer",
                        ),
                        rx.segmented_control.item(
                            rx.icon(tag="sun", size=20),
                            value="light",
                            class_name="cursor-pointer",
                        ),
                        rx.segmented_control.item(
                            rx.icon(tag="moon", size=20),
                            value="dark",
                            class_name="cursor-pointer",
                        ),
                        on_change=set_color_mode,
                        variant="classic",
                        radius="large",
                        value=color_mode,
                    ),
                    class_name="flex flex-col gap-2",
                ),
                class_name="flex flex-col gap-8 border-slate-5 bg-slate-1 shadow-lg px-[0.875rem] py-4 border border-box rounded-xl overflow-hidden",
            ),
            side="top",
            align="center",
            avoid_collisions=True,
            class_name="items-center bg-transparent !shadow-none !p-0 border-none w-[254px] overflow-visible",
            font_family="var(--font-family)",
        ),
    )
