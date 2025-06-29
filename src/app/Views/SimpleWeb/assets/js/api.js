export const api = new class {
    async act(params = {}) {
        const _url = new URL(location.href)
        _url.pathname = '/api/act'

        const postData = new FormData()

        Object.entries(params).forEach(n => {
            postData.set(n[0], n[1])
        })

        let data = await fetch(_url, {
            method: 'POST',
            body: postData
        })

        return await data.json()
    }

    async executable(type, name, args) {
        switch(type) {
            case "representation":
                args['i'] = "Executables.RunRepresentation"
                args['representation'] = name
                break
            case "act":
                args['i'] = name
                break
            case "extractor":
                args['i'] = "Executables.RunExtractor"
                args['extractor'] = name
                break
        }

        return await this.act(args)
    }
}

export default api
