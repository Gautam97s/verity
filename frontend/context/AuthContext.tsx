"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";

interface User {
    id: number;
    name: string;
    username: string;
}

interface AuthContextType {
    user: User | null;
    loading: boolean;
    login: (token: string) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const router = useRouter();
    const pathname = usePathname();

    const fetchUser = async (token: string): Promise<boolean> => {
        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/business/me`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            if (res.ok) {
                const userData = await res.json();
                setUser(userData);
                return true;
            } else {
                localStorage.removeItem("token");
                setUser(null);
                return false;
            }
        } catch (error) {
            console.error("Failed to fetch user", error);
            localStorage.removeItem("token");
            setUser(null);
            return false;
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (typeof window === "undefined") {
            setLoading(false);
            return;
        }

        const token = localStorage.getItem("token");
        if (token) {
            fetchUser(token);
        } else {
            setLoading(false);
        }
    }, []);

    const login = async (token: string) => {
        localStorage.setItem("token", token);
        setLoading(true);
        try {
            const success = await fetchUser(token);
            if (success) {
                router.push("/");
            }
        } catch (error) {
            console.error("Login error", error);
            setLoading(false);
        }
    };

    const logout = () => {
        localStorage.removeItem("token");
        setUser(null);
        router.push("/login"); // Or signup, but login is standard for logout
    };

    return (
        <AuthContext.Provider value={{ user, loading, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
}
