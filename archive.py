#!/usr/bin/env python3
"""Archive the current index.html as a dated edition in archive/.

Usage: python3 archive.py 2026-03-06

Creates archive/2026-03-06.html with:
- Hardcoded date (not dynamic JS)
- Back chevron to previous day's archive (hidden if it doesn't exist)
- Forward chevron to next day's archive or / if latest
"""
import sys, os, re
from datetime import date, timedelta

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 archive.py YYYY-MM-DD")
        sys.exit(1)

    d = date.fromisoformat(sys.argv[1])
    prev_d = d - timedelta(days=1)
    next_d = d + timedelta(days=1)

    repo = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(repo, 'index.html'), 'r') as f:
        html = f.read()

    # Format the date like the JS does: "Friday, March 6, 2026"
    date_str = d.strftime('%A, %B ') + str(d.day) + ', ' + str(d.year)

    # Replace the date span with hardcoded text
    # Add a forward chevron after the date-text span
    fwd_svg = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>'

    # Check if next day's archive exists; if not, forward goes to /
    next_file = os.path.join(repo, 'archive', f'{next_d.isoformat()}.html')
    if os.path.exists(next_file):
        fwd_href = f'{next_d.isoformat()}.html'
    else:
        fwd_href = '/'

    # Check if prev day's archive exists
    prev_file = os.path.join(repo, 'archive', f'{prev_d.isoformat()}.html')
    prev_style = '' if os.path.exists(prev_file) else ' style="display:none"'

    # Replace chevron href
    html = html.replace(
        'href="#yesterday"',
        f'href="{prev_d.isoformat()}.html"{prev_style}'
    )

    # Add forward chevron after the date-text span
    html = html.replace(
        '<span id="date-text"></span>',
        f'<span id="date-text">{date_str}</span>\n      <a href="{fwd_href}" class="chevron-fwd" aria-label="Next edition">{fwd_svg}</a>'
    )

    # Replace the entire script block with archive-specific JS (no date calc, no chevron fetch)
    archive_script = """<script>
  const btn = document.getElementById('toggle');
  const why = document.getElementById('why');
  btn.addEventListener('click', () => {
    const open = why.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
</script>"""

    html = re.sub(r'<script>.*?</script>', archive_script, html, flags=re.DOTALL)

    # Write archive file
    os.makedirs(os.path.join(repo, 'archive'), exist_ok=True)
    out_path = os.path.join(repo, 'archive', f'{d.isoformat()}.html')
    with open(out_path, 'w') as f:
        f.write(html)

    print(f'Archived: {out_path}')

if __name__ == '__main__':
    main()
