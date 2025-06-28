import api from "../api.js"
import Model from "../models/Model.js"
import ExecutableViewModel from "../view_models/ExecutableViewModel.js"
import ExecutableArgumentViewModel from "../view_models/ExecutableArgumentViewModel.js"

class ExecutableArgument extends Model {
    render_class = ExecutableArgumentViewModel

    get type() {
        return this.data.type
    }

    get name() {
        return this.data.name
    }

    get default() {
        return this.data.default
    }

    get docs() {
        return this.data.docs
    }

    get is_hidden() {
        return this.data.hidden == true
    }
}

class Executable extends Model {
    render_class = ExecutableViewModel

    static async getList(class_type) {
        const resp = await api.act({
            "i": "Executables.List",
            "class_type": class_type,
        })

        return Executable.fromArray(resp.payload)
    }

    static async getFromName(class_name) {
        const its = class_name.split('.')
        const class_type = its[1].slice(0, -1)
        const class_id = its[2] + '.' + its[3]

        const resp = await api.act({
            'i': "Executables.Describe",
            "class_type": class_type,
            'class': class_id
        })

        return new Executable(resp.payload)
    }

    get category() {
        return this.data.category
    }

    get name() {
        return this.data.name
    }

    get sub() {
        return this.data.sub
    }

    get docs() {
        return this.data.docs
    }

    get args() {
        const args = this.data.args
        const f_ = []
        args.forEach(el => {
            f_.push(new ExecutableArgument(el))
        })

        return f_
    }
}

export default Executable
