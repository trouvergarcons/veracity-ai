'use client';

import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Shield, Mail, ArrowLeft, CheckCircle2, Sparkles } from 'lucide-react';
import { toast } from 'sonner';
import CyberGlobe3D from '@/components/3d/CyberGlobe3D';
import { backendApi } from '@/lib/config';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleReset = async (e) => {
    e.preventDefault();
    if (!email) {
      toast.error('Please enter your email address');
      return;
    }

    setIsLoading(true);
    const toastId = toast.loading('Sending password recovery instructions...');

    try {
      const res = await fetch(backendApi('/api/auth/reset-password/'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });

      toast.dismiss(toastId);
      setSubmitted(true);
      toast.success('Password recovery instructions sent!');
    } catch (err) {
      toast.dismiss(toastId);
      setSubmitted(true);
      toast.success('Password recovery instructions sent!');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-slate-950 text-white relative overflow-hidden">
      {/* Interactive Background */}
      <CyberGlobe3D opacity={0.65} className="z-0" />

      {/* Ambient Cosmic Radial Glows */}
      <div className="absolute top-0 left-1/3 w-[800px] h-[450px] rounded-full bg-teal-500/[0.08] blur-[150px] pointer-events-none z-[1]" />
      <div className="absolute bottom-0 right-0 w-[600px] h-[400px] rounded-full bg-cyan-500/[0.06] blur-[130px] pointer-events-none z-[1]" />
      <div className="absolute top-1/2 -left-20 w-[450px] h-[450px] rounded-full bg-purple-500/[0.06] blur-[140px] pointer-events-none z-[1]" />

      <Card className="max-w-md w-full bg-slate-900/85 border-teal-500/30 backdrop-blur-xl shadow-2xl relative z-10">
        <CardHeader className="text-center space-y-2 pb-5">
          {/* Glowing Veracity AI Logo */}
          <div className="mx-auto relative group mb-1">
            <div className="absolute -inset-1.5 rounded-2xl bg-gradient-to-tr from-teal-400 to-cyan-400 opacity-50 blur-md group-hover:opacity-85 transition duration-500 animate-pulse" />
            <div className="relative w-16 h-16 rounded-2xl bg-slate-950 border border-teal-500/50 flex items-center justify-center p-2.5 shadow-xl">
              <Image
                src="/logo_128.png"
                alt="Veracity AI Logo"
                width={48}
                height={48}
                className="object-contain drop-shadow-[0_0_12px_rgba(20,184,166,0.7)]"
                priority
                unoptimized
              />
            </div>
          </div>

          <CardTitle className="text-2xl font-extrabold bg-gradient-to-r from-teal-200 via-cyan-300 to-blue-400 bg-clip-text text-transparent">
            Password Recovery
          </CardTitle>

          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-teal-500/10 border border-teal-500/30 text-teal-300 text-[10px] font-extrabold uppercase tracking-wider mx-auto">
            <Sparkles className="w-3 h-3 text-amber-400 animate-spin" style={{ animationDuration: '6s' }} />
            <span>DESIGN BY DIVYANSHU YADAV</span>
          </div>

          <CardDescription className="text-xs text-slate-400 pt-0.5">
            {submitted
              ? 'Check your inbox for the password reset instructions.'
              : 'Enter your registered email address to receive recovery steps.'}
          </CardDescription>
        </CardHeader>

        <CardContent>
          {submitted ? (
            <div className="space-y-5 text-center">
              <div className="mx-auto w-14 h-14 rounded-full bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                <CheckCircle2 className="w-8 h-8" />
              </div>
              <p className="text-xs text-slate-300">
                A verification link and token have been issued for <strong>{email}</strong>.
              </p>
              <Link href="/login">
                <Button className="w-full bg-slate-800 hover:bg-slate-700 text-white text-xs">
                  <ArrowLeft className="w-3.5 h-3.5 mr-2" /> Back to Sign In
                </Button>
              </Link>
            </div>
          ) : (
            <form onSubmit={handleReset} className="space-y-4">
              <div className="space-y-1.5">
                <Label className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                  <Mail className="w-3.5 h-3.5 text-slate-400" />
                  Email Address
                </Label>
                <Input
                  type="email"
                  placeholder="name@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="bg-slate-950/60 border-white/10 text-white placeholder:text-slate-500 text-sm h-10"
                />
              </div>

              <Button
                type="submit"
                disabled={isLoading}
                className="w-full h-10 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold text-sm transition"
              >
                {isLoading ? 'Sending...' : 'Send Recovery Link'}
              </Button>

              <div className="pt-3 text-center">
                <Link
                  href="/login"
                  className="inline-flex items-center text-xs text-slate-400 hover:text-white transition"
                >
                  <ArrowLeft className="w-3.5 h-3.5 mr-1" /> Back to Login
                </Link>
              </div>

              <div className="mt-4 p-2.5 rounded-xl bg-slate-950/60 border border-white/5 text-[11px] text-slate-400 text-center flex items-center justify-center gap-2">
                <span className="text-teal-300 font-bold">25MCA00PY0036</span>
                <span>•</span>
                <span>MCA 2025–2027 (Sem III)</span>
                <span>•</span>
                <span className="text-slate-300 font-medium">Guide: Dr. R. Sunitha</span>
              </div>
            </form>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

