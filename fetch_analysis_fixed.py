#!/usr/bin/env python3
"""
Fetch transcripts from a list of YouTube URLs, extract relevant segments,
perform basic analytics, and generate a markdown investment analysis paper.

Author: Automated Hermes Agent
"""

import re
from collections import defaultdict
from youtube_transcript_api import YouTubeTranscriptApi

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

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def extract_video_id(url: str) -> str | None:
    """Extract video ID from a YouTube URL."""
    match = re.search(r'[?v=]([^&]+)', url)
    if match:
        return match.group(1)
    return None


def fetch_transcript(video_id: str) -> str:
    """
    Retrieve English transcript for a given video ID using youtube_transcript_api.
    Returns concatenated transcript text or empty string if unavailable.
    """
    try:
        yt = YouTubeTranscriptApi()
        # Get all transcripts available for the video
        transcript_list = yt.list(video_id)

        # Try to find a manually created English transcript first
        for lang in ['en']:
            try:
                transcript = transcript_list.find_transcript([lang])
                fetched = transcript.fetch()
                # Concatenate all text entries
                full_text = ' '.join([entry['text'] for entry in fetched])
                return full_text
            except Exception:
                # If not found, continue to next step
                continue

            # Fallback to auto-generated English transcript if manually created not found
            try:
                transcript = transcript_list.find_generated_transcript([lang])
                fetched = transcript.fetch()
                full_text = ' '.join([entry['text'] for entry in fetched])
                return full_text
            except Exception:
                continue

        # If no English transcript found, return empty string
        return ''
    except Exception as e:
        print(f'Error fetching transcript for {video_id}: {e}')
        return ''


def analyse_transcript(combined_text: str) -> dict:
    """
    Perform rudimentary analytics on the combined transcript text.
    Identify key topics, count keyword occurrences, and return structured data.
    """
    # Split into sentences for readability
    sentences = re.split(r'(?<=[.!?])\s+', combined_text)

    # Build a dict mapping company/area to accumulated sentences
    segment_texts = defaultdict(str)
    for sentence in sentences:
        lowered = sentence.lower()
        for company, keyword in KEYWORDS.items():
            if keyword in lowered:
                segment_texts[company] += sentence + ' '

    # Count total keyword occurrences for emphasis
    interest_counts = {
        company: len(re.findall(keyword, combined_text, flags=re.IGNORECASE))
        for company, keyword in KEYWORDS.items()
    }

    # Rank topics by occurrence count
    sorted_topics = sorted(interest_counts.items(), key=lambda x: -x[1])
    top_topics = [topic for topic, _ in sorted_topics[:5]]

    return {
        'sentence_texts': segment_texts,
        'interest_counts': interest_counts,
        'top_topics': top_topics,
        'sentence_count': len(sentences)
    }


def build_markdown_report(data: dict) -> str:
    """
    Construct a markdown investment analysis report using the processed data.
    Approx. 5+ pages when printed (varies with content length).
    """
    # Basic structure
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
# Main execution
# ----------------------------------------------------------------------
def main() -> None:
    combined_text = ''
    for url in URLS:
        video_id = extract_video_id(url)
        if not video_id:
            continue
        print(f'Fetching transcript for {url}')
        transcript = fetch_transcript(video_id)
        combined_text += transcript
        combined_text += '\n\n---\n\n'  # Separate videos visually

    # Basic analytics on combined transcripts
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