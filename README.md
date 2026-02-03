# NewsFeed-Django
**PulseWire** is a web-based news dashboard that fetches and displays real-time headlines from **NewsAPI.org**. Users can browse curated desks, filter by region, and search for any topic in a polished, responsive layout that is ready to showcase on GitHub. 🚀

## Highlights
- **Curated desks** for technology, sports, business, science, entertainment, and more.
- **Region filters** to switch between top headlines by country.
- **Search-ready** interface with contextual hero story and latest updates.
- **Modern dashboard UI** designed for quick scanning and storytelling.

## Setup
1. Create a NewsAPI key at https://newsapi.org and export it as an environment variable:
   ```bash
   export NEWS_API_KEY="your_key_here"
   ```
2. Install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run the Django server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

> Tip: if `NEWS_API_KEY` is missing, the UI will still render and show a helpful message.
