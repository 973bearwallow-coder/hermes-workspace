#!/usr/bin/env python3
"""
Find meeting links from Google Calendar events.
Searches for events with 'coaching', 'meet', 'call', or 'boardroom' in the title
within the next N hours. Returns the first Google Meet link found.

Usage:
    python3 find_meeting_link.py [--hours 24] [--keyword coaching]
"""

import json
import subprocess
import sys
import argparse
from datetime import datetime, timedelta
from shlex import quote as shell_quote

GAPI = "/home/tom/.hermes/skills/productivity/google-workspace/scripts/google_api.py"

def find_meeting_link(hours_ahead=24, keyword="coaching"):
    """Search calendar for upcoming events with meeting links."""
    now = datetime.now()
    start = now
    end = now + timedelta(hours=hours_ahead)
    
    start_iso = start.isoformat(timespec='seconds') + '-04:00'
    end_iso = end.isoformat(timespec='seconds') + '-04:00'
    
    cmd = f'{GAPI} calendar list --start {shell_quote(start_iso)} --end {shell_quote(end_iso)}'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Calendar API error: {result.stderr}", file=sys.stderr)
        return None
    
    events = json.loads(result.stdout)
    
    # Search for events matching keyword
    keyword_lower = keyword.lower()
    for event in events:
        summary = event.get('summary', '').lower()
        if keyword_lower not in summary:
            continue
        
        event_time = event.get('start', '')
        title = event.get('summary', 'Unknown')
        
        # Check location field for Meet URL
        location = event.get('location', '')
        if 'meet.google.com' in location:
            print(f"Found: {title} at {event_time}")
            print(f"Meet link: {location}")
            return location
        
        # Check conferenceData for Meet links
        conference_data = event.get('conferenceData', {})
        if conference_data:
            entry_points = conference_data.get('entryPoints', [])
            for ep in entry_points:
                uri = ep.get('uri', '')
                if 'meet.google.com' in uri:
                    print(f"Found: {title} at {event_time}")
                    print(f"Meet link: {uri}")
                    return uri
    
    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find meeting links from Google Calendar')
    parser.add_argument('--hours', type=int, default=24, help='Hours ahead to search')
    parser.add_argument('--keyword', default='coaching', help='Keyword to search in event title')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    link = find_meeting_link(args.hours, args.keyword)
    
    if link:
        if args.json:
            print(json.dumps({"meet_link": link}))
        else:
            print(link)
        sys.exit(0)
    else:
        print("No meeting link found", file=sys.stderr)
        sys.exit(1)
