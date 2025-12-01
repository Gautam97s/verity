"use client";

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Sun, Moon, LayoutDashboard, Zap, Lightbulb, Presentation } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Navbar: React.FC = () => {
    const { user, logout } = useAuth();
    const [isDark, setIsDark] = useState(false);
    const pathname = usePathname();

    useEffect(() => {
        const storedTheme = localStorage.getItem('theme');
        if (storedTheme === 'dark' || (!storedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
            setIsDark(true);
        } else {
            document.documentElement.classList.remove('dark');
            setIsDark(false);
        }
    }, []);

    const toggleTheme = () => {
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('theme', 'light');
            setIsDark(false);
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('theme', 'dark');
            setIsDark(true);
        }
    };

    const navLinks = [
        { name: 'Dashboard', path: '/', icon: LayoutDashboard },
        { name: 'Insights', path: '/insights', icon: Lightbulb },
        { name: 'Actions', path: '/actions/send-reminder', icon: Zap },
        { name: 'Pitchdeck', path: '/pitchdeck', icon: Presentation },
    ];

    return (
        <header className="sticky top-0 z-50 w-full backdrop-blur-md bg-white/50 dark:bg-slate-900/50 border-b border-white/20 dark:border-slate-800/60">
            <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-10 h-16 flex items-center justify-between">
                {/* Logo */}
                <Link href="/" className="flex items-center gap-2 group">
                    <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-slate-800 to-slate-600 dark:from-slate-100 dark:to-slate-300">
                        Verity
                    </span>
                </Link>

                {/* Desktop Nav */}
                <nav className="hidden md:flex items-center gap-1">
                    {navLinks.map((link) => {
                        const isActive = pathname === link.path;
                        const Icon = link.icon;
                        return (
                            <Link
                                key={link.path}
                                href={link.path}
                                className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 flex items-center gap-2 ${isActive
                                    ? 'bg-slate-200/50 dark:bg-slate-800/50 text-indigo-600 dark:text-indigo-400'
                                    : 'text-slate-600 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400 hover:bg-slate-100/50 dark:hover:bg-slate-800/30'
                                    }`}
                            >
                                <Icon size={16} />
                                {link.name}
                            </Link>
                        );
                    })}
                </nav>

                {/* Actions */}
                <div className="flex items-center gap-3">
                    {user && (
                        <button
                            onClick={logout}
                            className="text-sm font-medium text-slate-500 hover:text-red-500 dark:text-slate-400 dark:hover:text-red-400 transition-colors"
                        >
                            Logout
                        </button>
                    )}

                    {/* Theme Toggle */}
                    <button
                        onClick={toggleTheme}
                        className="inline-flex items-center gap-2 rounded-full px-3 py-1.5 border border-slate-200/50 dark:border-slate-700/50 bg-white/40 dark:bg-slate-800/40 backdrop-blur-md transition-all hover:bg-white/60 dark:hover:bg-slate-800/60"
                        aria-label="Toggle theme"
                    >
                        {isDark ? (
                            <Moon size={16} className="text-indigo-400" />
                        ) : (
                            <Sun size={16} className="text-amber-500" />
                        )}
                    </button>
                </div>
            </div>
        </header>
    );
};

export default Navbar;
