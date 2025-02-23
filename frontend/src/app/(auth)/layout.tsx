import { WelcomeSVG } from "@/utils/image";
import Image from "next/image";
import React from "react";

const layout = ({ children }: Readonly<{ children: React.ReactNode }>) => {
    return (
        <main className="w-full h-[95vh] lg:grid grid-cols-2 gap-2 max-w-7xl mx-auto">
            <section className="col-span-1 h-full">
                <div className="w-full h-full flex justify-center items-center">
                    {children}
                </div>
            </section>
            <section className="hidden lg:flex col-span-1 w-full h-full justify-center items-center">
                <Image
                    src={WelcomeSVG}
                    alt="Welcome Back"
                    className="w-[600px]"
                />
            </section>
        </main>
    );
};

export default layout;
