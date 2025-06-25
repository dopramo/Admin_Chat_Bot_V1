from flask import Flask, jsonify, request, render_template
import csv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/suggest", methods=["GET"])
def suggest():
    query = request.args.get("q", "").strip().lower()
    menus = []
    exact_match = None
    with open('menus.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            title = row['title'].strip().lower()
            if query == title:
                exact_match = {
                    "title": row['title'],
                    "url": row['url'],
                    "description": row.get('description', '')
                }
                break  # Stop at the first exact match

    if exact_match:
        return jsonify([exact_match])

    # Fallback to partial match if no exact match
    query_words = [w.strip() for w in query.split() if w.strip()]
    with open('menus.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            keywords = [k.strip().lower() for k in row['keywords'].split(',')]
            title = row['title'].lower()
            if any(
                k.startswith(qw) or title.startswith(qw)
                for qw in query_words
                for k in keywords
            ):
                menus.append({
                    "title": row['title'],
                    "url": row['url'],
                    "description": row.get('description', '')
                })
    return jsonify(menus)

if __name__ == "__main__":
    app.run(debug=True)