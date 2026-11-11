'use client';

import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Shield, Lock, Mail, ArrowRight, Sparkles, CheckCircle2 } from 'lucide-react';
import { toast } from 'sonner';
import CyberGlobe3D from '@/components/3d/CyberGlobe3D';
import { backendApi } from '@/lib/config';

export default function LoginPage() {
  const router = useRouter();
  const [identifier, setIdentifier] = useState('divyanshu');
  const [password, setPassword] = useState('password123');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!identifier || !password) {
      toast.error('Please enter both username/email and password');
      return;
    }

    setIsLoading(true);
    const toastId = toast.loading('Signing in to Veracity AI...');

    try {
      const res = await fetch(backendApi('/api/auth/login/'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: identifier, password })
      });

      const data = await res.json();
      toast.dismiss(toastId);

      if (res.ok && data.success) {
        toast.success(`Welcome back, ${data.user.full_name}!`);
        localStorage.setItem('veracity_user', JSON.stringify(data.user));
        router.push('/');
      } else {
        // Allow demo login fallback
        toast.success('Signed in as Divyanshu Yadav (Demo Mode)');
        localStorage.setItem('veracity_user', JSON.stringify({
          id: 1,
          username: identifier,
          full_name: 'Divyanshu Yadav',
          email: 'divyanshu@veracity.ai'
        }));
        router.push('/');
      }
    } catch (err) {
      toast.dismiss(toastId);
      toast.success('Signed in as Divyanshu Yadav (Offline Demo)');
      localStorage.setItem('veracity_user', JSON.stringify({
        id: 1,
        username: identifier,
        full_name: 'Divyanshu Yadav',
        email: 'divyanshu@veracity.ai'
      }));
      router.push('/');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-slate-950 text-white relative overflow-hidden">
      {/* Interactive Cyber Background */}
      <CyberGlobe3D opacity={0.65} className="z-0" />

      {/* Ambient Cosmic Radial Glows matching Dashboard */}
      <div className="absolute top-0 left-1/3 w-[800px] h-[450px] rounded-full bg-teal-500/[0.08] blur-[150px] pointer-events-none z-[1]" />
      <div className="absolute bottom-0 right-0 w-[600px] h-[400px] rounded-full bg-cyan-500/[0.06] blur-[130px] pointer-events-none z-[1]" />
      <div className="absolute top-1/2 -left-20 w-[450px] h-[450px] rounded-full bg-purple-500/[0.06] blur-[140px] pointer-events-none z-[1]" />

      <Card className="max-w-md w-full bg-slate-900/85 border-teal-500/30 backdrop-blur-xl shadow-2xl relative z-10">
        <CardHeader className="text-center space-y-2 pb-5">
          {/* Glowing Veracity AI Logo */}
          <div className="mx-auto relative group mb-1">
            <div className="absolute -inset-1.5 rounded-2xl bg-gradient-to-tr from-teal-400 to-cyan-400 opacity-50 blur-md group-hover:opacity-85 transition duration-500 animate-pulse" />
            <div className="relative w-16 h-16 rounded-2xl bg-slate-950 border border-teal-500/50 flex items-center justify-center p-2 shadow-xl">
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
            Veracity AI
          </CardTitle>

          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-teal-500/10 border border-teal-500/30 text-teal-300 text-[10px] font-extrabold uppercase tracking-wider mx-auto">
            <Sparkles className="w-3 h-3 text-amber-400 animate-spin" style={{ animationDuration: '6s' }} />
            <span>DESIGN BY DIVYANSHU YADAV</span>
          </div>

          <CardDescription className="text-xs text-slate-400 pt-0.5">
            Sign in to access AI Fact Verification & Digital Wellbeing Platform
          </CardDescription>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-1.5">
              <Label className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                <Mail className="w-3.5 h-3.5 text-slate-400" />
                Username or Email
              </Label>
              <Input
                type="text"
                placeholder="Username or email"
                value={identifier}
                onChange={(e) => setIdentifier(e.target.value)}
                className="bg-slate-950/60 border-white/10 text-white placeholder:text-slate-500 text-sm h-10"
              />
            </div>

            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <Label className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                  <Lock className="w-3.5 h-3.5 text-slate-400" />
                  Password
                </Label>
                <Link
                  href="/forgot-password"
                  className="text-[11px] text-teal-400 hover:text-teal-300 transition"
                >
                  Forgot password?
                </Link>
              </div>
              <Input
                type="password"
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="bg-slate-950/60 border-white/10 text-white placeholder:text-slate-500 text-sm h-10"
              />
            </div>

            <Button
              type="submit"
              disabled={isLoading}
              className="w-full h-10 bg-gradient-to-r from-teal-500 to-cyan-500 hover:from-teal-400 hover:to-cyan-400 text-slate-950 font-extrabold text-sm transition shadow-lg shadow-teal-500/20 cursor-pointer"
            >
              {isLoading ? 'Signing In...' : 'Sign In'}
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>

            <div className="pt-4 border-t border-white/5 text-center text-xs text-slate-400">
              Don&apos;t have an account?{' '}
              <Link href="/register" className="text-teal-400 font-semibold hover:underline">
                Register now
              </Link>
            </div>

            <div className="mt-3 p-2.5 rounded-xl bg-slate-950/60 border border-white/5 text-[11px] text-slate-400 text-center flex items-center justify-center gap-2">
              <span className="text-teal-300 font-bold">25MCA00PY0036</span>
              <span>•</span>
              <span>MCA 2025–2027 (Sem III)</span>
              <span>•</span>
              <span className="text-slate-300 font-medium">Guide: Dr. R. Sunitha</span>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

