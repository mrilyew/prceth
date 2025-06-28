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
}

export default api
