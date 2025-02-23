import { useMutation } from "@tanstack/react-query";

import { loginUser, registerUser } from "./auth.api";

export const LoginUser = () => {
    return useMutation({
        mutationFn: loginUser,
        mutationKey: ["loginUser"],
        onSuccess: (data) => {
            console.log("Login successful!");
            console.table(data.token);
            console.table(data.user);
        },
        onError: (error) => {
            console.error("Login failed!", error);
        },
    });
};

export const RegisterUser = () => {
    return useMutation({
        mutationFn: registerUser,
        mutationKey: ["registerUser"],
        onSuccess: (data) => {
            console.log("Register successful!");
            console.table(data.token);
            console.table(data.user);
        },
        onError: (error) => {
            console.error("Registration failed!", error);
        },
    });
};
