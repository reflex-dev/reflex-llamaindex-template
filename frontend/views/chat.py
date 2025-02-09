import reflex as rx
from frontend.components.badge import made_with_reflex
from frontend.state import State


def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        # Question
        rx.box(
            rx.markdown(
                question,
                class_name="[&>p]:!my-2.5",
            ),
            class_name="relative bg-slate-3 px-5 rounded-3xl max-w-[70%] text-slate-12 self-end",
        ),
        # Answer
        rx.box(
            rx.box(
                rx.image(
                    src="llama.svg",
                    class_name="h-6" + rx.cond(State.processing, " animate-pulse", ""),
                ),
            ),
            rx.box(
                rx.markdown(
                    answer,
                    class_name="[&>p]:!my-2.5",
                ),
                rx.box(
                    rx.el.button(
                        rx.icon(tag="copy", size=18),
                        class_name="p-1 text-slate-10 hover:text-slate-11 transform transition-colors cursor-pointer",
                        on_click=[rx.set_clipboard(answer), rx.toast("Copied!")],
                        title="Copy",
                    ),
                    class_name="-bottom-9 left-5 absolute opacity-0 group-hover:opacity-100 transition-opacity",
                ),
                class_name="relative bg-accent-4 px-5 rounded-3xl max-w-[70%] text-slate-12 self-start",
            ),
            class_name="flex flex-row gap-6",
        ),
        class_name="flex flex-col gap-8 pb-10 group",
    )


def chat() -> rx.Component:
    return rx.scroll_area(
        rx.foreach(
            State.chat_history,
            lambda messages: qa(messages[0], messages[1]),
        ),
        scrollbars="vertical",
        class_name="w-full",
    )


def action_bar() -> rx.Component:
    return rx.box(
        rx.form(
            rx.el.input(
                placeholder="Ask anything",
                name="question",
                class_name="box-border bg-slate-3 px-4 py-2 pr-14 rounded-full w-full outline-none focus:outline-accent-10 h-[48px] text-slate-12 placeholder:text-slate-9 peer",
            ),
            rx.el.button(
                rx.cond(
                    State.processing,
                    rx.icon(
                        tag="loader-circle",
                        size=19,
                        color="white",
                        class_name="animate-spin",
                    ),
                    rx.icon(tag="arrow-up", size=19, color="white"),
                ),
                class_name="top-1/2 right-4 absolute bg-accent-9 hover:bg-accent-10 disabled:hover:bg-accent-9 opacity-65 disabled:opacity-50 peer-placeholder-shown:opacity-50 p-1.5 rounded-full transition-colors -translate-y-1/2 cursor-pointer disabled:cursor-default peer-placeholder-shown:cursor-default",
                disabled=rx.cond(State.processing, True, False),
            ),
            on_submit=State.answer,
            class_name="relative w-full",
            reset_on_submit=True,
        ),
        # Made with Reflex link
        made_with_reflex(),
        class_name="flex flex-col justify-center items-center gap-6 w-full",
    )
