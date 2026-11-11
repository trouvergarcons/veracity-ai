import { NextResponse } from 'next/server';
import { authenticateToken } from '@/lib/auth';
import { verifyClaim } from '@/lib/verify';

// CORS headers for extension requests
const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

export async function OPTIONS() {
    return NextResponse.json({}, { headers: corsHeaders });
}

export async function POST(req) {
    const auth = await authenticateToken(req);
    if (auth.error) {
        return NextResponse.json({ error: auth.error }, { status: auth.status, headers: corsHeaders });
    }

    try {
        const { platform, postContent, imageUrls, pageUrl } = await req.json();

        if (!postContent && !pageUrl) {
            return NextResponse.json(
                { error: 'postContent or pageUrl is required' },
                { status: 400, headers: corsHeaders }
            );
        }

        const content = postContent || `Content from: ${pageUrl}`;
        const result = await verifyClaim(content, pageUrl);

        return NextResponse.json({
            ...result,
            platform: platform || 'unknown',
            checkedAt: new Date().toISOString(),
        }, { headers: corsHeaders });

    } catch (error) {
        console.error('Extension check error:', error);
        return NextResponse.json(
            { error: error.message || 'Failed to verify' },
            { status: 500, headers: corsHeaders }
        );
    }
}
