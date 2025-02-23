import { LoginUser, RegisterUser } from "./api/auth.mutation";

export const useAuth = () => {
    const login = LoginUser();
    const register = RegisterUser();

    return {
        login,
        register,
    };
};
