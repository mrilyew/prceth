class WebUtils():
    def is_generated_ext(self, ext: str):
        return ext in ["php", "html"]

web_utils = WebUtils()
