"use client";

import { z } from "zod";

import { Button } from "@/components/ui/button";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";

import type { loginFormSchema } from "@/features/auth/formSchema";
import useFormSchema from "@/features/auth/useFormSchema";
import Link from "next/link";

const SignInForm = () => {
    const { loginForm } = useFormSchema();

    const onSubmit = (values: z.infer<typeof loginFormSchema>) => {
        console.table(values);
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
                            <FormLabel>Email Address</FormLabel>
                            <FormControl>
                                <Input
                                    placeholder="john.doe@example.com"
                                    type="email"
                                    {...field}
                                />
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
                            <FormLabel>Password</FormLabel>
                            <FormControl>
                                <Input
                                    placeholder="Enter Password"
                                    type="password"
                                    {...field}
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <div className="flex justify-between">
                    <Button type="submit">Log In</Button>
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
