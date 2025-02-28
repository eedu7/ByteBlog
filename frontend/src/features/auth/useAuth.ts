import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";

import { loginUser, registerUser } from "./api/auth.api";
import { useStore } from "./useUser";

export const useAuth = () => {

    const router = useRouter();

    const { setUser, getUser } = useStore();

    const login = useMutation({
        mutationFn: loginUser,
        mutationKey: ["loginUser"],
        onSuccess: (data) => {
            console.log("Login successful!");
            console.table(data.token.expires_in);
            console.table(data.user);

            // Setting up the user
            setUser(data.user);

            // 
            console.log("###");
            console.log("###");
            console.log(getUser());
            console.log("###");
            console.log("###");
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
            console.log("Register successful!");
            console.table(data.token);
            console.table(data.user);

            // Setting up the user
            setUser(data.user);

            // Redirect to home Page
            router.push("/");
        },
        onError: (error) => {
            console.error("Registration failed!", error);
        },
    });

    const currentUser = getUser();

    return {
        login,
        register,
        currentUser,
    };
};
