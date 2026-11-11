'use client';

import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { Sidebar } from '@/components/Sidebar';
import { Toaster } from 'sonner';
import CyberGlobe3D from '@/components/3d/CyberGlobe3D';
import {
    Sparkles,
    ShieldCheck,
    Home,
    Zap,
    MoreVertical,
    Bot,
    HeartPulse,
    BarChart3,
    LogIn
} from 'lucide-react';

const topNavLinks = [
    {
        name: 'Home',
        href: '/',
        icon: Home,
        title: 'Go to Home Feed',
        accentColor: 'text-teal-400',
        visibility: 'flex'
    },
    {
        name: 'Quick Check',
        href: '/check',
        icon: Zap,
        title: 'Quick Fact Check Claim or URL',
        accentColor: 'text-cyan-400',
        visibility: 'flex'
    },
    {
        name: 'AI Verifier',
        href: '/chat',
        icon: Bot,
        title: 'Interactive AI Verifier Chat & Fact-Checker',
        accentColor: 'text-purple-400',
        visibility: 'hidden md:flex'
    },
    {
        name: 'Wellbeing',
        href: '/wellbeing',
        icon: HeartPulse,
        title: 'Digital Wellbeing & Live Laptop Screen Time',
        accentColor: 'text-emerald-400',
        visibility: 'hidden lg:flex'
    }
];

