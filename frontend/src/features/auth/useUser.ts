"use client";

import { create } from "zustand";
import { getCookie, setCookie } from "cookies-next/client";

import { User } from "./api/auth.types";

interface UserState {
  user: User;
  setUser: (newUser: User) => void;
  getUser: () => User;
}

export const useUser = create<UserState>((set, get) => ({
  user: getCookie("user")
    ? (JSON.parse(getCookie("user") as string) as User)
    : { uuid: "", email: "", username: "" },
  setUser: (newUser: User) => {
    set({ user: newUser });

    setCookie("user", JSON.stringify(newUser), { maxAge: 60 * 60 * 24 * 7 });
  },
  getUser: () => get().user,
}));
