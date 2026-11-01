import reflex as rx
from reflex_base.constants.installer import PackageJson

# Reflex 0.10.0 pins vite 8.3.2 (GHSA-587h-7wmj-h5pm, GHSA-r825-w8mm-5pxw, GHSA-698v-4r3x-3vcv) and
# re-applies its pins on every install, so raise it here. Drop this once Reflex pins >= 8.3.3.
PackageJson.DEV_DEPENDENCIES["vite"] = "8.3.4"

config = rx.Config(
    app_name="silverpoint_react_demo",
    # @silverpoint/react 0.9.0's SpDeck destroys its controller in an effect cleanup but keeps it in
    # useState, so React's StrictMode double-mount (development only) leaves the deck inert: no
    # navigation, no events. Production builds are unaffected. Reported upstream; drop this line
    # once silverpoint ships the fix (see the README, "Known issues").
    react_strict_mode=False,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(theme=rx.theme(appearance="light", accent_color="gray", radius="small")),
    ],
)
