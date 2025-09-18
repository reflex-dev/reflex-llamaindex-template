import reflex as rx
from frontend.style import create_colors_dict

config = rx.Config(
    app_name="frontend",
    api_url="http://localhost:9000",
    backend_port=9000,
    deployment_name="deployment",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV3Plugin(
            {
                "darkMode": "class",
                "theme": {
                    "colors": {
                        **create_colors_dict(),
                    },
                },
            }
        ),
    ],
)
