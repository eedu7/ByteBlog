const layout = ({ children }: Readonly<{ children: React.ReactNode }>) => {
    return (
        <>
            <h1>Authentication</h1>
            {children}
        </>
    );
};

export default layout;
