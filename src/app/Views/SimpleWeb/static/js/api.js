api = new class {
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
}

runner = new class {
    async run(type, class_name, args) {
        let act_name = null

        switch(type) {
            case 'extractor':
                act_name = 'Executables.RunExtractor'
                args['extractor'] = class_name
                break
            case 'act':
                act_name = null
                break
            case 'representation':
                act_name = 'Executables.RunRepresentation'
                args['representation'] = class_name
                break
        }

        if(act_name != null) {
            args['i'] = act_name
        }

        return await api.act(args)
    }
}
