import flet as ft

def main(page: ft.Page):
    page.title = "Email Client"
    page.padding = 0
    
    def toolbar_item(icon, text):
        return ft.Container(
            content=ft.Column(
                [
                    ft.IconButton(
                        icon=icon,
                        icon_color="grey",
                        icon_size=20,
                    ),
                    ft.Text(text, size=12, color="grey")
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            padding=ft.padding.only(right=10),
        )

    # Top toolbar
    toolbar = ft.Container(
        content=ft.Row(
            [
                ft.Text("Email Client", color="white", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.TextField(
                        hint_text="Search",
                        border_radius=20,
                        filled=True,
                        expand=True,
                    ),
                    expand=True,
                    padding=10,
                ),
            ],
        ),
        bgcolor="#3EA68B",
        padding=10,
    )

    # Action buttons
    action_buttons = ft.Container(
        content=ft.Row(
            [
                ft.ElevatedButton(
                    "New mail",
                    icon=ft.icons.EDIT,
                    bgcolor="#3EA68B",
                    color="white",
                ),
                toolbar_item(ft.icons.DELETE, "Delete"),
                toolbar_item(ft.icons.ARCHIVE, "Archive"),
                toolbar_item(ft.icons.MARK_EMAIL_READ, "Mark read"),
                toolbar_item(ft.icons.MOVE_TO_INBOX, "Move to"),
            ],
        ),
        padding=10,
    )

    # Email list view
    def create_email_item(sender, subject, preview, time):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.CircleAvatar(
                                content=ft.Text(sender[0].upper()),
                                bgcolor=ft.colors.BLUE_200,
                                radius=20,
                            ),
                            ft.Column(
                                [
                                    ft.Text(sender, weight=ft.FontWeight.BOLD),
                                    ft.Text(subject),
                                    ft.Text(preview, color="grey", size=12),
                                ],
                                expand=True,
                            ),
                            ft.Text(time, color="grey", size=12),
                        ]
                    ),
                    ft.Divider(height=1),
                ]
            ),
            padding=10,
        )

    # Sidebar navigation
    sidebar = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        height=page.height,
        bgcolor=ft.colors.BLUE_GREY_50,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.INBOX_OUTLINED,
                selected_icon=ft.icons.INBOX,
                label="Inbox",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.STAR_OUTLINE,
                selected_icon=ft.icons.STAR,
                label="Starred"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SEND_OUTLINED,
                selected_icon=ft.icons.SEND,
                label="Sent"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.DELETE_OUTLINE,
                selected_icon=ft.icons.DELETE,
                label="Trash"
            ),
        ],
    )

    # Main content
    content = ft.Column(
        [
            toolbar,
            action_buttons,
            ft.Tabs(
                selected_index=0,
                tabs=[
                    ft.Tab(text="Focused"),
                    ft.Tab(text="Other"),
                ],
            ),
            ft.Column(
                [
                    create_email_item(
                        "Red Nacional", 
                        "Consumo de servicio eléctrico",
                        "Estimado Cliente, le informamos hemos procesado...",
                        "Fri 0:09"
                    ),
                    create_email_item(
                        "PDL Services", 
                        "Documento electrónico",
                        "Estimado(a) cliente: Acaba de recibir su documen...",
                        "Wed 30-Oct"
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
        ],
        spacing=0,
    )

    # Main layout
    page.add(
        ft.Row(
            [
                sidebar,
                ft.VerticalDivider(width=1),
                content,
            ],
            expand=True,
        )
    )

ft.app(target=main)