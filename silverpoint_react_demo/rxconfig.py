import reflex as rx
from reflex_base.constants.installer import PackageJson

# Reflex 0.10.0 pins vite 8.3.2 (GHSA-587h-7wmj-h5pm, GHSA-r825-w8mm-5pxw, GHSA-698v-4r3x-3vcv) and
# re-applies its pins on every install, so raise it here. Drop this once Reflex pins >= 8.3.3.
PackageJson.DEV_DEPENDENCIES["vite"] = "8.3.4"

config = rx.Config(
    app_name="silverpoint_react_demo",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(theme=rx.theme(appearance="light", accent_color="gray", radius="small")),
    ],
)
