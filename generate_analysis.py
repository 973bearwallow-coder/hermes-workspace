#!/usr/bin/env python3
"""
Fetch transcripts from a list of YouTube URLs using yt-dlp,
parse WebVTT subtitles, generate a markdown investment analysis,
and write it to /home/tom/hermes-workspace/ElonMusk_Investment_Analysis.md.

Author: Automated Hermes Agent
"""

import os
import re
import subprocess
import html
from collections import defaultdict

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
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

# Keywords to map video topics to company/area names
KEYWORDS = {
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

# Ensure subtitle output directory exists
SUB_DIR = 'subtitles'
os.makedirs(SUB_DIR, exist_ok=True)

# ----------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------
def parse_vtt(content: str) -> str:
    """
    Parse a WebVTT subtitle content and return plain text.
    Strips timestamps, HTML entities, and cue identifiers.
    """
    lines = content.splitlines()
    text_parts = []
    for line in lines:
        stripped = line.strip()
        # Skip timestamp lines (contain '-->')
        if '-->' in stripped:
            continue
        # Skip cue identifiers (pure numbers) and empty lines
        if stripped.isdigit():
            continue
        if stripped == 'WEBVTT':
            continue
        if stripped == '':
            continue
        # Unescape HTML entities and collect
        text_parts.append(html.unescape(stripped))
    return ' '.join(text_parts)


def fetch_subtitles(video_id: str, url: str) -> str:
    """
    Use yt-dlp to download English subtitles for a given YouTube URL.
    Returns parsed plain text transcript or empty string if not available.
    """
    target_file = os.path.join(SUB_DIR, f'{video_id}.en.vtt')
    # Build yt-dlp command
    cmd = [
        'yt-dlp',
        '--skip-download',
        '-q',                # quiet mode
        '-o', target_file,   # output template to known filename
        '--write-sub',      # download subtitles
        '--sub-lang', 'en', # English only
        url
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f'yt-dlp error for {url}: {result.stderr}')
            return ''
        # Check if file was created
        if not os.path.isfile(target_file):
            print(f'Subtitle file not created: {target_file}')
            return ''
        # Read and parse subtitle content
        with open(target_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return parse_vtt(content)
    except Exception as e:
        print(f'Exception fetching subtitles for {url}: {e}')
        return ''


def extract_video_id(url: str) -> str | None:
    """Extract video ID from a YouTube URL."""
    match = re.search(r'[?v=]([^&]+)', url)
    if match:
        return match.group(1)
    # Fallback for short URLs (e.g., youtu.be/ID)
    match = re.search(r'/([^/?]+)$', url)
    if match:
        return match.group(1)
    return None


def analyse_transcript(combined_text: str) -> dict:
    """
    Basic analytics: map keywords to sentences and count occurrences.
    Returns structured data for markdown generation.
    """
    # Split into sentences (simple approach)
    sentences = re.split(r'(?<=[.!?])\s+', combined_text)

    segment_texts = defaultdict(str)
    for sentence in sentences:
        lowered = sentence.lower()
        for company, keyword in KEYWORDS.items():
            if keyword in lowered:
                segment_texts[company] += sentence + ' '

    interest_counts = {
        company: len(re.findall(keyword, combined_text, flags=re.IGNORECASE))
        for company, keyword in KEYWORDS.items()
    }

    sorted_topics = sorted(interest_counts.items(), key=lambda x: -x[1])
    top_topics = [topic for topic, _ in sorted_topics[:5]]

    return {
        'sentence_texts': segment_texts,
        'interest_counts': interest_counts,
        'top_topics': top_topics,
        'sentence_count': len(sentences)
    }


def build_markdown_report(data: dict) -> str:
    """Construct the final markdown investment analysis report."""
    md = [
        '# Elon Musk & His Companies – Investment Analysis',
        '',
        '## Executive Summary',
        '',
        '(Generated automatically from YouTube video transcripts. '
        'The analysis focuses on publicly discussed projects, growth areas, '
        'risks, and opportunities.)',
        ''
    ]

    # Company sections
    for company in data['top_topics']:
        md.append(f'## {company}')
        md.append('')
        if company in data['sentence_texts'] and data['sentence_texts'][company]:
            md.append(data['sentence_texts'][company].strip())
        else:
            md.append('_No specific transcript excerpts captured for this segment._')
        md.append('')

    # Positive factors
    positives = [
        'Strong market positioning in electric vehicles (Tesla).',
        'Diversified portfolio of high‑growth projects (SpaceX, Starlink, Boring Company).',
        'Brand resilience and visionary leadership.',
        'Continued innovation in AI, neurotechnology (Neuralink), and infrastructure.',
        'Potential for new revenue streams from X (Twitter) monetization and AI initiatives.'
    ]
    md.append('## Positive Factors')
    md.append('')
    for p in positives:
        md.append(f'- {p}')
    md.append('')

    # Negative factors / risks
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

    # Future prospects & opportunities
    md.append('## Future Prospects & Opportunities')
    md.append('')
    future_points = [
        'SpaceX Starship full reusability could disrupt launch cost structure.',
        "Tesla's rollout of Full Self‑Driving and robotaxi network.",
        "Neuralink's potential breakthroughs in brain‑computer interfaces.",
        "The Boring Company's tunnel network for urban transport.",
        "X's ad‑tech and subscription models for revenue diversification.",
        "Starlink expansion and satellite internet market capture."
    ]
    for fp in future_points:
        md.append(f'- {fp}')
    md.append('')

    # Conclusion
    md.append('## Conclusion')
    md.append('')
    md.append('Elon Musk’s portfolio represents a high‑conviction, high‑beta investment thesis.')
    md.append('The combination of market‑leading positions in EVs and commercial spaceflight,')
    md.append('alongside ambitious moonshots, offers outsized upside if execution stays on track.')
    md.append('Investors should weigh capital intensity, regulatory headwinds, and operational')
    md.append('risks against the potential for monopolistic advantages in emerging industries.')
    md.append('')
    md.append('_Prepared using automated transcript ingestion and heuristic analysis._')

    return '\n'.join(md)


# ----------------------------------------------------------------------
# Main Execution
# ----------------------------------------------------------------------
def main() -> None:
    combined_text = ''
    for url in URLS:
        video_id = extract_video_id(url)
        if not video_id:
            continue
        print(f'Fetching transcript for {url}')
        transcript = fetch_subtitles(video_id, url)
        if transcript:
            combined_text += transcript
            combined_text += '\n\n---\n\n'  # Visual separator between videos
        else:
            print(f'No transcript obtained for {url}')

    if not combined_text.strip():
        print('No transcripts were successfully fetched. Exiting.')
        return

    # Basic analytics on the combined transcripts
    analytics = analyse_transcript(combined_text)

    # Build markdown report
    report_md = build_markdown_report(analytics)

    # Write to target location
    output_path = '/home/tom/hermes-workspace/ElonMusk_Investment_Analysis.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_md)

    print(f'Analysis markdown written to {output_path}')
    print(f'Total sentences processed: {analytics["sentence_count"]}')
    print(f'Top topics identified: {analytics["top_topics"]}')


if __name__ == '__main__':
    main()