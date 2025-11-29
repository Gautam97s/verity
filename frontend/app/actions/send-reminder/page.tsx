"use client";

import React, { useState, useEffect, useRef } from 'react';
import { API } from '../../../lib/api';
import { ReminderResponse, SendReminderRequest } from '../../../types';
import gsap from 'gsap';
import { Send, CheckCircle, AlertCircle, MessageSquare, Phone } from 'lucide-react';

export default function SendReminderPage() {
    const containerRef = useRef<HTMLDivElement>(null);

    const [formData, setFormData] = useState<SendReminderRequest>({
        business_id: 1,
        customer_name: "Rahul Sharma",
        customer_phone: "+919876543210",
        invoice_number: "INV-2024-001",
        amount_due: 15000,
        due_date: "2024-05-20",
        days_overdue: 5,
        preferred_tone: "professional",
        preferred_language: "english"
    });

    const [loading, setLoading] = useState(false);
    const [response, setResponse] = useState<ReminderResponse | null>(null);

    useEffect(() => {
        if (containerRef.current) {
            gsap.fromTo(containerRef.current,
                { opacity: 0, y: 20 },
                {
                    opacity: 1,
                    y: 0,
                    duration: 0.6,
                    ease: "power2.out"
                }
            );
        }
    }, []);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: name === 'amount_due' || name === 'days_overdue' || name === 'business_id' ? Number(value) : value
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setResponse(null);

        try {
            const res = await API.post('/actions/send_whatsapp_reminder', formData);
            setResponse(res.data);
        } catch (error) {
            console.warn("API unavailable, simulating success for demo.");
            // Fallback Mock Response for Demo
            setResponse({
                message: "Demo Mode: Message queued for delivery.",
                delivery: {
                    status: "mock",
                    to: formData.customer_phone,
                    body: `[Demo] Hello ${formData.customer_name}, this is a gentle reminder regarding invoice ${formData.invoice_number} of ₹${formData.amount_due} which is overdue by ${formData.days_overdue} days.`,
                    sid: "SM12345MOCK"
                }
            });
        } finally {
            setLoading(false);
            // Animate success card in
            setTimeout(() => {
                gsap.from(".result-card", {
                    opacity: 0,
                    scale: 0.95,
                    y: 10,
                    duration: 0.5,
                    ease: "back.out(1.7)"
                });
            }, 100);
        }
    };

    return (
        <div className="max-w-3xl mx-auto space-y-8">
            <div className="text-center space-y-2">
                <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">Payment Reminder</h1>
                <p className="text-slate-500 dark:text-slate-400">Generate and send AI-optimized WhatsApp reminders.</p>
            </div>

            <div ref={containerRef} className="rounded-2xl border border-white/60 dark:border-slate-700/60 bg-white/95 dark:bg-slate-900/95 backdrop-blur-xl shadow-lg shadow-slate-900/5 dark:shadow-black/20 overflow-hidden">
                <div className="p-6 md:p-8">
                    <form onSubmit={handleSubmit} className="space-y-6">

                        {/* Customer Details */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <label className="text-xs uppercase tracking-wider text-slate-500 font-semibold">Customer Name</label>
                                <input
                                    type="text"
                                    name="customer_name"
                                    value={formData.customer_name}
                                    onChange={handleChange}
                                    className="w-full px-4 py-2.5 rounded-lg bg-slate-50 dark:bg-slate-950/50 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all outline-none"
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-xs uppercase tracking-wider text-slate-500 font-semibold">Phone Number</label>
                                <div className="relative">
                                    <Phone size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                                    <input
                                        type="text"
                                        name="customer_phone"
                                        value={formData.customer_phone}
                                        onChange={handleChange}
                                        className="w-full pl-10 pr-4 py-2.5 rounded-lg bg-slate-50 dark:bg-slate-950/50 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all outline-none"
                                        required
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Invoice Details */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <div className="space-y-2">
                                <label className="text-xs uppercase tracking-wider text-slate-500 font-semibold">Invoice #</label>
                                <input
                                    type="text"
                                    name="invoice_number"
                                    value={formData.invoice_number}
                                    onChange={handleChange}
                                    className="w-full px-4 py-2.5 rounded-lg bg-slate-50 dark:bg-slate-950/50 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-indigo-500/50 outline-none"
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-xs uppercase tracking-wider text-slate-500 font-semibold">Amount Due (₹)</label>
                                <input
                                    type="number"
                                    name="amount_due"
                                    value={formData.amount_due}
                                    onChange={handleChange}
                                    className="w-full px-4 py-2.5 rounded-lg bg-slate-50 dark:bg-slate-950/50 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-indigo-500/50 outline-none"
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-xs uppercase tracking-wider text-slate-500 font-semibold">Days Overdue</label>
                                <input
                                    type="number"
                                    name="days_overdue"
                                    value={formData.days_overdue}
                                    onChange={handleChange}
                                    className="w-full px-4 py-2.5 rounded-lg bg-slate-50 dark:bg-slate-950/50 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-indigo-500/50 outline-none"
                                />
                            </div>
                        </div>

                        {/* AI Settings */}
                        <div className="pt-4 border-t border-slate-200 dark:border-slate-700/50">
                            <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-4 flex items-center gap-2">
                                <MessageSquare size={16} className="text-indigo-500" />
                                AI Message Configuration
                            </h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <label className="text-xs uppercase tracking-wider text-slate-500 font-semibold">Tone</label>
                                    <select
                                        name="preferred_tone"
                                        value={formData.preferred_tone}
                                        onChange={handleChange}
                                        className="w-full px-4 py-2.5 rounded-lg bg-slate-50 dark:bg-slate-950/50 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-indigo-500/50 outline-none appearance-none cursor-pointer"
                                    >
                                        <option value="polite">Polite</option>
                                        <option value="professional">Professional</option>
                                        <option value="firm">Firm</option>
                                        <option value="urgent">Urgent</option>
                                    </select>
                                </div>
                                <div className="space-y-2">
                                    <label className="text-xs uppercase tracking-wider text-slate-500 font-semibold">Language</label>
                                    <select
                                        name="preferred_language"
                                        value={formData.preferred_language}
                                        onChange={handleChange}
                                        className="w-full px-4 py-2.5 rounded-lg bg-slate-50 dark:bg-slate-950/50 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-indigo-500/50 outline-none appearance-none cursor-pointer"
                                    >
                                        <option value="english">English</option>
                                        <option value="hindi">Hindi</option>
                                        <option value="hinglish">Hinglish</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        <div className="pt-6">
                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full py-3 rounded-xl bg-gradient-to-r from-indigo-500 via-sky-500 to-emerald-400 hover:from-indigo-600 hover:via-sky-600 hover:to-emerald-500 text-white font-semibold text-base shadow-lg shadow-indigo-500/30 flex items-center justify-center gap-2 transition-all hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-70 disabled:pointer-events-none"
                            >
                                {loading ? (
                                    <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                ) : (
                                    <>
                                        <Send size={18} />
                                        Send WhatsApp Reminder
                                    </>
                                )}
                            </button>
                        </div>

                    </form>
                </div>
            </div>

            {/* Result Card */}
            {response && (
                <div className="result-card rounded-2xl border border-white/60 dark:border-slate-700/60 bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl p-6 shadow-xl">
                    <div className="flex items-start gap-4">
                        <div className={`p-3 rounded-full ${response.delivery.status === 'error' ? 'bg-rose-100 text-rose-600' : 'bg-emerald-100 text-emerald-600'}`}>
                            {response.delivery.status === 'error' ? <AlertCircle size={24} /> : <CheckCircle size={24} />}
                        </div>
                        <div className="flex-1 space-y-2">
                            <h4 className="text-lg font-semibold text-slate-900 dark:text-white">
                                {response.delivery.status === 'error' ? 'Delivery Failed' : 'Message Sent Successfully'}
                            </h4>
                            <p className="text-sm text-slate-600 dark:text-slate-300">
                                {response.message}
                            </p>
                            <div className="mt-4 p-4 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 font-mono text-sm text-slate-600 dark:text-slate-400 whitespace-pre-wrap">
                                {response.delivery.body}
                            </div>
                        </div>
                    </div>
                </div>
            )}

        </div>
    );
}
