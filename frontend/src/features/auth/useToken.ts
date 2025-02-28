import { create } from "zustand";
import { Token } from "./api/auth.types";

interface TokenState {
    token: Token;
    setToken: (newToken: Token) => void;
    getToken: () => Token

}

export const useToken = create<TokenState>((set, get) => ({
    token: {
        access_token: "",
        refresh_token: "",
        expires_in: 0,
        token_type: "bearer"
    },
    setToken: () => (newToken: Token) => set({ token: newToken }),
    getToken: () => get().token,
}))