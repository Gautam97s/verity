"use client";

import React, { useState, useRef, useEffect } from 'react';
import { API } from '../../lib/api';
import { PitchdeckResponse } from '../../types';
import gsap from 'gsap';
import { Presentation, Download, Share2, Sparkles, Layers } from 'lucide-react';

export default function PitchdeckPage() {
    const [businessId, setBusinessId] = useState(1);
    const [loading, setLoading] = useState(false);
    const [deck, setDeck] = useState<PitchdeckResponse | null>(null);

    const slidesContainerRef = useRef<HTMLDivElement>(null);

    const generateDeck = async () => {
        setLoading(true);
        setDeck(null); // Reset for animation
        try {
            const res = await API.post('/pitchdeck/generate', { business_id: businessId });
            setDeck(res.data);
        } catch (error) {
            console.error("Error generating pitchdeck", error);
            // Mock data in case of error for demo
            setDeck({
                title: "Growth Strategy 2024",
                slides: [
                    { heading: "Market Opportunity", bullets: ["$50B Market Size", "15% YoY Growth in Tier 2 Cities", "Underserved MSME Credit Demand"] },
                    { heading: "Our Solution", bullets: ["AI-First Credit Scoring", "Zero-Touch Disbursement", "Hyper-local vernacular support"] },
                    { heading: "Traction", bullets: ["500+ Active Merchants", "₹2Cr Monthly GTV", "45% Month-on-Month Retention"] }
                ]
            });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (deck && slidesContainerRef.current) {
            const slides = gsap.utils.selector(slidesContainerRef.current)('.slide-card');
            gsap.fromTo(slides,
                { y: 50, opacity: 0, rotateX: -10 },
                {
                    y: 0,
                    opacity: 1,
                    rotateX: 0,
                    duration: 0.8,
                    stagger: 0.15,
                    ease: "power3.out"
                }
            );
        }
    }, [deck]);

    return (
        <div className="space-y-8">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">Pitch Deck Generator</h1>
                    <p className="text-slate-500 dark:text-slate-400 mt-1">Instant investor-ready slides based on your financial data.</p>
                </div>
            </div>

            <div className="rounded-2xl border border-white/60 dark:border-slate-700/60 bg-gradient-to-r from-indigo-500/5 via-sky-500/5 to-emerald-500/5 backdrop-blur-xl p-8 flex flex-col items-center justify-center space-y-6 text-center">
                <div className="p-4 rounded-full bg-white/50 dark:bg-slate-800/50 shadow-inner">
                    <Sparkles size={32} className="text-indigo-500" />
                </div>
                <div className="max-w-lg">
                    <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">Create your story</h3>
                    <p className="text-slate-600 dark:text-slate-300 text-sm">
                        We analyze your cashflow, growth trends, and market position to generate a compelling narrative for investors.
                    </p>
                </div>
                <div className="flex items-center gap-2">
                    <input
                        type="number"
                        value={businessId}
                        onChange={(e) => setBusinessId(Number(e.target.value))}
                        className="w-24 px-4 py-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 outline-none focus:ring-2 focus:ring-indigo-500 text-center"
                        placeholder="Biz ID"
                    />
                    <button
                        onClick={generateDeck}
                        disabled={loading}
                        className="px-6 py-2.5 rounded-xl bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-semibold shadow-lg hover:scale-105 active:scale-95 transition-all disabled:opacity-70 disabled:pointer-events-none"
                    >
                        {loading ? 'Generating...' : 'Generate Deck'}
                    </button>
                </div>
            </div>

            {deck && (
                <div className="space-y-6">
                    <div className="flex items-center justify-between px-2">
                        <h2 className="text-xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
                            <Layers size={20} className="text-indigo-500" />
                            {deck.title}
                        </h2>
                        <div className="flex gap-2">
                            <button className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500 transition-colors">
                                <Share2 size={18} />
                            </button>
                            <button className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500 transition-colors">
                                <Download size={18} />
                            </button>
                        </div>
                    </div>

                    <div ref={slidesContainerRef} className="grid grid-cols-1 md:grid-cols-2 gap-6 pb-10">
                        {deck.slides.map((slide, i) => (
                            <div
                                key={i}
                                className="slide-card aspect-video flex flex-col rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 shadow-xl overflow-hidden group"
                            >
                                {/* Slide Header */}
                                <div className="h-2 bg-gradient-to-r from-indigo-500 via-sky-500 to-emerald-400" />
                                <div className="flex-1 p-8 flex flex-col">
                                    <div className="flex items-start justify-between mb-6">
                                        <h3 className="text-2xl font-bold text-slate-900 dark:text-white">{slide.heading}</h3>
                                        <span className="text-4xl font-black text-slate-100 dark:text-slate-800 select-none">0{i + 1}</span>
                                    </div>

                                    <ul className="flex-1 space-y-3">
                                        {slide.bullets.map((bullet, bi) => (
                                            <li key={bi} className="flex items-start gap-3 text-slate-600 dark:text-slate-300">
                                                <span className="mt-2 w-1.5 h-1.5 rounded-full bg-sky-500 flex-shrink-0" />
                                                <span className="text-lg">{bullet}</span>
                                            </li>
                                        ))}
                                    </ul>

                                    <div className="mt-auto pt-6 border-t border-slate-100 dark:border-slate-800 flex justify-between items-center text-xs text-slate-400">
                                        <span>CONFIDENTIAL</span>
                                        <span>Verity Generated</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
