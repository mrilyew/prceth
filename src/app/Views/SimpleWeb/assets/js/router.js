import _app from "../js/main.js"
import AboutController from "../js/controllers/about.js"
import ContentController from "../js/controllers/content.js"

export const router = new class {
    url = null
    list = [
        {
            'route': 'index',
            'class': (new AboutController),
            'method': 'main'
        },
        {
            'route': 'content',
            'class': (new ContentController),
            'method': 'main'
        },
        {
            'route': 'cu',
            'class': (new ContentController),
            'method': 'page'
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
            route = this.__findRoute('index')
        }

        let controller = route.class

        _app.navigation.setTab(_hash)
        controller.loader()
        await controller[route.method]()
    }
}

export class HashURL extends URL {
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

window.addEventListener("DOMContentLoaded", async () => {
    await router.route(location.href)
})

export default router
