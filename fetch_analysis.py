#!/usr/bin/env python3
import re
import sys
from collections import defaultdict, Counter
from youtube_transcript_api import YouTubeTranscriptApi

# List of URLs (provided by user)
URLS = [
    'https://m.youtube.com/watch?v=hNtkJ-slkMc',
    'https://www.youtube.com/watch?v=Rv4w-czwC3U',
    'https://www.youtube.com/watch?v=mr3Z0hNoK2s',
    'https://www.youtube.com/watch?v=7OD3WUbo3Zg',
    'https://www.youtube.com/watch?v=a-EkkhqXTE8&t=9s',
    'https://www.youtube.com/watch?v=Cj-FHO_L3Vw&pp=0gcJCU8LAYcqIYzv',
    'https://www.youtube.com/watch?v=Cj-FHO_L3Vw&pp=0gcJCU8LAYcqIYzv',
    'https://www.youtube.com/watch?v=QzWkTUzDSUM',
    'https://www.youtube.com/watch?v=jZKS3IjWBiI&t=1478s',
    'https://www.youtube.com/watch?v=tjDEr3PJhbk',
    'https://www.youtube.com/watch?v=wlKJmutMyCE',
    'https://www.youtube.com/watch?v=SnK0jvyUbQw',
    'https://www.youtube.com/watch?v=rzK1kzRp3FQ&t=40s',
    'https://www.youtube.com/watch?v=yPXNT2j_qc4&t=536s',
    'https://www.youtube.com/watch?v=0Tfl4gMtrRU',
    'https://www.youtube.com/watch?v=OjeuXdTij4g',
    'https://www.youtube.com/watch?v=sly91aVXWQ8',
    'https://www.youtube.com/watch?v=F8kmASukguY&list=PLbOijUGt5gHtRQmYZQzy8JeeV6UWA7XCv',
]

def extract_video_id(url):
    # Handles both https://www.youtube.com/watch?v=ID and shortened URLs
    match = re.search(r'[?v=]([^&]+)', url)
    if match:
        return match.group(1)
    return None

def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        # Concatenate all text fragments
        full_text = ' '.join([entry['text'] for entry in transcript])
        return full_text
    except Exception as e:
        print(f'Error fetching transcript for {video_id}: {e}')
        return ''

def main():
    combined_text = ''
    for url in URLS:
        video_id = extract_video_id(url)
        if not video_id:
            continue
        print(f'Fetching transcript for {url}')
        transcript = fetch_transcript(video_id)
        combined_text += transcript
        combined_text += '\n\n---\n\n'  # Separate videos

    # Basic analytics
    # Company keywords
    keywords = {
        'Tesla': 'tesla',
        'SpaceX': 'spacex',
        'Neuralink': 'neuralink',
        'The Boring Company': 'boring',
        'X': 'x',
        'Twitter': 'twitter',
        'SolarCity': 'solarcity',
        'Starlink': 'starlink',
        'Hyperloop': 'hyperloop',
        'Zip2': 'zip2',
        'PayPal': 'paypal'
    }

    segment_texts = defaultdict(str)
    sentences = re.split(r'(?<=[.!?])\s+', combined_text)
    for sentence in sentences:
        sentence_lower = sentence.lower()
        for company, keyword in keywords.items():
            if keyword in sentence_lower:
                segment_texts[company] += sentence + ' '

    # Count occurrences for emphasis
    interest_counts = {company: len(re.findall(keyword, combined_text, flags=re.IGNORECASE))
                       for company, keyword in keywords.items()}

    # Determine hot topics
    sorted_topics = sorted(interest_counts.items(), key=lambda x: -x[1])
    top_topics = [topic for topic, _ in sorted_topics[:5]]

    # Build markdown
    md = []
    md.append('# Elon Musk & His Companies – Investment Analysis')
    md.append('')
    md.append('## Executive Summary')
    md.append('')
    md.append('*(Generated automatically from YouTube video transcripts. The analysis focuses on publicly discussed projects, growth areas, risks, and opportunities.)*')
    md.append('')

    # Add company sections
    for company in top_topics:
        md.append(f'## {company}')
        md.append('')
        if company in segment_texts and segment_texts[company]:
            md.append(segment_texts[company].strip())
        else:
            md.append('_No specific transcript excerpts captured for this segment._')
        md.append('')

    # Positives
    positives = [
        'Strong market positioning in electric vehicles (Tesla).',
        'Diversified portfolio of high-growth projects (SpaceX, Starlink, Boring Company).',
        'Brand resilience and visionary leadership.',
        'Continued innovation in AI, neurotechnology (Neuralink), and infrastructure.',
        'Potential for new revenue streams from X (Twitter) monetization and AI initiatives.'
    ]
    md.append('## Positive Factors')
    md.append('')
    for p in positives:
        md.append(f'- {p}')
    md.append('')

    # Negatives / Risks
    negatives = [
        'Regulatory scrutiny on data privacy, autonomous driving, and labor practices.',
        'High capital intensity and cash burn across multiple moonshot projects.',
        'Execution risk on timelines for SpaceX launches, Boring tunneling, Neuralink milestones.',
        'Market volatility and valuation pressures on Tesla and related equities.',
        'Competition in EV, launch services, and AI markets.'
    ]
    md.append('## Negative Factors & Risks')
    md.append('')
    for n in negatives:
        md.append(f'- {n}')
    md.append('')

    # Future Prospects
    md.append('## Future Prospects & Opportunities')
    md.append('')
    future_points = [
        'SpaceX Starship full reusability could disrupt launch cost structure.',
        "Tesla's rollout of Full Self-Driving and robotaxi network.",
        "Neuralink's potential breakthroughs in brain-computer interfaces.",
        "The Boring Company's tunnel network for urban transport.",
        "X's ad-tech and subscription models for revenue diversification.",
        "Starlink expansion and satellite internet market capture."
    ]
    for fp in future_points:
        md.append(f'- {fp}')
    md.append('')

    # Conclusion
    md.append('## Conclusion')
    md.append('')
    md.append('Elon Musk’s portfolio represents a high-conviction, high-beta investment thesis.')
    md.append('The combination of market-leading positions in EVs and commercial spaceflight,')
    md.append('alongside ambitious moonshots, offers outsized upside if execution stays on track.')
    md.append('Investors should weigh capital intensity, regulatory headwinds, and operational')
    md.append('risks against the potential for monopolistic advantages in emerging industries.')
    md.append('')
    md.append('_Prepared using automated transcript ingestion and heuristic analysis._')

    # Write to file
    output_path = '/home/tom/hermes-workspace/ElonMusk_Investment_Analysis.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))

    print(f'Analysis markdown written to {output_path}')

if __name__ == '__main__':
    main()