import React, { useState } from "react";

interface ResponsiveLayoutProps {
  children: React.ReactNode;
}

export const ResponsiveLayout: React.FC<ResponsiveLayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex min-h-screen flex-col bg-neutral-50 dark:bg-neutral-950">
      {/* Top Navigation Bar */}
      <header className="sticky top-0 z-40 flex h-16 items-center justify-between border-b bg-white px-4 dark:border-neutral-800 dark:bg-neutral-900 md:px-6">
        <div className="flex items-center gap-3">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label="Toggle navigation menu"
            className="rounded p-2 text-neutral-600 hover:bg-neutral-100 md:hidden dark:text-neutral-300 dark:hover:bg-neutral-800"
          >
            ☰
          </button>
          <span className="text-xl font-bold tracking-tight text-neutral-900 dark:text-white">
            Application
          </span>
        </div>
      </header>

      {/* Main Workspace */}
      <div className="flex flex-1">
        {/* Desktop Sidebar */}
        <aside className="hidden w-64 border-r bg-white p-4 dark:border-neutral-800 dark:bg-neutral-900 md:block">
          <nav className="space-y-1">
            <a href="#" className="flex rounded-md bg-primary-50 px-3 py-2 text-sm font-medium text-primary-700 dark:bg-neutral-800 dark:text-white">
              Dashboard
            </a>
            <a href="#" className="flex rounded-md px-3 py-2 text-sm font-medium text-neutral-700 hover:bg-neutral-100 dark:text-neutral-300 dark:hover:bg-neutral-800">
              Settings
            </a>
          </nav>
        </aside>

        {/* Content Area */}
        <main className="flex-1 p-4 md:p-8">
          <div className="mx-auto max-w-7xl">{children}</div>
        </main>
      </div>
    </div>
  );
};
