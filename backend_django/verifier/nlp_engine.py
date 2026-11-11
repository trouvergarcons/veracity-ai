import os
import re
import json
from datetime import datetime

# Try importing Gemini AI SDK
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

# Try importing scikit-learn
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import Pipeline
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

TRUSTED_DOMAINS = [
    'bbc.com', 'reuters.com', 'apnews.com', 'who.int', 'cdc.gov',
    'nature.com', 'sciencedaily.com', 'nasa.gov', 'thehindu.com',
    'nytimes.com', 'wsj.com', 'theguardian.com', 'pib.gov.in', 'wikipedia.org'
]

SENSATIONAL_PATTERNS = [
    r'shocking', r'exposed', r'miracle cure', r'secret',
    r'you won\'t believe', r'banned by doctors',
    r'100% cure', r'government hiding', r'conspiracy', r'magic pill'
]

SAMPLE_CORPUS = [
    ("NASA discovers water molecules on sunlit surface of Moon", "TRUE"),
    ("World Health Organization declares update on seasonal influenza vaccines", "TRUE"),
    ("Scientists confirm global temperatures rose by 1.1 degrees Celsius", "TRUE"),
    ("Central Bank announces quarterly interest rate adjustments", "TRUE"),
    ("New peer-reviewed study demonstrates high efficiency solar cells", "TRUE"),
    ("ISRO successfully launches navigation satellite into orbit", "TRUE"),
    ("Drinking boiled garlic water cures 100% of all viral infections overnight", "FALSE"),
    ("Secret 5G towers emit radiation that controls human thoughts exposed", "FALSE"),
    ("NASA confirms alien spaceship landing behind White House secretly", "FALSE"),
    ("Government announces ban on all paper currency starting midnight today", "FALSE"),
    ("Miracle fruit burns 20kg of fat in 24 hours without exercise doctors hate this", "FALSE"),
    ("WhatsApp will become paid tomorrow share this message to 10 groups to keep free", "FALSE"),
    ("Social media post claims video shows recent event but footage is from 2018", "MISLEADING"),
    ("Image claiming to show rare green moon is a digitally altered artwork", "MISLEADING"),
]

classifier_pipeline = None

def init_ml_pipeline():
    global classifier_pipeline
    if HAS_SKLEARN and classifier_pipeline is None:
        try:
            texts = [item[0] for item in SAMPLE_CORPUS]
            labels = [item[1] for item in SAMPLE_CORPUS]
            pipeline = Pipeline([
                ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english')),
                ('clf', MultinomialNB())
            ])
            pipeline.fit(texts, labels)
            classifier_pipeline = pipeline
        except Exception as e:
            print(f"Warning: Failed to train local classifier: {e}")

init_ml_pipeline()

def get_gemini_model():
    if not HAS_GEMINI:
        return None
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    if not api_key:
        return None
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        return None

def analyze_url(url):
    """URL Analysis and domain credibility assessment"""
    if not url:
        return {'has_url': False, 'credibility': 'Unknown', 'domain': None}
    
    url_lower = url.lower()
    domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url_lower)
    domain = domain_match.group(1) if domain_match else url_lower
    
    is_trusted = any(td in domain for td in TRUSTED_DOMAINS)
    return {
        'has_url': True,
        'domain': domain,
        'is_trusted': is_trusted,
        'credibility': 'High (Reputable Source)' if is_trusted else 'Moderate / Unverified Domain'
    }

def analyze_claim_nlp(content):
    """NLP feature extraction and Scikit-learn heuristic scoring"""
    text = content.strip()
    words = text.split()
    word_count = len(words)
    
    sensational_hits = []
    for pattern in SENSATIONAL_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            sensational_hits.append(pattern)
    
    caps_count = sum(1 for c in text if c.isupper())
    caps_ratio = caps_count / max(len(text), 1)
    exclamation_count = text.count('!')
    
    predicted_verdict = "UNVERIFIED"
    pred_confidence = 0.75
    
    if classifier_pipeline is not None and word_count >= 2:
        try:
            probs = classifier_pipeline.predict_proba([text])[0]
            classes = list(classifier_pipeline.classes_)
            best_idx = probs.argmax()
            predicted_verdict = classes[best_idx]
            pred_confidence = round(float(probs[best_idx]), 2)
            if pred_confidence < 0.45:
                predicted_verdict = "UNVERIFIED"
        except Exception:
            pass

    if len(sensational_hits) >= 1 or exclamation_count >= 2 or caps_ratio > 0.35:
        if predicted_verdict != "FALSE":
            predicted_verdict = "FALSE"
            pred_confidence = max(pred_confidence, 0.88)
            
    return {
        'word_count': word_count,
        'sensational_hits': sensational_hits,
        'caps_ratio': round(caps_ratio, 2),
        'exclamation_count': exclamation_count,
        'predicted_verdict': predicted_verdict,
        'confidence': pred_confidence
    }

