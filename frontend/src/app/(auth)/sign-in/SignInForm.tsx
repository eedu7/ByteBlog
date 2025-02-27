"use client";

import Link from "next/link";
import React from "react";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import { EyeIcon, EyeOffIcon, MailIcon } from "lucide-react";

import { loginFormSchema } from "@/features/auth/formSchema";
import useFormSchema from "@/features/auth/useFormSchema";
import { useAuth } from "@/features/auth/useAuth";

const SignInForm = () => {
    const [isVisible, setIsVisible] = React.useState<boolean>(false);

    const toggleVisibility = () => setIsVisible((prevState) => !prevState);

    const { loginForm } = useFormSchema();

    const { login } = useAuth();

    const onSubmit = (values: z.infer<typeof loginFormSchema>) => {
        login.mutate(values);
    };

    return (
        <Form {...loginForm}>
            <form
                onSubmit={loginForm.handleSubmit(onSubmit)}
                className="space-y-8">
                <FormField
                    control={loginForm.control}
                    name="email"
                    render={({ field }) => (
                        <FormItem>
                            <FormControl>
                                <div className="*:not-first:mt-2">
                                    <Label htmlFor="email">Email Address</Label>
                                    <div className="relative">
                                        <Input
                                            id="email"
                                            className="peer pe-9"
                                            placeholder="Email"
                                            type="email"
                                            {...field}
                                        />
                                        <div className="text-muted-foreground/80 pointer-events-none absolute inset-y-0 end-0 flex items-center justify-center pe-3 peer-disabled:opacity-50">
                                            <MailIcon
                                                size={16}
                                                aria-hidden="true"
                                            />
                                        </div>
                                    </div>
                                </div>
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={loginForm.control}
                    name="password"
                    render={({ field }) => (
                        <FormItem>
                            <FormControl>
                                <div className="*:not-first:mt-2">
                                    <Label htmlFor="password">Password</Label>
                                    <div className="relative">
                                        <Input
                                            id="password"
                                            className="pe-9"
                                            placeholder="Password"
                                            type={
                                                isVisible ? "text" : "password"
                                            }
                                            {...field}
                                        />
                                        <button
                                            className="text-muted-foreground/80 hover:text-foreground focus-visible:border-ring focus-visible:ring-ring/50 absolute inset-y-0 end-0 flex h-full w-9 items-center justify-center rounded-e-md transition-[color,box-shadow] outline-none focus:z-10 focus-visible:ring-[3px] disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50"
                                            type="button"
                                            onClick={toggleVisibility}
                                            aria-label={
                                                isVisible
                                                    ? "Hide password"
                                                    : "Show password"
                                            }
                                            aria-pressed={isVisible}
                                            aria-controls="password">
                                            {isVisible ? (
                                                <EyeOffIcon
                                                    size={16}
                                                    aria-hidden="true"
                                                />
                                            ) : (
                                                <EyeIcon
                                                    size={16}
                                                    aria-hidden="true"
                                                />
                                            )}
                                        </button>
                                    </div>
                                </div>
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <div className="flex justify-between">
                    <Button type="submit" disabled={login.isPending}>
                        {login.isPending ? "Loading..." : "Log In"}
                    </Button>
                    <Link
                        href="/sign-up"
                        className="text-sm text-blue-600 underline underline-offset-2 hover:text-blue-900 hover:scale-110 transition-transform">
                        Need an account? Register here
                    </Link>
                </div>
            </form>
        </Form>
    );
};

export default SignInForm;
