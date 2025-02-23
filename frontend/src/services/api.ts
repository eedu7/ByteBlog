import axios from "axios";

export const axiosClient = axios.create({
    baseURL: "http://localhost:8000",
    timeout: 5000,
    headers: {
        "Content-Type": "application/json",
    },
});
