from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OPENLIB = "https://openlibrary.org/search.json"


def fetch_books(query, limit=10):
    if not query:
        return []

    try:
        r = requests.get(OPENLIB, params={"q": query}, timeout=10)
        docs = r.json().get("docs", [])[:limit]

        books = []

        for item in docs:

            # -------------------------
            # SAFE ISBN HANDLING
            # -------------------------
            isbn_list = item.get("isbn", [])
            isbn = isbn_list[0] if isbn_list else None

            # -------------------------
            # COVER LOGIC (UPDATED)
            # -------------------------
            cover_i = item.get("cover_i")

            if cover_i:
                cover = f"https://covers.openlibrary.org/b/id/{cover_i}-M.jpg"
            elif isbn:
                cover = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
            else:
                cover = "https://via.placeholder.com/180x260?text=No+Cover"

            # -------------------------
            # BOOK OBJECT (UNCHANGED STRUCTURE)
            # -------------------------
            books.append({
                "title": item.get("title", "No Title"),
                "author": item.get("author_name", ["Unknown"])[0] if item.get("author_name") else "Unknown",
                "year": item.get("first_publish_year", "N/A"),
                "isbn": isbn or "Not Available",
                "cover": cover
            })

        return books

    except:
        return []


# -------------------------
# HOME PAGE (UNCHANGED)
# -------------------------
@app.route("/")
def home():
    return render_template("catalog.html")


# -------------------------
# SEARCH API (UNCHANGED)
# -------------------------
@app.route("/search")
def search():
    q = request.args.get("q", "")
    return jsonify(fetch_books(q))


if __name__ == "__main__":
    app.run(debug=True)
