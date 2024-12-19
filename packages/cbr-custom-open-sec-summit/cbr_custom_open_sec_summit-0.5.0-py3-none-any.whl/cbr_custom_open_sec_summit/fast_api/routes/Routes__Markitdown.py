import cbr_custom_open_sec_summit
from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes
from osbot_utils.utils.Files            import path_combine, file_exists

ROUTES_PATHS__MARKITDOWN = ['/markitdown/markitdown-pdf',  '/markitdown/markitdown-xslx']

class Routes__Markitdown(Fast_API_Routes):
    tag :str = 'markitdown'

    def markitdown(self, target_file):
        from markitdown import MarkItDown
        path_test_file = path_combine(cbr_custom_open_sec_summit.path, target_file)
        if file_exists(path_test_file):
            md     = MarkItDown()
            result = md.convert(path_test_file)
            return result.text_content

    def markitdown_pdf(self):
        file__pdf = 'fast_api/routes/sample.pdf'
        return self.markitdown(file__pdf)

    def markitdown_xslx(self):
        file__xlsx = 'fast_api/routes/test.xlsx'
        return self.markitdown(file__xlsx)




    def setup_routes(self):
        self.add_route_get(self.markitdown_pdf)
        self.add_route_get(self.markitdown_xslx)