export default function DashboardLayout({ children }) {
    const [isNavOpen, setIsNavOpen] = useState(false);
    const [activeOverride, setActiveOverride] = useState(null);
    const isDragging = useRef(false);
    const pathname = usePathname();

    useEffect(() => {
        setActiveOverride(null);
    }, [pathname]);

    const isLinkActive = (href) => {
        if (activeOverride) {
            return activeOverride === href;
        }
        if (!pathname) return false;
        if (href === '/') {
            return pathname === '/';
        }
        return pathname === href || pathname.startsWith(href + '/');
    };

    return (
        <div className="flex h-screen overflow-hidden bg-slate-950 text-white relative">
            {/* 3D Cyber Globe & Neural Network in the Background (Full Screen View) */}
            <CyberGlobe3D opacity={0.52} className="z-0" />

            {/* Ambient Cosmic Radial Glows */}
            <div className="absolute top-0 left-1/3 w-[800px] h-[450px] rounded-full bg-teal-500/[0.05] blur-[150px] pointer-events-none z-[1]" />
            <div className="absolute bottom-0 right-0 w-[600px] h-[400px] rounded-full bg-cyan-500/[0.04] blur-[130px] pointer-events-none z-[1]" />
            <div className="absolute top-1/2 -left-20 w-[450px] h-[450px] rounded-full bg-purple-500/[0.04] blur-[140px] pointer-events-none z-[1]" />

            {/* Slide-Over 3-Dots Navigation Drawer */}
            <Sidebar isOpen={isNavOpen} onClose={() => setIsNavOpen(false)} />

            {/* Main Application Area (Expansive Full Width) */}
            <main className="flex-1 overflow-y-auto relative z-10 flex flex-col justify-between">
                {/* Modern Top Header Navigation Bar with 3-Dots Menu & Quick Buttons */}
                <header className="sticky top-0 z-30 flex items-center justify-between px-4 sm:px-6 py-3 bg-slate-950/80 backdrop-blur-xl border-b border-white/[0.08] shadow-lg">
                    {/* Left: 3-Dots Menu Button & Brand */}
                    <div className="flex items-center gap-3">
                        {/* 3-Dots Navigation Button */}
                        <button
                            onClick={() => setIsNavOpen(true)}
                            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/5 hover:bg-teal-500/10 text-slate-300 hover:text-teal-300 border border-white/10 hover:border-teal-500/40 transition shadow-sm group cursor-pointer"
                            title="Open Navigation Menu (3-Dots)"
                        >
                            <MoreVertical className="w-4 h-4 text-teal-400 group-hover:scale-110 transition" />
                            <span className="text-xs font-semibold hidden sm:inline">Sections</span>
                        </button>

                        <Link href="/" className="flex items-center gap-2.5 group" title="Veracity AI Home Feed">
                            <div className="relative w-8 h-8 rounded-xl bg-slate-900 border border-teal-500/50 flex items-center justify-center p-1 shadow-md group-hover:border-teal-300 transition shrink-0 group-hover:shadow-[0_0_12px_rgba(20,184,166,0.5)]">
                                <Image
                                    src="/logo_64.png"
                                    alt="Veracity AI Official Logo"
                                    width={24}
                                    height={24}
                                    className="object-contain drop-shadow-[0_0_6px_rgba(20,184,166,0.6)]"
                                    priority
                                    unoptimized
                                />
                            </div>
                            <div className="flex flex-col">
                                <span className="text-lg sm:text-xl font-black bg-gradient-to-r from-teal-300 via-cyan-300 to-blue-400 bg-clip-text text-transparent group-hover:opacity-90 transition tracking-tight leading-tight">
                                    Veracity AI
                                </span>
                                <span className="text-[10px] text-slate-400 font-medium tracking-normal leading-none mt-0.5">
                                    Intelligent AI Fact Verification Platform
                                </span>
                            </div>
                        </Link>
                    </div>

                    {/* Center: Quick Action Buttons for ALL Pages */}
                    <div className="flex items-center gap-2">
                        {topNavLinks.map((item) => {
                            const active = isLinkActive(item.href);
                            const IconComponent = item.icon;

                            return (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    onClick={() => setActiveOverride(item.href)}
                                    className={`${item.visibility} items-center gap-1.5 rounded-xl text-xs transition-all duration-200 cursor-pointer shadow-sm ${
                                        active
                                            ? 'px-3.5 py-1.5 bg-gradient-to-r from-teal-500 to-cyan-500 text-slate-950 font-extrabold shadow-md shadow-teal-500/25 scale-[1.02]'
                                            : 'px-3 py-1.5 bg-white/5 hover:bg-white/10 text-slate-300 hover:text-white border border-white/10 hover:border-teal-500/30 font-semibold'
                                    }`}
                                    title={item.title}
                                >
                                    <IconComponent
                                        className={`w-3.5 h-3.5 shrink-0 transition-colors ${
                                            active
                                                ? 'text-slate-950 fill-slate-950'
                                                : `${item.accentColor}`
                                        }`}
                                    />
                                    <span className={active ? 'text-slate-950 font-extrabold' : 'text-slate-300 hover:text-white'}>
                                        {item.name}
                                    </span>
                                </Link>
                            );
                        })}
                    </div>

                    {/* Right: Designer Prestige Branding & 3-Dots Quick Trigger */}
                    <div className="flex items-center gap-2">
                        {/* Designed by Divyanshu Yadav Chip */}
                        <div
                            className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-gradient-to-r from-teal-500/10 via-cyan-500/10 to-blue-500/10 border border-teal-500/30 shadow-sm backdrop-blur-md cursor-default"
                            title="Designed & Developed by Divyanshu Yadav (Roll No: 25MCA00PY0036)"
                        >
                            <Sparkles className="w-3.5 h-3.5 text-amber-400 animate-spin" style={{ animationDuration: '6s' }} />
                            <span className="text-xs font-bold text-white tracking-wide">
                                Designed by <span className="bg-gradient-to-r from-teal-300 via-cyan-300 to-blue-400 bg-clip-text text-transparent">Divyanshu Yadav</span>
                            </span>
                            <span className="text-[10px] text-teal-400/90 font-mono pl-1 border-l border-white/10 hidden xl:inline">
                                25MCA00PY0036
                            </span>
                        </div>

                        {/* Right 3-Dots Quick Trigger */}
                        <button
                            onClick={() => setIsNavOpen(true)}
                            className="p-1.5 rounded-xl bg-teal-500/10 hover:bg-teal-500/20 text-teal-300 border border-teal-500/30 transition shadow-sm cursor-pointer"
                            title="Open All Navigation Sections (3-Dots)"
                        >
                            <MoreVertical className="w-4 h-4" />
                        </button>
                    </div>
                </header>

                {/* Page Content */}
                <div className="flex-1 w-full px-4 py-5 lg:px-8 lg:py-6">
                    {children}
                </div>

                {/* Footer Signature */}
                <footer className="w-full px-6 py-4 border-t border-white/[0.06] bg-slate-950/80 backdrop-blur-md flex flex-col sm:flex-row items-center justify-between text-xs text-slate-400 gap-2">
                    <div className="flex items-center gap-2">
                        <Image
                            src="/logo_32.png"
                            alt="Veracity AI Logo"
                            width={16}
                            height={16}
                            className="object-contain drop-shadow-[0_0_4px_rgba(20,184,166,0.5)]"
                            unoptimized
                        />
                        <span>Veracity AI Platform • MCA 2025–2027 (Sem III)</span>
                    </div>
                    <div className="flex items-center gap-1.5 text-[11px]">
                        <span>Project Designed & Developed by</span>
                        <strong className="text-teal-300 font-semibold">Divyanshu Yadav</strong>
                        <span className="text-slate-500">(Roll No: 25MCA00PY0036)</span>
                        <span className="text-slate-500">•</span>
                        <span className="text-slate-400">Under Guidance of Dr. R. Sunitha</span>
                    </div>
                </footer>
            </main>

            {/* Global Movable & Draggable Veracity AI Logo Widget (Fixed to Viewport, Never Hidden by Scroll) */}
            <motion.div
                drag
                dragMomentum={false}
                whileHover={{ scale: 1.08 }}
                whileDrag={{ scale: 1.15, cursor: 'grabbing' }}
                onDragStart={() => {
                    isDragging.current = true;
                }}
                onDragEnd={() => {
                    setTimeout(() => {
                        isDragging.current = false;
                    }, 80);
                }}
                className="fixed bottom-6 right-6 z-50 cursor-grab active:cursor-grabbing select-none touch-none"
            >
                <button
                    onClick={() => {
                        if (!isDragging.current) {
                            setIsNavOpen(true);
                        }
                    }}
                    className="p-2.5 rounded-2xl bg-slate-900/95 hover:bg-slate-800/95 border-2 border-teal-400/60 hover:border-teal-300 backdrop-blur-2xl shadow-[0_0_20px_rgba(20,184,166,0.35)] hover:shadow-[0_0_25px_rgba(20,184,166,0.6)] transition-all duration-200 group cursor-grab active:cursor-grabbing flex items-center gap-2.5"
                    title="Veracity AI (Hold & Drag anywhere on screen • Click to open sections)"
                >
                    <div className="relative w-9 h-9 rounded-xl bg-slate-950 border border-teal-500/50 flex items-center justify-center p-1 shadow-md group-hover:border-teal-300 transition shrink-0 pointer-events-none">
                        <Image
                            src="/logo_64.png"
                            alt="Veracity AI Logo"
                            width={26}
                            height={26}
                            draggable={false}
                            className="object-contain drop-shadow-[0_0_8px_rgba(20,184,166,0.7)] pointer-events-none"
                            priority
                            unoptimized
                        />
                    </div>
                    <span className="text-xs font-black bg-gradient-to-r from-teal-300 via-cyan-300 to-blue-400 bg-clip-text text-transparent pr-1.5 hidden sm:inline pointer-events-none tracking-wide">
                        Veracity AI
                    </span>
                </button>
            </motion.div>

            <Toaster
                theme="dark"
                toastOptions={{
                    className: 'glass border-white/6 text-foreground',
                }}
            />
        </div>
    );
}
