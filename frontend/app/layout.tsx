import React from 'react';
import type { Metadata } from 'next';
import Navbar from '../components/Navbar';
import Background from '../components/Background';
import "./globals.css";

export const metadata: Metadata = {
  title: 'Verity - MSME Financial Dashboard',
  description: 'AI-powered financial management platform for Indian MSMEs.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className="bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors duration-300">
        <div className="relative min-h-screen overflow-hidden font-sans selection:bg-indigo-500/30">
          <Background />

          <div className="relative z-10 flex flex-col min-h-screen">
            <Navbar />
            <main className="flex-grow w-full max-w-6xl mx-auto px-4 sm:px-6 lg:px-10 py-8 sm:py-10 lg:py-12">
              {children}
            </main>

            <footer className="py-6 text-center text-slate-400 dark:text-slate-600 text-sm">
              <p>© 2024 Verity. Empowering MSMEs.</p>
            </footer>
          </div>
        </div>
      </body>
    </html>
  );
}
