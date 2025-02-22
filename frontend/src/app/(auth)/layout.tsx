import React from "react";

const layout = ({ children }: Readonly<{ children: React.ReactNode }>) => {
    return (
        <>
            <h1 className="block text-center text-4xl font-bold font-mono">
                Authentication Page
            </h1>
            <div>{children}</div>
        </>
    );
};

export default layout;
