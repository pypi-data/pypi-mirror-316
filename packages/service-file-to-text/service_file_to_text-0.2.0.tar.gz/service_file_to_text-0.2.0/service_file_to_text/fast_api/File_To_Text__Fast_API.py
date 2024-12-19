from osbot_fast_api.api.Fast_API                                     import Fast_API
from service_file_to_text.fast_api.routes.Routes__Info         import Routes__Info
from service_file_to_text.markitdown.routes.Routes__Markitdown import Routes__Markitdown


class File_To_Text__Fast_API(Fast_API):
    base_path  : str  = '/'
    enable_cors: bool = True

    def setup_routes(self):
        self.add_routes(Routes__Info)
        self.add_routes(Routes__Markitdown)

