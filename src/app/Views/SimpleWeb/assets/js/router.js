import app from "./main.js"
import routes from "./utils/routes.js"
import HashURL from "./utils/HashURL.js"

export const router = new class {
    url = null
    list = routes

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

        app.navigation.setTab(_hash)
        app.setSideContent('')
        controller.loader()
        await controller[route.method]()
    }
}

window.addEventListener("hashchange", async (event) => {
    await router.route(event.newURL)
})

window.addEventListener("DOMContentLoaded", async () => {
    await router.route(location.href)
})

export default router
