"use client";

import React, { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { API } from '../../lib/api';
import { Insight } from '../../types';
import gsap from 'gsap';
import { Lightbulb, AlertTriangle, CheckCircle2, Info, RefreshCw } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export default function InsightsPage() {
    const { user, loading: authLoading } = useAuth();
    const [insights, setInsights] = useState<Insight[]>([]);
    const [loading, setLoading] = useState(false);
    const [mounted, setMounted] = useState(false);
    const containerRef = useRef<HTMLDivElement>(null);
    const router = useRouter();

    useEffect(() => {
        setMounted(true);
        if (!authLoading && !user) {
            router.push("/signup");
        } else if (user) {
            fetchInsights();
        }
    }, [user, authLoading]);

    const fetchInsights = async () => {
        if (!user) return;
        setLoading(true);
        try {
            const res = await API.get(`/insights/${user.id}`);
            if (res.data && res.data.insights) {
                setInsights(res.data.insights);
            } else {
                setInsights([]);
            }
        } catch (error) {
            console.warn("Failed to load insights");
            setInsights([]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (insights.length > 0 && containerRef.current) {
            const cards = gsap.utils.selector(containerRef.current)('.insight-card');
            gsap.fromTo(cards,
                { y: 20, opacity: 0 },
                { y: 0, opacity: 1, duration: 0.5, stagger: 0.1, ease: "power2.out", clearProps: "all" }
            );
        }
    }, [insights]);

    const getSeverityColor = (severity: string) => {
        switch (severity) {
            case 'high': return 'bg-rose-500 text-rose-50 border-rose-200 dark:border-rose-900';
            case 'medium': return 'bg-amber-500 text-amber-50 border-amber-200 dark:border-amber-900';
            case 'low': return 'bg-emerald-500 text-emerald-50 border-emerald-200 dark:border-emerald-900';
            default: return 'bg-slate-500 text-white';
        }
    };

    const getIcon = (severity: string) => {
        switch (severity) {
            case 'high': return <AlertTriangle size={18} />;
            case 'medium': return <Info size={18} />;
            case 'low': return <CheckCircle2 size={18} />;
            default: return <Lightbulb size={18} />;
        }
    };

    if (!mounted || authLoading) {
        return <div className="min-h-screen flex items-center justify-center text-slate-400">Loading...</div>;
    }

    return (
        <div className="space-y-8">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">Business Intelligence</h1>
                    <p className="text-slate-500 dark:text-slate-400 mt-1">AI-generated financial health check and opportunities.</p>
                </div>
                <div className="flex items-center gap-3">
                    <button
                        onClick={fetchInsights}
                        disabled={loading}
                        className="p-2 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 transition-colors"
                    >
                        <RefreshCw size={20} className={loading ? 'animate-spin' : ''} />
                    </button>
                </div>
            </div>

            <div ref={containerRef} className="grid grid-cols-1 gap-4">
                {loading ? (
                    <div className="space-y-4">
                        {[1, 2, 3].map((i) => (
                            <div key={i} className="h-32 rounded-2xl bg-white/40 dark:bg-slate-800/40 animate-pulse border border-white/20 dark:border-slate-700/20" />
                        ))}
                    </div>
                ) : insights.length > 0 ? (
                    insights.map((insight, idx) => (
                        <div
                            key={idx}
                            className="insight-card group relative overflow-hidden rounded-2xl border border-white/60 dark:border-slate-700/60 bg-white/70 dark:bg-slate-900/70 backdrop-blur-xl p-6 shadow-sm hover:shadow-lg transition-all duration-300"
                        >
                            <div className="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-transparent via-slate-200 dark:via-slate-700 to-transparent opacity-50" />

                            <div className="flex flex-col md:flex-row gap-6">
                                <div className="flex-1 space-y-3">
                                    <div className="flex items-center gap-3">
                                        <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider flex items-center gap-1.5 shadow-sm ${getSeverityColor(insight.severity)}`}>
                                            {getIcon(insight.severity)}
                                            {insight.severity} Priority
                                        </span>
                                        <span className="text-xs font-mono text-slate-400 uppercase">{insight.type}</span>
                                    </div>

                                    <h3 className="text-xl font-semibold text-slate-800 dark:text-slate-100">
                                        {insight.title}
                                    </h3>
                                    <p className="text-slate-600 dark:text-slate-300 leading-relaxed">
                                        {insight.description}
                                    </p>
                                </div>

                                <div className="md:w-64 flex-shrink-0 flex flex-col justify-center border-t md:border-t-0 md:border-l border-slate-200 dark:border-slate-700/50 pt-4 md:pt-0 md:pl-6">
                                    <span className="text-xs uppercase tracking-wider text-slate-500 mb-2 font-semibold">Recommended Action</span>
                                    <div className="p-3 rounded-lg bg-indigo-50 dark:bg-indigo-950/30 border border-indigo-100 dark:border-indigo-900/50 text-sm text-indigo-800 dark:text-indigo-200 font-medium cursor-pointer hover:bg-indigo-100 dark:hover:bg-indigo-900/50 transition-colors">
                                        {insight.call_to_action}
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <div className="text-center py-20 bg-white/30 dark:bg-slate-900/30 rounded-2xl border border-dashed border-slate-300 dark:border-slate-700">
                        <p className="text-slate-500">No specific insights found for this business.</p>
                    </div>
                )}
            </div>
        </div>
    );
}
