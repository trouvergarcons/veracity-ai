'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
    Newspaper,
    MessageSquareText,
    HistoryIcon,
    Settings,
    Sparkles,
    ShieldCheck,
    BarChart3,
    HeartPulse,
    LogIn,
    X,
    Home,
    Zap,
    Cpu
} from 'lucide-react';
import Image from 'next/image';

const navItems = [
    {
        name: 'Home / Rumours Feed',
        href: '/',
        icon: Home,
        description: 'Live verified claims stream'
    },
    {
        name: 'Quick Check',
        href: '/check',
        icon: Zap,
        description: 'Instant AI claim analysis'
    },
    {
        name: 'AI Verifier Chat',
        href: '/chat',
        icon: MessageSquareText,
        description: 'Conversational verification'
    },
    {
        name: 'Analysis Dashboard',
        href: '/analysis',
        icon: BarChart3,
        description: 'Visual insights & Looker Studio'
    },
    {
        name: 'Digital Wellbeing',
        href: '/wellbeing',
        icon: HeartPulse,
        description: 'Screen time & Win32 telemetry'
    },
    {
        name: 'History',
        href: '/history',
        icon: HistoryIcon,
        description: 'Past scans & saved checks'
    },
    {
        name: 'Settings',
        href: '/settings',
        icon: Settings,
        description: 'API keys & preferences'
    },
];

