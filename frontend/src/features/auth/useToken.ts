"use client";

import { create } from "zustand";
import { getCookie, setCookie } from "cookies-next/client";

interface TokenState {
  access_token: string;
  refresh_token: string;
  setAccessToken: (token: string, expires_in: number) => void;
  setRefreshToken: (token: string, expires_in: number) => void;
  getAccessToken: () => string | null;
  getRefreshToken: () => string | null;
}

export const useToken = create<TokenState>((set, get) => ({
  access_token: "",
  refresh_token: "",

  setAccessToken: (token: string, expires_in: number) => {
    set({ access_token: token });
    setCookie("access_token", token, {
      maxAge: expires_in,
      secure: true,
      sameSite: "strict",
    });
  },

  setRefreshToken: (token: string, expires_in: number) => {
    set({ refresh_token: token });
    setCookie("refresh_token", token, {
      maxAge: expires_in,
      secure: true,
      sameSite: "strict",
    });
  },

  getAccessToken: () => {
    const access_token = get().access_token;
    return access_token || (getCookie("access_token") as string | null);
  },

  getRefreshToken: () => {
    const refresh_token = get().refresh_token;
    return refresh_token || (getCookie("refresh_token") as string | null);
  },
}));
