import api from "../api.js"
import Model from "../models/Model.js"
import ExecutableViewModel from "../view_models/ExecutableViewModel.js"

class Executable extends Model {
    render_class = ExecutableViewModel

    static async getList(class_type) {
        const resp = await api.act({
            "i": "Executables.List",
            "class_type": class_type,
        })

        return Executable.fromArray(resp.payload)
    }
}

export default Executable
