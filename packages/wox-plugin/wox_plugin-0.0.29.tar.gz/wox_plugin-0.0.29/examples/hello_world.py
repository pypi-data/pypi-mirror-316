from typing import List
from wox_plugin import (
    BasePlugin,
    Context,
    Query,
    Result,
    WoxImage,
    WoxImageType,
    PluginInitParams,
)


class HelloWorldPlugin(BasePlugin):
    """A simple hello world plugin for Wox"""

    async def init(self, ctx: Context, init_params: PluginInitParams) -> None:
        """Initialize the plugin"""
        self.api = init_params.API

    async def query(self, ctx: Context, query: Query) -> List[Result]:
        """Handle user query"""
        return [
            Result(
                Title="Hello World",
                SubTitle=f"You typed: {query.Search}",
                Icon=WoxImage(ImageType=WoxImageType.EMOJI, ImageData="👋"),
                Action=self.api.open_url("https://wox-launcher.com"),
            )
        ]
