import React from "react";

const DashboardPage = () => {
  return (
    <>
      <div className="w-full h-full bg-zinc-300">
        <header className="max-w-7xl mx-auto h-[5vh] flex justify-center items-center">
          <span className="text-2xl font-bold font-mono tracking-widest">
            Header
          </span>
        </header>
        <main className="max-w-7xl mx-auto h-[90vh] flex justify-center items-center">
          <span className="text-2xl font-bold font-mono tracking-widest">
            Dashboard Body
          </span>
        </main>
        <footer className="max-w-7xl mx-auto h-[5vh] flex justify-center items-center">
          <span className="text-2xl font-bold font-mono tracking-widest">
            Footer
          </span>
        </footer>
      </div>
    </>
  );
};

export default DashboardPage;
