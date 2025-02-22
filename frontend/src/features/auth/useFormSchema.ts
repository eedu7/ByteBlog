import { zodResolver } from "@hookform/resolvers/zod";

import { useForm } from "react-hook-form";
import { z } from "zod";
import { loginFormSchema, registerFormSchema } from "./formSchema";

const useFormSchema = () => {
    const registerForm = useForm<z.infer<typeof registerFormSchema>>({
        resolver: zodResolver(registerFormSchema),
        defaultValues: {
            username: "",
            email: "",
            password: "",
        },
        mode: "onChange",
    });

    const loginForm = useForm<z.infer<typeof loginFormSchema>>({
        resolver: zodResolver(loginFormSchema),
        defaultValues: {
            email: "",
            password: "",
        },
        mode: "onChange",
    });

    return { registerForm, loginForm };
};

export default useFormSchema;
