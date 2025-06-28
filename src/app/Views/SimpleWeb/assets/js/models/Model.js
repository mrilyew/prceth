class Model {
    render_class = null

    constructor(data) {
        this.data = data
    }

    static fromArray(arr) {
        const f = []
        arr.forEach(el => {
            f.push(new this(el))
        })

        return f
    }

    render(args) {
        const data = this.data
        const _cl = new this.render_class()

        return _cl.template(data)
    }
}

export default Model
