import http from "../http-common"

class DataService {
    getAll() {
        return http.get("/v2/pages/?type=core.CorePage&fields=intro,body,id,date")
    }
}

export default new DataService()