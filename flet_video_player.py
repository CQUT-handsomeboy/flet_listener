"""
视频播放 主操作界面demo
"""

import flet as ft
import asyncio
from icecream import ic

from archive.td import caption_select, entry_select


def main(page: ft.Page):
    page.theme = ft.Theme(font_family="MiSans")
    page.window.full_screen = True

    rail = ft.NavigationRail(
        selected_index=0,
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
        # on_change=lambda e: print("Selected destination:", e.control.selected_index),
    )

    sample_media = [ft.VideoMedia("http://localhost:801")]

    create_card = lambda x, y: ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.ABC),
                        title=ft.Text(x),
                        subtitle=ft.Text(y),
                    )
                ]
            )
        )
    )

    async def check_and_show():
        nonlocal caption
        while True:
            await asyncio.sleep(1)
            t = await video.get_current_position_async()
            t /= 1000
            t = int(t)
            # print(t)
            caption_text = caption_select(t - 2, t)

            ret = entry_select(t, t)
            if ret is not None:
                entry_name, entry_explanation = ret
                card = create_card(entry_name, entry_explanation)
                cards.append(card)

            caption.content.content.controls[0].subtitle = ft.Text(caption_text)

            await page.update_async()

    page.run_task(check_and_show)

    caption_text = ft.Text("")

    caption = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.TRANSLATE),
                        title=ft.Text("实时字幕"),
                        subtitle=caption_text,
                    )
                ]
            ),
        ),
    )

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Row(
                    controls=[
                        ft.Column(
                            alignment=ft.alignment.top_center,
                            width=1100,
                            controls=[
                                video := ft.Video(
                                    show_controls=True,
                                    expand=True,
                                    playlist=sample_media,
                                    playlist_mode=ft.PlaylistMode.LOOP,
                                    fill_color=ft.colors.BLACK,
                                    aspect_ratio=16 / 9,
                                    volume=100,
                                    autoplay=True,
                                    filter_quality=ft.FilterQuality.HIGH,
                                    muted=False,
                                ),
                                caption,
                            ],
                        ),
                        ft.Column(
                            cards := [], scroll=True, auto_scroll=True, width=350
                        ),
                    ],
                ),
            ],
            expand=True,
        )
    )


import multiprocessing


def run_another_script():
    import archive.run_video_server as run_video_server

    run_video_server.main()


if __name__ == "__main__":
    p = multiprocessing.Process(target=run_another_script)
    p.start()
    ft.app(target=main)
