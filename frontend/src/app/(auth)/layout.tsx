import { WelcomeSVG } from "@/utils/image";
import Image from "next/image";
import React from "react";

const layout = ({ children }: Readonly<{ children: React.ReactNode }>) => {
    return (
        <>
            <nav className="block text-center font-bold font-mono h-[5vh] border border-rose-400">
                Authentication Page
            </nav>
            <main className="w-full h-[95vh] md:grid grid-cols-2 gap-2">
                <section className="col-span-1 h-full">
                    <div className="w-full pt-24 md:pt-0 md:h-full flex justify-center md:items-center">
                        {children}
                    </div>
                </section>
                <section className="hidden col-span-1 w-full h-full md:flex justify-center items-center">
                    <Image src={WelcomeSVG} alt="Welcome Back" className="w-[600px]" />
                </section>
            </main>
        </>
       
    );
};

export default layout;
