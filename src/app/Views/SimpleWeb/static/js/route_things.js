class MainFrameController {
    renderMainTemplate() {
        u('body').append(`
            <div id="frame">
                <div id="upper_tabs"></div>

                <div class="frame_content"></div>
            </div>

            <div id="other">
                <b style="margin-left: 5px">preth v0.0</b>

                <nav id="right_nav_panel">
                    <a data-tab="exec" href="#executables">Executables</a>
                    <a data-tab="list" href="#list">List</a>
                </nav>
            </div>
        `)
    }
}

router = new class {
    url = null
    list = [
        {
            'route': 'executables',
            'method': (new ExecutablePageController).act_page
        },
        {
            'route': 'executables_list',
            'method': (new ExecutablePageController).list_page
        },
        {
            'route': 'executable',
            'method': (new ExecutablePageController).exec_page
        },
        {
            'route': 'list',
            'method': (new ListPageController).list
        },
    ]

    __findRoute(hash) {
        let fnl = null

        this.list.forEach(item => {
            if(item.route == hash) {
                fnl = item
            }
        })

        return fnl
    }

    async route(path) {
        const _url = new HashURL(path)
        this.url = _url
        const _hash = _url.getHash().replace('#', '')
        let route = this.__findRoute(_hash)

        if (route == null) {
            route = this.__findRoute('executables')
        }

        let controller_method = route.method
        upper_tabs_controller.setHtml('')
        await controller_method()
    }
}

navigation_controller = new class {
    setTab(tab) {
        u('#right_nav_panel a').removeClass('selected')
        u(`#right_nav_panel a[data-tab="${tab}"]`).addClass('selected')
    }
}

upper_tabs_controller = new class {
    setHtml(html) {
        u('#upper_tabs').html(html)
    }

    setTab(tab) {
        u(`#upper_tabs .tab[data-name="${tab}"]`).addClass('selected')
    }
}

class HashURL extends URL {
    constructor(url) {
        super(url)
        this.hashParams = new URLSearchParams(this.hash.slice(1).split('?')[1] || '')
    }

    getParam(name, def = null) {
        return this.hashParams.get(name) ?? def
    }

    setParam(name, value) {
        this.hashParams.set(name, value)
        this._updateParams()
    }

    _updateParams() {
        let [path, ] = this.hash.slice(1).split('?')
        let newHash = path;
        const params = this.hashParams.toString()

        if(params) {
            newHash += '?' + params;
        }

        this.hashParams = new URLSearchParams(newHash.slice(1).split('?')[1] || '')
        this.hash = newHash;
    }

    hasParam(name) {
        return Boolean(this.hashParams.get(name))
    }

    deleteParam(name) {
        this.hashParams.delete(name)
        this._updateParams()
    }

    getParams() {
        return this.hashParams
    }

    getHash() {
        return this.hash.replace('#', '').replace('?' + this.hashParams.toString(), '')
    }
}

window.addEventListener("hashchange", async (event) => {
    await router.route(event.newURL)
})

main_controller = new MainFrameController()
main_controller.renderMainTemplate()

caches = {}

router.route(location.href)