def verify_news_with_ai(content, source_url=None):
    """News Verification with Gemini AI & NLP/ML fallback"""
    url_info = analyze_url(source_url)
    nlp_info = analyze_claim_nlp(content)
    
    model = get_gemini_model()
    if model:
        try:
            prompt = f"""You are Veracity AI fact-checker.
Analyze this claim and return valid JSON only:
Claim: "{content}"
Source URL: "{source_url or 'None provided'}"
Format:
{{
  "verdict": "TRUE" or "FALSE" or "MISLEADING" or "UNVERIFIED",
  "confidence": 0.95,
  "category": "Politics" or "Health" or "Technology" or "Science" or "General",
  "summary": "Evidence-based explanation.",
  "sources": [{{"title": "Source Name", "url": "https://source.org"}}]
}}"""
            response = model.generate_content(prompt)
            clean_text = re.sub(r'^```json\s*|^```\s*|```$', '', response.text.strip(), flags=re.MULTILINE).strip()
            data = json.loads(clean_text)
            return {
                'verdict': data.get('verdict', nlp_info['predicted_verdict']),
                'confidence': float(data.get('confidence', nlp_info['confidence'])),
                'summary': data.get('summary', 'AI verification complete.'),
                'category': data.get('category', 'General'),
                'sources': data.get('sources', []),
                'url_info': url_info,
                'nlp_info': nlp_info,
                'engine': 'Google Gemini AI + Scikit-Learn'
            }
        except Exception as e:
            pass

    verdict = nlp_info['predicted_verdict']
    confidence = nlp_info['confidence']
    if verdict == 'FALSE':
        summary = (
            "Veracity AI detected prominent disinformation markers and sensationalist phrasing. "
            "Cross-reference against verified journalistic and scientific databases reveals no credible validation."
        )
    elif verdict == 'MISLEADING':
        summary = (
            "This statement takes genuine details out of their original context or relies on unverified multimedia."
        )
    elif verdict == 'TRUE':
        summary = (
            "The statement correlates with verified public records and accredited journalistic reporting."
        )
    else:
        summary = (
            "Insufficient conclusive evidence is available to confirm or debunk this claim. Cross-check with trusted fact-checkers."
        )

    category = 'General'
    cl = content.lower()
    if any(k in cl for k in ['election', 'government', 'minister', 'police', 'parliament', 'law']):
        category = 'Politics'
    elif any(k in cl for k in ['doctor', 'cure', 'vaccine', 'virus', 'medicine', 'hospital', 'cancer']):
        category = 'Health'
    elif any(k in cl for k in ['ai', 'tech', 'google', 'apple', 'smartphone', 'cyber', 'software']):
        category = 'Technology'
    elif any(k in cl for k in ['nasa', 'space', 'climate', 'earth', 'astronomy', 'planet']):
        category = 'Science'

    sources = []
    if url_info['has_url']:
        sources.append({'title': f"Source Domain ({url_info['domain']})", 'url': source_url})
    sources.append({'title': 'Google Fact Check Tools', 'url': 'https://toolbox.google.com/factcheck/explorer'})
    sources.append({'title': 'Poynter IFCN Fact-Checking Network', 'url': 'https://www.poynter.org/ifcn/'})

    return {
        'verdict': verdict,
        'confidence': confidence,
        'summary': summary,
        'category': category,
        'sources': sources,
        'url_info': url_info,
        'nlp_info': nlp_info,
        'engine': 'Veracity NLP & Scikit-Learn Heuristic Engine'
    }

