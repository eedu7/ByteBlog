import { z } from "zod";

export const registerFormSchema = z.object({
    username: z
        .string()
        .min(2, {
            message: "Username must be at least 2 characters.",
        })
        .max(20, {
            message: "Username must be at most 20 characters.",
        }),
    email: z.string().email(),
    password: z
        .string()
        .min(8, {
            message: "Password must be at least 8 characters.",
        })
        .max(16, {
            message: "Password must be at most 16 characters.",
        }),
});

export const loginFormSchema = z.object({
    email: z.string().email(),
    password: z
        .string()
        .min(8, { message: "Password must be at least 8 characters." })
        .max(16, { message: "Password must be at most 16 characters." }),
});
