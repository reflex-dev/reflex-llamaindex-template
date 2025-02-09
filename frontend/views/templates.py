import reflex as rx
from frontend.state import State


def template_card(icon: str, title: str, description: str, color: str) -> rx.Component:
    return rx.el.button(
        rx.icon(tag=icon, color=rx.color(color, 9), size=16),
        rx.text(title, class_name="font-medium text-slate-11 text-sm"),
        rx.text(description, class_name="text-slate-10 text-xs"),
        class_name="relative align-top flex flex-col gap-2 border-slate-4 bg-slate-1 hover:bg-slate-3 shadow-sm px-3 pt-3 pb-4 border rounded-2xl text-[15px] text-start transition-colors",
        on_click=State.answer({"question": description}),
    )


def templates() -> rx.Component:
    return rx.box(
        rx.image(
            src="/reflex_x_llamaindex.svg",
            class_name="opacity-70 w-auto h-11 pointer-events-none",
        ),
        rx.box(
            template_card(
                "message-circle",
                "Ask a question",
                "What is the capital of France?",
                "grass",
            ),
            template_card(
                "calculator",
                "Solve a math problem",
                "What is the square root of 144?",
                "tomato",
            ),
            template_card(
                "globe",
                "Get a fun fact",
                "Tell me an interesting fact about dolphins.",
                "blue",
            ),
            template_card(
                "book",
                "Recommend a book",
                "What's a good mystery novel for beginners?",
                "amber",
            ),
            class_name="gap-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 w-full",
        ),
        class_name="top-1/2 lg:top-1/3 left-1/2 z-50 absolute flex flex-col justify-center items-center gap-10 px-6 w-full max-w-4xl transform -translate-x-1/2 -translate-y-1/2",
        style={
            "animation": "reveal 0.35s ease-out",
            "@keyframes reveal": {"0%": {"opacity": "0"}, "100%": {"opacity": "1"}},
        },
        display=rx.cond(State.chat_history, "none", "flex"),
    )
