"use client";

import React, { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import gsap from 'gsap';
import { API } from '../lib/api';
import { useAuth } from '../context/AuthContext';
import { CashflowSummary, Insight, ForecastResponse } from '../types';
import { TrendingUp, TrendingDown, DollarSign, Activity, ArrowRight, Wallet } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';



const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md p-3 border border-white/50 dark:border-slate-700/50 rounded-xl shadow-xl">
        <p className="text-sm font-semibold text-slate-700 dark:text-slate-200 mb-2">{label}</p>
        <div className="space-y-1">
          <p className="text-xs font-medium text-emerald-600 dark:text-emerald-400 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
            Inflow: ₹{(payload[0].value / 1000).toFixed(0)}k
          </p>
          <p className="text-xs font-medium text-indigo-600 dark:text-indigo-400 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-indigo-500"></span>
            Outflow: ₹{(payload[1].value / 1000).toFixed(0)}k
          </p>
        </div>
      </div>
    );
  }
  return null;
};

export default function DashboardPage() {
  const { user, loading: authLoading } = useAuth();
  const [loading, setLoading] = useState(false);
  const [mounted, setMounted] = useState(false);
  const router = useRouter();

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/signup");
    } else if (user) {
      loadData();
    }
  }, [user, authLoading]);

  // Data State
  const [cashflow, setCashflow] = useState<CashflowSummary | null>(null);
  const [insights, setInsights] = useState<Insight[]>([]);
  const [forecast, setForecast] = useState<ForecastResponse | null>(null);
  const [chartData, setChartData] = useState<any[]>([]);

  // Refs for animation
  const heroTextRef = useRef<HTMLDivElement>(null);
  const metricsRef = useRef<HTMLDivElement>(null);
  const chartSectionRef = useRef<HTMLDivElement>(null);
  const insightsRef = useRef<HTMLDivElement>(null);

  const loadData = async () => {
    if (!user) return;
    setLoading(true);
    try {
      // Parallel requests
      const [cfRes, insRes, fcRes, histRes] = await Promise.allSettled([
        API.get(`/cashflow/summary/${user.id}`),
        API.get(`/insights/${user.id}`),
        API.get(`/forecast/${user.id}`),
        API.get(`/cashflow/history/${user.id}`)
      ]);

      // Handle Cashflow
      if (cfRes.status === 'fulfilled') {
        setCashflow(cfRes.value.data);
      }

      // Handle Insights
      if (insRes.status === 'fulfilled') {
        setInsights(insRes.value.data.insights || []);
      }

      // Handle Forecast
      if (fcRes.status === 'fulfilled') {
        setForecast(fcRes.value.data);
      }

      // Handle History (Chart)
      if (histRes.status === 'fulfilled') {
        setChartData(histRes.value.data);
      }

    } catch (error) {
      console.error("Error loading dashboard data", error);
    } finally {
      setLoading(false);
    }
  };

  // Initial Animation
  useEffect(() => {
    // Animations
    const tl = gsap.timeline({ defaults: { ease: "power2.out" } });

    // Hero Text
    if (heroTextRef.current) {
      tl.fromTo(heroTextRef.current.children,
        { y: 30, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.8,
          stagger: 0.1
        }
      );
    }

    // Metrics Cards
    if (metricsRef.current) {
      tl.fromTo(metricsRef.current.children,
        { y: 20, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.6,
          stagger: 0.1
        }, "-=0.4");
    }

    // Chart
    if (chartSectionRef.current) {
      tl.fromTo(chartSectionRef.current,
        { y: 20, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.6
        }, "-=0.3");
    }

    // Insights & Forecast
    if (insightsRef.current) {
      tl.fromTo(insightsRef.current.children,
        { y: 20, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.6,
          stagger: 0.1
        }, "-=0.2");
    }
  }, []);

  // Format currency
  const formatINR = (val: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(val);
  };

  if (authLoading) {
    return <div className="min-h-screen flex items-center justify-center text-slate-400">Loading...</div>;
  }

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div ref={heroTextRef} className="space-y-2">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl md:text-4xl font-semibold tracking-tight text-slate-900 dark:text-white">
              Financial Overview
            </h1>
            <p className="text-slate-500 dark:text-slate-400 mt-1">
              Real-time cashflow visibility and AI-driven insights.
            </p>
          </div>

          {/* Controls */}
          <div className="flex items-center gap-3">
            <button
              onClick={loadData}
              disabled={loading}
              className="px-4 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-slate-600 dark:text-slate-300 text-sm font-medium transition-all"
            >
              {loading ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>
        </div>
      </div>

      {/* Metrics Grid */}
      <div ref={metricsRef} className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Net Balance */}
        <div className="group relative overflow-hidden rounded-2xl border border-white/60 dark:border-slate-700/60 bg-gradient-to-br from-white/80 via-slate-50/80 to-sky-50/50 dark:from-slate-800/80 dark:via-slate-900/80 dark:to-slate-950/80 backdrop-blur-xl shadow-lg shadow-slate-900/5 dark:shadow-black/20 p-6 transition-all hover:-translate-y-1 hover:shadow-xl">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400 font-semibold mb-1">Net Balance</p>
              <h3 className="text-3xl font-bold text-slate-800 dark:text-white">
                {cashflow ? formatINR(cashflow.net_balance) : '₹ --'}
              </h3>
            </div>
            <div className="p-2 rounded-lg bg-sky-500/10 text-sky-600 dark:text-sky-400">
              <Wallet size={24} />
            </div>
          </div>
          <div className="mt-4 flex items-center gap-2 text-sm text-emerald-600 dark:text-emerald-400">
            <TrendingUp size={16} />
            <span>Healthy buffer</span>
          </div>
        </div>

        {/* Total Inflow */}
        <div className="group relative overflow-hidden rounded-2xl border border-white/60 dark:border-slate-700/60 bg-white/70 dark:bg-slate-900/70 backdrop-blur-xl shadow-lg shadow-slate-900/5 dark:shadow-black/20 p-6 transition-all hover:-translate-y-1 hover:shadow-xl">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400 font-semibold mb-1">Total Inflow</p>
              <h3 className="text-3xl font-bold text-slate-800 dark:text-white">
                {cashflow ? formatINR(cashflow.total_inflow) : '₹ --'}
              </h3>
            </div>
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
              <DollarSign size={24} />
            </div>
          </div>
          <div className="mt-4 text-sm text-slate-500 dark:text-slate-400">
            Last 3 Months
          </div>
        </div>

        {/* Total Outflow */}
        <div className="group relative overflow-hidden rounded-2xl border border-white/60 dark:border-slate-700/60 bg-white/70 dark:bg-slate-900/70 backdrop-blur-xl shadow-lg shadow-slate-900/5 dark:shadow-black/20 p-6 transition-all hover:-translate-y-1 hover:shadow-xl">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400 font-semibold mb-1">Total Outflow</p>
              <h3 className="text-3xl font-bold text-slate-800 dark:text-white">
                {cashflow ? formatINR(cashflow.total_outflow) : '₹ --'}
              </h3>
            </div>
            <div className="p-2 rounded-lg bg-rose-500/10 text-rose-600 dark:text-rose-400">
              <Activity size={24} />
            </div>
          </div>
          <div className="mt-4 flex items-center gap-2 text-sm text-rose-500 dark:text-rose-400">
            <TrendingDown size={16} />
            <span>High operational cost</span>
          </div>
        </div>
      </div>

      {/* Chart Section */}
      <div ref={chartSectionRef} className="rounded-2xl border border-white/60 dark:border-slate-700/60 bg-white/70 dark:bg-slate-900/70 backdrop-blur-xl shadow-lg shadow-slate-900/5 dark:shadow-black/20 p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-600 dark:text-indigo-400">
              <TrendingUp size={20} />
            </div>
            <h3 className="text-lg font-semibold text-slate-800 dark:text-white">Cashflow Trend</h3>
          </div>
          <div className="flex items-center gap-4 text-xs font-medium">
            <div className="flex items-center gap-1.5 text-slate-600 dark:text-slate-300">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Inflow
            </div>
            <div className="flex items-center gap-1.5 text-slate-600 dark:text-slate-300">
              <span className="w-2.5 h-2.5 rounded-full bg-indigo-500"></span> Outflow
            </div>
          </div>
        </div>

        <div className="h-[300px] w-full">
          {!mounted ? (
            <div className="h-full w-full flex items-center justify-center text-slate-400 animate-pulse">Loading Chart...</div>
          ) : chartData.length === 0 ? (
            <div className="h-full w-full flex items-center justify-center text-slate-400 italic">No transaction data available</div>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorInflow" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorOutflow" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="currentColor" className="text-slate-200 dark:text-slate-700" opacity={0.4} />
                <XAxis
                  dataKey="month"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: '#94a3b8', fontSize: 12 }}
                  dy={10}
                />
                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: '#94a3b8', fontSize: 12 }}
                  tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
                />
                <Tooltip content={<CustomTooltip />} cursor={{ stroke: '#94a3b8', strokeWidth: 1, strokeDasharray: '4 4' }} />
                <Area
                  type="monotone"
                  dataKey="inflow"
                  stroke="#10b981"
                  fillOpacity={1}
                  fill="url(#colorInflow)"
                  strokeWidth={2}
                  animationDuration={1500}
                />
                <Area
                  type="monotone"
                  dataKey="outflow"
                  stroke="#6366f1"
                  fillOpacity={1}
                  fill="url(#colorOutflow)"
                  strokeWidth={2}
                  animationDuration={1500}
                />
              </AreaChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      {/* Insights & Forecast Split */}
      <div ref={insightsRef} className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Forecast Card */}
        <div className="rounded-2xl border border-white/60 dark:border-slate-700/60 bg-gradient-to-br from-indigo-50/50 via-white/60 to-white/60 dark:from-indigo-950/30 dark:via-slate-900/60 dark:to-slate-900/60 backdrop-blur-xl p-6 shadow-lg">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-600 dark:text-indigo-400">
              <Activity size={20} />
            </div>
            <h3 className="text-lg font-semibold text-slate-800 dark:text-white">Forecast & Analysis</h3>
          </div>

          <div className="space-y-4">
            {forecast ? (
              <>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-slate-500 dark:text-slate-400">Trend:</span>
                  <span className={`px-2 py-0.5 rounded-full text-xs font-bold uppercase tracking-wide ${forecast.trend === 'improving' ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-300' :
                    forecast.trend === 'declining' ? 'bg-rose-100 text-rose-700 dark:bg-rose-500/20 dark:text-rose-300' :
                      'bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-300'
                    }`}>
                    {forecast.trend}
                  </span>
                </div>
                <p className="text-slate-700 dark:text-slate-300 leading-relaxed">
                  {forecast.summary}
                </p>
                <div className="pt-2">
                  <h4 className="text-xs uppercase tracking-wider text-slate-500 mb-2 font-semibold">Recommendations</h4>
                  <ul className="space-y-2">
                    {(forecast.recommendations || []).map((rec, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-slate-600 dark:text-slate-300">
                        <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-indigo-500 flex-shrink-0" />
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
              </>
            ) : (
              <div className="text-center py-10 text-slate-400 italic">Load data to see forecast</div>
            )}
          </div>
        </div>

        {/* Recent Insights Preview */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-slate-800 dark:text-white">Recent Insights</h3>
            <a href="/insights" className="text-sm font-medium text-indigo-600 dark:text-indigo-400 hover:text-indigo-500 flex items-center gap-1 transition-colors">
              View All <ArrowRight size={14} />
            </a>
          </div>

          <div className="space-y-3">
            {insights.length > 0 ? (
              insights.slice(0, 3).map((insight, idx) => (
                <div key={idx} className="group p-4 rounded-xl border border-white/50 dark:border-slate-700/50 bg-white/40 dark:bg-slate-800/40 hover:bg-white/60 dark:hover:bg-slate-800/60 transition-all backdrop-blur-sm">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <h4 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-1">{insight.title}</h4>
                      <p className="text-xs text-slate-500 dark:text-slate-400 line-clamp-2">{insight.description}</p>
                    </div>
                    <span className={`flex-shrink-0 w-2 h-2 rounded-full mt-1.5 ${insight.severity === 'high' ? 'bg-rose-500 shadow-[0_0_8px_rgba(244,63,94,0.6)]' :
                      insight.severity === 'medium' ? 'bg-amber-500' :
                        'bg-emerald-500'
                      }`} />
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-10 text-slate-400 italic rounded-xl border border-dashed border-slate-300 dark:border-slate-700">
                No insights available
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
