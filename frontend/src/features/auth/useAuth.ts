import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";

import { loginUser, registerUser } from "./api/auth.api";
import { useUser } from "./useUser";
import { useToken } from "./useToken";

export const useAuth = () => {

    const router = useRouter();

    const { setUser, getUser } = useUser();
    const { setAccessToken, setRefreshToken, getAccessToken, getRefreshToken } = useToken();

    const login = useMutation({
        mutationFn: loginUser,
        mutationKey: ["loginUser"],
        onSuccess: (data) => {
            // Saving the user
            setUser(data.user);

            // Saving the JWT tokens
            setAccessToken(data.token.access_token, data.token.expires_in)
            setRefreshToken(data.token.refresh_token, data.token.expires_in)

            // Redirect to home page
            router.push("/");
        },
        onError: (error) => {
            console.error("Login failed!", error);
        },
    });
    const register = useMutation({
        mutationFn: registerUser,
        mutationKey: ["registerUser"],
        onSuccess: (data) => {
            // Setting up the user
            setUser(data.user);

            // Saving the JWT tokens
            setAccessToken(data.token.access_token, data.token.expires_in);
            setRefreshToken(data.token.refresh_token, data.token.expires_in);

            // Redirect to home Page
            router.push("/");
        },
        onError: (error) => {
            console.error("Registration failed!", error);
        },
    });

    const currentUser = getUser();
    const access_token = getAccessToken();
    const refresh_token = getRefreshToken();

    return {
        login,
        register,
        currentUser,
        access_token,
        refresh_token
    };
};
