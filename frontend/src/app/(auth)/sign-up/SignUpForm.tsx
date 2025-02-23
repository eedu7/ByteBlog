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

import { type registerFormSchema } from "@/features/auth/formSchema";
import useFormSchema from "@/features/auth/useFormSchema";
import Link from "next/link";

const SignUpForm = () => {
    const { registerForm } = useFormSchema();

    const onSubmit = (values: z.infer<typeof registerFormSchema>) => {
        console.table(values);
    };

    return (
        <Form {...registerForm}>
            <form
                onSubmit={registerForm.handleSubmit(onSubmit)}
                className="space-y-8">
                <FormField
                    control={registerForm.control}
                    name="username"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Username</FormLabel>
                            <FormControl>
                                <Input placeholder="John Doe" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={registerForm.control}
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
                    control={registerForm.control}
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
                    <Button type="submit">Register</Button>
                    <Link
                        href="/sign-in"
                        className="text-sm text-blue-600 underline underline-offset-2 hover:text-blue-900 hover:scale-110 transition-transform">
                        Already have an account? Log in here
                    </Link>
                </div>
            </form>
        </Form>
    );
};

export default SignUpForm;
