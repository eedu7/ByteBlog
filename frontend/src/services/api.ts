import axios from "axios";

import { useToken } from "@/features/auth/useToken";

export const axiosClient = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
  },
});

axiosClient.interceptors.request.use(
  (config) => {
    const { getAccessToken } = useToken.getState();

    const access_token = getAccessToken();

    if (access_token) {
      config.headers["Authorization"] = `Bearer ${access_token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
