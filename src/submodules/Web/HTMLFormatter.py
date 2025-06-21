class HTMLFormatter():
    def __init__(self):
        pass

    @staticmethod
    def removeInlineJS(soup):
        for tag in soup.find_all(True):
            js_attributes = [attr for attr in tag.attrs if attr.startswith('on')]
            for attr in js_attributes:
                del tag[attr]

    @staticmethod
    def removeScriptTags(soup):
        for script_tag in soup.find_all('script'):
            script_tag.decompose()

    @staticmethod
    def removeOverflowY(soup):
        for tag in soup.find_all(style=True):
            styles = tag['style'].split(';')
            styles = [style for style in styles if not style.strip().startswith('overflow-y:')]
            tag['style'] = '; '.join(styles).strip()

    @staticmethod
    def findAllIMG(soup):
        return soup.find_all('img', src=True)

    @staticmethod
    def findAllScripts(soup):
        return soup.find_all('script', src=True)

    @staticmethod
    def findAllHrefs(soup):
        return soup.find_all(True,href=True)    

    @staticmethod
    def findAllLinks(soup):
        return soup.find_all('link', href=True)

    @staticmethod
    def srcToBase(url, base):
        if not url.startswith('http'):
            url = base + url

    @staticmethod
    def parseMeta(soup):
        # TODO parse "article" "nav" tags or smthng
        final_meta = {}
        for meta in soup.find_all('meta'):
            meta_name = meta.get('name')
            meta_content = meta.get('content')
            if meta_name == None:
                meta_name = meta.get('property')

            final_meta[meta_name] = meta_content

        return final_meta
