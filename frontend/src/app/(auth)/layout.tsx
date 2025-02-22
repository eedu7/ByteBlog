import React from "react";

const layout = ({ children }: Readonly<{ children: React.ReactNode }>) => {
    return (
        <>
            <nav className="block text-center text-4xl font-bold font-mono h-[5vh]">
                Authentication Page
            </nav>
            <main className="w-full h-[95vh] grid grid-cols-2 gap-2">
                <section className="col-span-1 h-full">{children}</section>
                <section className="col-span-1 w-full"></section>
            </main>
        </>
    );
};

export default layout;
