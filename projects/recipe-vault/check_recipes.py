import json
import os

# Read the index
with open(os.path.expanduser('~/hermes-workspace/projects/recipe-vault/index.json'), 'r') as f:
    index = json.load(f)

# Get all urls
all_urls = [(r['name'], r['url'], r['file']) for r in index['recipes']]

# Print all for checking
for i, (name, url, file) in enumerate(all_urls):
    print(f"{i+1}. {name}")
    print(f"   {url}")
