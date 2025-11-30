"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Eye, EyeOff, Loader2, Building2 } from "lucide-react";
import { useAuth } from "../../context/AuthContext";

const signupSchema = z.object({
    name: z.string().min(1, "Business Name is required"),
    username: z.string().min(3, "Username must be at least 3 characters"),
    password: z.string().min(6, "Password must be at least 6 characters"),
});

type SignupFormValues = z.infer<typeof signupSchema>;

export default function SignupPage() {
    const router = useRouter();
    const { login } = useAuth();
    const [isLoading, setIsLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState("");

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<SignupFormValues>({
        resolver: zodResolver(signupSchema),
    });

    const onSubmit = async (data: SignupFormValues) => {
        setIsLoading(true);
        setError("");

        try {
            const response = await fetch("http://localhost:8000/auth/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Signup failed");
            }

            const result = await response.json();
            await login(result.access_token);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen text-white flex items-start justify-center p-4 pt-24">
            <div className="group/card w-full max-w-sm bg-gradient-to-br from-[#00ff75] to-[#3700ff] rounded-[22px] transition-all duration-300 hover:shadow-[0px_0px_30px_1px_rgba(0,255,117,0.3)] p-[2px]">
                <div className="h-full w-full bg-[#171717] rounded-[20px] transition-all duration-200 group-hover/card:scale-[0.98] group-hover/card:rounded-[20px] overflow-hidden">
                    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4 px-8 py-8 bg-[#171717] rounded-[25px]">
                        <p className="text-center text-white text-xl font-semibold mb-4">Sign Up</p>

                        {error && (
                            <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm text-center">
                                {error}
                            </div>
                        )}

                        <div className="flex items-center gap-2 rounded-[25px] p-3 bg-[#171717] shadow-[inset_2px_5px_10px_rgb(5,5,5)] border border-transparent focus-within:border-white/10 transition-colors">
                            <Building2 className="w-5 h-5 text-white flex-shrink-0" />
                            <input
                                {...register("name")}
                                type="text"
                                className="bg-transparent border-none outline-none w-full text-[#d3d3d3] placeholder-zinc-500"
                                placeholder="Business Name"
                                autoComplete="off"
                            />
                        </div>
                        {errors.name && (
                            <p className="text-red-400 text-xs -mt-3 ml-4">{errors.name.message}</p>
                        )}

                        <div className="flex items-center gap-2 rounded-[25px] p-3 bg-[#171717] shadow-[inset_2px_5px_10px_rgb(5,5,5)] border border-transparent focus-within:border-white/10 transition-colors">
                            <svg viewBox="0 0 16 16" fill="currentColor" height="16" width="16" xmlns="http://www.w3.org/2000/svg" className="w-5 h-5 text-white flex-shrink-0">
                                <path d="M13.106 7.222c0-2.967-2.249-5.032-5.482-5.032-3.35 0-5.646 2.318-5.646 5.702 0 3.493 2.235 5.708 5.762 5.708.862 0 1.689-.123 2.304-.335v-.862c-.43.199-1.354.328-2.29.328-2.926 0-4.813-1.88-4.813-4.798 0-2.844 1.921-4.881 4.594-4.881 2.735 0 4.608 1.688 4.608 4.156 0 1.682-.554 2.769-1.416 2.769-.492 0-.772-.28-.772-.76V5.206H8.923v.834h-.11c-.266-.595-.881-.964-1.6-.964-1.4 0-2.378 1.162-2.378 2.823 0 1.737.957 2.906 2.379 2.906.8 0 1.415-.39 1.709-1.087h.11c.081.67.703 1.148 1.503 1.148 1.572 0 2.57-1.415 2.57-3.643zm-7.177.704c0-1.197.54-1.907 1.456-1.907.93 0 1.524.738 1.524 1.907S8.308 9.84 7.371 9.84c-.895 0-1.442-.725-1.442-1.914z"></path>
                            </svg>
                            <input
                                {...register("username")}
                                type="text"
                                className="bg-transparent border-none outline-none w-full text-[#d3d3d3] placeholder-zinc-500"
                                placeholder="Username"
                                autoComplete="off"
                            />
                        </div>
                        {errors.username && (
                            <p className="text-red-400 text-xs -mt-3 ml-4">{errors.username.message}</p>
                        )}

                        <div className="flex items-center gap-2 rounded-[25px] p-3 bg-[#171717] shadow-[inset_2px_5px_10px_rgb(5,5,5)] border border-transparent focus-within:border-white/10 transition-colors">
                            <svg viewBox="0 0 16 16" fill="currentColor" height="16" width="16" xmlns="http://www.w3.org/2000/svg" className="w-5 h-5 text-white flex-shrink-0">
                                <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"></path>
                            </svg>
                            <input
                                {...register("password")}
                                type={showPassword ? "text" : "password"}
                                className="bg-transparent border-none outline-none w-full text-[#d3d3d3] placeholder-zinc-500"
                                placeholder="Password"
                            />
                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                className="text-zinc-500 hover:text-zinc-300 transition-colors"
                            >
                                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                            </button>
                        </div>
                        {errors.password && (
                            <p className="text-red-400 text-xs -mt-3 ml-4">{errors.password.message}</p>
                        )}

                        <div className="flex flex-col gap-4 mt-6">
                            <button
                                type="submit"
                                disabled={isLoading}
                                className="w-full py-2.5 rounded-[5px] bg-[#252525] text-white hover:bg-black transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed font-medium flex items-center justify-center shadow-[inset_2px_2px_5px_rgba(255,255,255,0.05)]"
                            >
                                {isLoading ? <Loader2 className="animate-spin w-5 h-5" /> : "Sign Up"}
                            </button>

                            <p className="text-center text-sm text-zinc-500 mt-1">
                                Already have an account?{" "}
                                <Link href="/login" className="text-[#3700ff] hover:text-[#2a00c4] transition-colors font-medium">
                                    Login
                                </Link>
                            </p>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}
