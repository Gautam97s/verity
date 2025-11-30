"use client";

import React, { useEffect, useRef } from 'react';
import Navbar from './Navbar';
import { AuthProvider } from '../context/AuthContext';
import gsap from 'gsap';

export default function ClientLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const blob1Ref = useRef<HTMLDivElement>(null);
    const blob2Ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        // Subtle ambient animation for background blobs
        if (blob1Ref.current && blob2Ref.current) {
            gsap.to(blob1Ref.current, {
                x: '+=30',
                y: '-=20',
                duration: 8,
                repeat: -1,
                yoyo: true,
                ease: 'sine.inOut'
            });
            gsap.to(blob2Ref.current, {
                x: '-=30',
                y: '+=20',
                duration: 10,
                repeat: -1,
                yoyo: true,
                ease: 'sine.inOut',
                delay: 1
            });
        }
    }, []);

    return (
        <AuthProvider>
            <div className="relative min-h-screen overflow-hidden font-sans selection:bg-indigo-500/30">
                {/* Background Blobs */}
                <div
                    ref={blob1Ref}
                    className="absolute top-[-10rem] left-[-10rem] w-[40rem] h-[40rem] bg-gradient-to-br from-sky-300/30 via-indigo-300/20 to-emerald-200/30 dark:from-sky-900/30 dark:via-indigo-900/20 dark:to-emerald-900/30 blur-3xl rounded-full opacity-60 pointer-events-none z-0"
                />
                <div
                    ref={blob2Ref}
                    className="absolute bottom-[-5rem] right-[-5rem] w-[35rem] h-[35rem] bg-gradient-to-tl from-purple-300/30 via-pink-300/20 to-orange-200/30 dark:from-purple-900/30 dark:via-pink-900/20 dark:to-orange-900/30 blur-3xl rounded-full opacity-50 pointer-events-none z-0"
                />

                {/* Gradient Overlay */}
                <div className="absolute inset-0 bg-gradient-to-tr from-sky-200 via-indigo-100 to-emerald-100 opacity-60 dark:opacity-0 pointer-events-none z-0" />

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
        </AuthProvider>
    );
}
