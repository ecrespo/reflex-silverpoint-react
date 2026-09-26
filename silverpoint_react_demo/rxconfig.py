import reflex as rx

config = rx.Config(
    app_name="silverpoint_react_demo",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(theme=rx.theme(appearance="light", accent_color="gray", radius="small")),
    ],
)
