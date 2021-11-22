import http from "../http-common"

class DataService {
    getAll() {
        return http.get("/api/v2/pages/?type=core.CorePage&fields=intro,body,id,date")
    }

    getBaseURL() {
        return http.defaults.baseURL
    }
}

export default new DataService()