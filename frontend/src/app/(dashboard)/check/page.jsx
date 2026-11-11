'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useMutation } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { VerdictDisplay } from '@/components/Verdict';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import {
  Search,
  Globe,
  ExternalLink,
  Sparkles,
  ThumbsUp,
  ThumbsDown,
  Link2,
  Home,
  RefreshCw,
  ArrowLeft,
  CheckCircle
} from 'lucide-react';

export default function QuickCheckPage() {
  const [textInput, setTextInput] = useState('');
  const [urlInput, setUrlInput] = useState('');
  const [activeTab, setActiveTab] = useState('text');
  const [result, setResult] = useState(null);

  const verifyMutation = useMutation({
    mutationFn: async ({ content, url }) => {
      const res = await fetch('/api/verify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: content || `Analyze: ${url}`,
          source_url: url,
        }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || 'Verification failed');
      }

      return res.json();
    },

    onSuccess: (data) => {
      setResult(data);
    },

    onError: (error) => {
      toast.error(error.message);
    },
  });

  const feedbackMutation = useMutation({
    mutationFn: async (vars) => {
      return { success: true };
    },

    onSuccess: (_, vars) => {
      toast.success(
        vars.isCorrect
          ? 'Thanks! Marked.'
          : "Thanks! We'll review this verdict."
      );
    },
  });

  const handleCheck = () => {
    if (activeTab === 'text' && textInput.trim()) {
      verifyMutation.mutate({ content: textInput });
    } else if (activeTab === 'url' && urlInput.trim()) {
      verifyMutation.mutate({ url: urlInput });
    }
  };

  return (
    <div className="flex flex-col h-full space-y-6 max-w-3xl mx-auto">

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/10 pb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-white/[0.06] flex items-center justify-center">
            <Search className="w-5 h-5 text-emerald-400" />
          </div>

          <div>
            <h1 className="text-2xl font-bold tracking-tight">Quick Check</h1>
            <p className="text-xs text-muted-foreground flex items-center gap-1.5 mt-0.5">
              <span>Instant AI-powered claim verification</span>
              <span>•</span>
              <span className="text-teal-400 font-medium">Designed by Divyanshu Yadav (25MCA00PY0036)</span>
            </p>
          </div>
        </div>

        <Button
          asChild
          variant="outline"
          size="sm"
          className="border-white/10 bg-white/5 hover:bg-white/10 text-xs text-slate-200 self-start sm:self-auto cursor-pointer"
        >
          <Link href="/">
            <Home className="w-3.5 h-3.5 mr-1.5 text-teal-400" />
            Home Page
          </Link>
        </Button>
      </div>

      {/* Input Card */}
      <Card className="glass border-white/[0.06] overflow-hidden">
        <CardContent className="p-5 space-y-4">

          <Tabs value={activeTab} onValueChange={setActiveTab}>

            <TabsList className="glass border border-white/[0.06] bg-transparent h-9">

              <TabsTrigger value="text" className="text-xs gap-1.5">
                <Sparkles className="w-3 h-3" />
                Claim Text
              </TabsTrigger>

              <TabsTrigger value="url" className="text-xs gap-1.5">
                <Link2 className="w-3 h-3" />
                URL / Link
              </TabsTrigger>

            </TabsList>

            <TabsContent value="text" className="mt-4">
              <Textarea
                value={textInput}
                onChange={(e) => setTextInput(e.target.value)}
                placeholder="Type or paste a claim to verify..."
                rows={4}
                className="bg-white/[0.02] border-white/[0.06] text-sm resize-none"
              />
            </TabsContent>

            <TabsContent value="url" className="mt-4">
              <Input
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                placeholder="https://example.com/article..."
                className="bg-white/[0.02] border-white/[0.06] text-sm h-12"
              />
            </TabsContent>

          </Tabs>

          <Button
            onClick={handleCheck}
            disabled={
              verifyMutation.isPending ||
              (activeTab === 'text'
                ? !textInput.trim()
                : !urlInput.trim())
            }
            className="w-full h-11 btn-gradient text-white gap-2"
          >
            {verifyMutation.isPending ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Search className="w-4 h-4" />
                Verify Now
              </>
            )}
          </Button>

        </CardContent>
      </Card>

      {/* Loading */}
      <AnimatePresence>
        {verifyMutation.isPending && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="glass rounded-xl p-5 border border-white/[0.06]"
          >
            <div className="flex items-center gap-4">

              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-emerald-500/20 to-teal-500/20 flex items-center justify-center">
                <Globe className="w-5 h-5 text-emerald-400 animate-pulse" />
              </div>

              <div className="flex-1">
                <p className="text-sm font-medium">
                  Searching the web for evidence...
                </p>

                <p className="text-[11px] text-muted-foreground/50">
                  Querying multiple sources and analyzing credibility
                </p>
              </div>

            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Result */}
      <AnimatePresence>
        {result && !verifyMutation.isPending && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-4"
          >

            <VerdictDisplay
              verdict={result.verdict}
              confidence={result.confidence}
              summary={result.summary}
            />

            {result.sources?.length > 0 && (
              <Card className="glass border-white/[0.06]">
                <CardContent className="p-4 space-y-3">

                  <span className="text-xs text-muted-foreground">
                    Evidence Sources ({result.sources.length})
                  </span>

                  <div className="space-y-2">
                    {result.sources.map((src, i) => (
                      <a
                        key={i}
                        href={src.url}
                        target="_blank"
                        rel="noreferrer"
                        className="flex items-center gap-2 text-xs"
                      >
                        <ExternalLink className="w-3 h-3" />
                        <span className="text-cyan-400">
                          {src.title || src.url}
                        </span>
                      </a>
                    ))}
                  </div>

                </CardContent>
              </Card>
            )}

            {/* Action Bar with Prominent Home Button after Verification */}
            <div className="p-4 rounded-2xl bg-gradient-to-r from-slate-900/95 via-slate-900/80 to-teal-950/40 border border-teal-500/30 flex flex-wrap items-center justify-between gap-3 shadow-xl backdrop-blur-md">
              <div className="flex items-center gap-2.5">
                {/* Home Button */}
                <Button
                  asChild
                  className="bg-gradient-to-r from-teal-500 to-cyan-500 text-slate-950 font-extrabold hover:from-teal-400 hover:to-cyan-400 shadow-md transition cursor-pointer"
                >
                  <Link href="/">
                    <Home className="w-4 h-4 mr-2 fill-slate-950" />
                    Go to Home Page
                  </Link>
                </Button>

                {/* Check Another Claim Button */}
                <Button
                  variant="outline"
                  onClick={() => {
                    setResult(null);
                    setTextInput('');
                    setUrlInput('');
                  }}
                  className="border-white/10 hover:bg-white/5 text-xs text-slate-300"
                >
                  <RefreshCw className="w-3.5 h-3.5 mr-1.5" />
                  Check Another Claim
                </Button>
              </div>

              {/* Feedback buttons */}
              <div className="flex items-center gap-1.5 text-xs text-slate-400">
                <span className="text-[11px] text-slate-500 hidden sm:inline mr-1">Feedback:</span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => feedbackMutation.mutate({ isCorrect: true })}
                  className="hover:text-emerald-400 hover:bg-emerald-500/10 text-xs h-8"
                >
                  <ThumbsUp className="w-3.5 h-3.5 mr-1" />
                  Accurate
                </Button>

                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => feedbackMutation.mutate({ isCorrect: false })}
                  className="hover:text-rose-400 hover:bg-rose-500/10 text-xs h-8"
                >
                  <ThumbsDown className="w-3.5 h-3.5 mr-1" />
                  Inaccurate
                </Button>
              </div>
            </div>

          </motion.div>
        )}
      </AnimatePresence>

    </div>
  );
}