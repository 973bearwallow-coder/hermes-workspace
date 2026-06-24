# Email Organization System
_Created June 13, 2026_

## Process
1. Keep all emails in inbox for 1 day
2. Then sort into folders below
3. Run daily

## Folders & Retention Rules

| Folder | What Goes There | Retention | Special Rules |
|--------|----------------|-----------|---------------|
| Appointments | Meeting invites, scheduling emails | 1 month | Ask Tom before adding to Google Calendar. If yes → add to calendar. If no → keep in file for 1 month then delete. |
| Farm | Tractor Supply, farm-related emails | 1 month | Delete after 1 month |
| Guns | Gun/ammo/optics promotions from companies | 2 weeks | Delete after 2 weeks |
| News | China news, market news, generic news | 1 week | Delete after 1 week |
| Promotions | Amazon, Home Depot, sale hype (not in other folders) | 1 week | Delete after 1 week |
| Tools | New tools from Home Depot, Harbor Freight, etc. | 1 week | Delete after 1 week |

## Implementation
- Charles/OpenClaw bot has inbox email files set up
- Process: read inbox → classify → move to folder → apply retention rules
