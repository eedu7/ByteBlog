import { axiosClient } from "@/services/api";
import {
    AuthResponse,
    LoginUserRequest,
    RegisterUserRequest,
} from "./auth.types";

export const registerUser = async (
    data: RegisterUserRequest
): Promise<AuthResponse> => {
    try {
        const response = await axiosClient.post("/auth/register", data);
        return response.data;
    } catch (error) {
        console.error("User registration failed!", error);
        throw new Error("User registration failed!");
    }
};

export const loginUser = async (
    data: LoginUserRequest
): Promise<AuthResponse> => {
    try {
        const response = await axiosClient.post("/auth/login", data);
        return response.data;
    } catch (error) {
        console.error("User login failed!", error);
        throw new Error("User login failed!");
    }
};