export function Sidebar({ isOpen = false, onClose = () => {} }) {
    const pathname = usePathname();

    return (
        <>
            {/* Backdrop Overlay when 3-dots drawer is open: Shows Logo and DESIGN BY DIVYANSHU YADAV in the blurred screen area */}
            {isOpen && (
                <div
                    onClick={onClose}
                    className="fixed inset-0 z-40 bg-black/75 backdrop-blur-md transition-all duration-300 animate-in fade-in flex items-center justify-center p-6 lg:pl-80 cursor-pointer"
                >
                    {/* Centered Holographic Display in the blurred screen area (other than taskbar) */}
                    <div
                        onClick={(e) => e.stopPropagation()}
                        className="max-w-md w-full p-8 rounded-3xl bg-slate-900/85 border border-teal-500/40 shadow-2xl backdrop-blur-2xl relative overflow-hidden flex flex-col items-center text-center group cursor-default animate-in zoom-in-95 duration-200"
                    >
                        {/* Ambient Atmospheric Glows */}
                        <div className="absolute -top-20 -right-20 w-60 h-60 bg-teal-500/20 rounded-full blur-3xl pointer-events-none group-hover:bg-teal-500/30 transition duration-700 animate-pulse" />
                        <div className="absolute -bottom-20 -left-20 w-60 h-60 bg-cyan-500/15 rounded-full blur-3xl pointer-events-none" />

                        {/* Large Illuminated Veracity AI Logo */}
                        <div className="relative mb-5">
                            <div className="absolute -inset-2 rounded-3xl bg-gradient-to-tr from-teal-400 via-cyan-400 to-blue-500 opacity-60 blur-lg group-hover:opacity-90 transition duration-500 animate-pulse" />
                            <div className="relative w-24 h-24 rounded-3xl bg-slate-950 border border-teal-400/60 flex items-center justify-center p-3 shadow-2xl">
                                <Image
                                    src="/logo_256.png"
                                    alt="Veracity AI Official Logo"
                                    width={72}
                                    height={72}
                                    className="object-contain drop-shadow-[0_0_16px_rgba(20,184,166,0.8)]"
                                    priority
                                    unoptimized
                                />
                            </div>
                        </div>

                        {/* Brand Title */}
                        <h2 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-teal-200 via-cyan-300 to-blue-400 bg-clip-text text-transparent">
                            Veracity AI
                        </h2>
                        <p className="text-xs text-slate-300 font-medium mt-1">
                            Neural Fact Verification & Intelligence Platform
                        </p>

                        {/* Divider Line */}
                        <div className="my-5 w-32 h-[1px] bg-gradient-to-r from-transparent via-teal-400/60 to-transparent" />

                        {/* DESIGN BY DIVYANSHU YADAV Prestige Badge */}
                        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-teal-500/20 via-cyan-500/20 to-blue-500/20 border border-teal-400/50 text-teal-200 shadow-lg">
                            <Sparkles className="w-4 h-4 text-amber-400 animate-spin" style={{ animationDuration: '6s' }} />
                            <span className="text-xs font-extrabold tracking-wider uppercase">
                                DESIGN BY DIVYANSHU YADAV
                            </span>
                        </div>

                        {/* Student Details */}
                        <div className="flex items-center gap-2 mt-3 text-xs text-slate-300 font-mono">
                            <span className="text-teal-300 font-bold">Roll No: 25MCA00PY0036</span>
                            <span className="text-slate-500">•</span>
                            <span className="text-slate-400">MCA 2025–2027 (Sem III)</span>
                        </div>
                        <p className="text-[11px] text-slate-400 mt-1">
                            Under the guidance of <strong className="text-slate-200">Dr. R. Sunitha</strong>
                        </p>

                        {/* Dismiss Hint */}
                        <button
                            onClick={onClose}
                            className="mt-6 px-4 py-1.5 rounded-xl bg-white/5 hover:bg-white/10 text-xs font-semibold text-slate-400 hover:text-white border border-white/10 transition cursor-pointer"
                        >
                            Click backdrop or choose a section to continue
                        </button>
                    </div>
                </div>
            )}

            {/* Slide-Over Drawer Navigation */}
            <aside
                className={`fixed top-0 left-0 bottom-0 z-50 flex flex-col w-80 max-w-[85vw] bg-slate-950/95 border-r border-teal-500/30 backdrop-blur-2xl shadow-2xl transition-transform duration-300 ease-in-out ${
                    isOpen ? 'translate-x-0' : '-translate-x-full'
                }`}
            >
                {/* Ambient glow inside drawer */}
                <div className="absolute -top-20 -left-10 w-60 h-60 rounded-full bg-teal-500/10 blur-[80px] pointer-events-none" />
                <div className="absolute -bottom-20 -right-10 w-40 h-40 rounded-full bg-blue-500/10 blur-[60px] pointer-events-none" />

                {/* Drawer Header & Close Button */}
                <div className="flex items-center justify-between px-6 pt-6 pb-4 border-b border-white/10 relative z-10">
                    <div className="flex items-center gap-3">
                        <div className="relative w-10 h-10 rounded-xl bg-slate-900 border border-teal-500/50 flex items-center justify-center p-1.5 shadow-lg shadow-teal-500/25">
                            <Image
                                src="/logo_64.png"
                                alt="Veracity AI Logo"
                                width={28}
                                height={28}
                                className="object-contain drop-shadow-[0_0_8px_rgba(20,184,166,0.7)]"
                                priority
                                unoptimized
                            />
                        </div>
                        <div className="flex flex-col">
                            <span className="text-lg font-black text-white tracking-tight leading-tight">
                                Veracity AI
                            </span>
                            <span className="text-[10px] text-teal-400 font-medium leading-none mt-0.5">
                                Intelligent AI Fact Verification Platform
                            </span>
                        </div>
                    </div>

                    {/* Close 'X' Button */}
                    <button
                        onClick={onClose}
                        className="p-2 rounded-xl bg-white/5 hover:bg-white/10 text-slate-400 hover:text-white border border-white/10 transition"
                        title="Close Navigation"
                    >
                        <X className="w-4 h-4" />
                    </button>
                </div>

                {/* Navigation Items List */}
                <nav className="flex-1 px-4 py-4 space-y-1 overflow-y-auto relative z-10">
                    <div className="flex items-center justify-between px-3 mb-2 text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                        <span>Main Sections</span>
                        <span className="text-teal-400 font-mono">7 Modules</span>
                    </div>

                    {navItems.map((item) => {
                        const isActive = pathname === item.href;

                        return (
                            <Link
                                key={item.href}
                                href={item.href}
                                onClick={onClose}
                            >
                                <div
                                    className={`flex items-center gap-3 px-3.5 py-2.5 rounded-xl transition-all duration-150 group cursor-pointer ${
                                        isActive
                                            ? 'bg-gradient-to-r from-teal-500/20 to-cyan-500/10 border border-teal-500/40 text-white font-semibold shadow-md'
                                            : 'text-slate-400 hover:text-white hover:bg-white/5 border border-transparent'
                                    }`}
                                >
                                    <div
                                        className={`w-8 h-8 rounded-lg flex items-center justify-center transition ${
                                            isActive
                                                ? 'bg-teal-500 text-slate-950 shadow-md font-bold'
                                                : 'bg-white/5 group-hover:bg-white/10 text-slate-300'
                                        }`}
                                    >
                                        <item.icon className="h-4 w-4" />
                                    </div>

                                    <div className="flex flex-col min-w-0">
                                        <span className="text-xs font-semibold truncate">
                                            {item.name}
                                        </span>
                                        <span className="text-[10px] text-slate-400 truncate">
                                            {item.description}
                                        </span>
                                    </div>

                                    {isActive && (
                                        <div className="ml-auto w-1.5 h-1.5 rounded-full bg-teal-400 animate-pulse" />
                                    )}
                                </div>
                            </Link>
                        );
                    })}
                </nav>

                {/* Footer: Quick Account & System Status */}
                <div className="relative z-10 px-4 py-3 border-t border-white/10 flex items-center justify-between text-xs bg-slate-950/60">
                    <div className="flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                        <span className="text-[11px] text-slate-400 font-mono">System Active</span>
                    </div>

                    <Link
                        href="/login"
                        onClick={onClose}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/5 hover:bg-teal-500/20 text-slate-300 hover:text-teal-300 border border-white/10 hover:border-teal-500/30 transition text-xs font-semibold"
                        title="Account Sign In"
                    >
                        <LogIn className="w-3.5 h-3.5" />
                        <span>Login</span>
                    </Link>
                </div>
            </aside>
        </>
    );
}