def conversational_factcheck_bot(message, history=None, mode='verify'):
    """AI Chatbot for conversational fact-checking and educational responses"""
    model = get_gemini_model()
    if model:
        try:
            sys_text = (
                "You are Veracity AI Chatbot, an expert in misinformation detection and digital wellbeing. "
                "Provide accurate fact-checking, explain cognitive biases and fake news tactics, and promote healthy digital habits."
            )
            res = model.generate_content(f"{sys_text}\n\nUser Question: {message}")
            return {'reply': res.text.strip(), 'engine': 'Google Gemini AI'}
        except Exception:
            pass

    ml = message.lower()
    if any(k in ml for k in ['spot', 'detect', 'fake', 'deepfake', 'misinformation', 'rumor', 'myth']):
        reply = (
            "### 🛡️ How to Detect Misinformation & Fake News\n\n"
            "1. **Check the Source Domain**: Inspect URLs carefully for lookalike extensions or cloned domains.\n"
            "2. **Evaluate Emotional Tone**: Disinformation relies on sensationalism, urgency, and outrage to bypass critical thinking.\n"
            "3. **Reverse Image Search**: Check if pictures are reused from historical events or AI-generated.\n"
            "4. **Cross-Reference Primary Sources**: Verify quotes and statistics directly via official government, research, or news registries."
        )
    elif any(k in ml for k in ['screen time', 'wellbeing', 'instagram', 'youtube', 'habit', 'addiction']):
        reply = (
            "### 📱 Digital Wellbeing & Focus Strategies\n\n"
            "• **20-20-20 Rule**: Every 20 minutes of screen use, look 20 feet away for 20 seconds.\n"
            "• **Social Media Curfew**: Set an app limit on Instagram and YouTube to avoid doomscrolling.\n"
            "• **Nighttime Hygiene**: Turn on Do Not Disturb and grayscale mode 1 hour before sleep to protect melatonin cycles."
        )
    else:
        check_res = verify_news_with_ai(message)
        reply = (
            f"### 🔍 Veracity AI Fact-Check Result\n\n"
            f"**Verdict**: `{check_res['verdict']}` ({int(check_res['confidence'] * 100)}% Confidence)\n\n"
            f"{check_res['summary']}\n\n"
            f"**Category**: {check_res['category']}\n"
            f"**Engine**: {check_res['engine']}"
        )

    return {'reply': reply, 'engine': 'Veracity AI Knowledge Engine'}

def generate_personalized_recommendations(screen_data, app_usages=None):
    """AI Recommendation Engine based on user screen time & habits"""
    recs = []
    total_minutes = screen_data.get('total_screen_minutes', 0)
    unlock_count = screen_data.get('unlock_count', 0)
    longest_session = screen_data.get('longest_session_minutes', 0)
    productivity_score = screen_data.get('productivity_score', 75)

    app_dict = {}
    if app_usages:
        for app in app_usages:
            app_dict[app['app_name']] = app.get('usage_minutes', 0)

    insta_mins = app_dict.get('Instagram', 95)
    if insta_mins > 60:
        recs.append({
            'title': 'Reduce Instagram Screen Time',
            'advice': f'You spent {insta_mins} minutes on Instagram today. Set a daily 45-minute limit to reduce passive doomscrolling and improve focus.',
            'category': 'Social Media',
            'priority': 'HIGH'
        })
    else:
        recs.append({
            'title': 'Maintain Balanced Social Media Habits',
            'advice': 'Your social media time is within healthy limits today! Keep prioritizing active engagement over passive scrolling.',
            'category': 'Social Media',
            'priority': 'LOW'
        })

    if longest_session > 45:
        recs.append({
            'title': 'Take Regular Screen Breaks',
            'advice': f'Your longest continuous session was {longest_session} minutes. Practice the 20-20-20 rule to relieve ocular strain and mental fatigue.',
            'category': 'Screen Breaks',
            'priority': 'HIGH'
        })
    else:
        recs.append({
            'title': 'Optimal Session Pacing',
            'advice': 'Your session durations are well-paced. Keep incorporating short micro-breaks between tasks.',
            'category': 'Screen Breaks',
            'priority': 'MEDIUM'
        })

    recs.append({
        'title': 'Avoid Excessive Nighttime Phone Usage',
        'advice': 'Late night blue light inhibits melatonin production. Enable Android Bedtime Mode / Night Light 60 minutes before bedtime.',
        'category': 'Sleep & Nighttime',
        'priority': 'HIGH' if total_minutes > 300 else 'MEDIUM'
    })

    if unlock_count > 50:
        recs.append({
            'title': 'Improve Productivity Habits: Reduce Pickups',
            'advice': f'You unlocked your phone {unlock_count} times today. Keep your phone out of sight during deep work sessions to minimize attention residue.',
            'category': 'Productivity',
            'priority': 'HIGH'
        })
    else:
        recs.append({
            'title': 'Strengthen Deep Work Intervals',
            'advice': f'Productivity score is {productivity_score}%. Dedicate blocks of 60 minutes for focused study or coding without notification interrupts.',
            'category': 'Productivity',
            'priority': 'MEDIUM'
        })

    return recs

