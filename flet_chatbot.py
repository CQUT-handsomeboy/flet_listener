"""
对话机器人demo
"""

import flet as ft
import asyncio
from icecream import ic
from random import randint

get_chat_card = lambda x, y, z: ft.Card(
    content=ft.Container(
        content=ft.Column(
            [
                ft.ListTile(
                    leading=ft.CircleAvatar(
                        content=ft.Icon(
                            ft.icons.BOLT if z == "bot" else ft.icons.PERSON_2
                        )
                    ),
                    title=ft.Text(x),
                    subtitle=ft.Text(y),
                )
            ]
        ),
        padding=5,
    )
)


def main(page: ft.Page):
    page.theme = ft.Theme(font_family="MiSans")
    page.window.full_screen = True

    rail = ft.NavigationRail(
        selected_index=3,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=100,
        min_extended_width=400,
        leading=ft.FloatingActionButton(icon=ft.icons.SETTINGS, text="通用设置"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.TV,
                selected_icon=ft.icons.TV,
                label="观看直播",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.BOOK_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.BOOK),
                label="疑难收藏",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.PERSON_OUTLINE,
                selected_icon_content=ft.Icon(ft.icons.PERSON),
                label_content=ft.Text("个人信息"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.CHAT_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.CHAT),
                label_content=ft.Text("课堂助手"),
            ),
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
    )

    chat_col = ft.Column(
        controls=[],
        height=900,
        scroll=True,
        auto_scroll=True,
    )

    user_send = False  # 用户发送标志位，每一次用户发送以后，将此标志位置1，由此判断是否是用户发送

    async def send_message(e):
        nonlocal textfield
        value = textfield.value
        c = get_chat_card("用户", textfield.value, 0)
        chat_col.controls.append(c)
        textfield.value = ""
        page.update()
        meta = {
            "这节": "这是一个叫做智领未来智谋教育追踪摄像系统的项目，教师首先介绍了该系统的基本原理与实现过程"
            "，然后向我们演示了核心功能，总而言之，该系统通过创新性地集成边缘计算、流媒体传输等多个领域的技术，"
            "大大提升了教师的教学体验。",
            "你好": "你好，我是你的课堂助手，我能帮你概括课堂的主要内容，有什么问题尽管问题！",
        }
        await asyncio.sleep(1 + randint(500, 1000) / 500)
        if len(value) < 2 or (value[:2] not in meta):
            return
        k = value[:2]
        chat_col.controls.append(get_chat_card("课堂助手", meta[k], "bot"))
        await page.update_async()

    chat_textfield_row = ft.Row(
        controls=[
            textfield := ft.TextField(label="与课堂助手对话", width=1400),
            ft.IconButton(
                ft.icons.SEND,
                icon_color=ft.colors.GREEN,
                width=50,
                on_click=send_message,
            ),
        ],
    )

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Column(
                    controls=[chat_col, chat_textfield_row],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    width=1450,
                ),
            ],
            expand=True,
        )
    )


ft.app(main)
