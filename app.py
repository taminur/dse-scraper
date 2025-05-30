from flask import Flask, jsonify, send_file
import os
from scraper import collect_from_dsebd

app = Flask(__name__)

DATA_CSV = "latest_stock_data.csv"

@app.route("/scrape", methods=["GET"])
def scrape():
    try:
        df = collect_from_dsebd()
        # Save as CSV for download route
        df.to_csv(DATA_CSV, index=False)
        return jsonify({"success": True, "rows": len(df), "columns": list(df.columns), "data":df.to_json()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/download", methods=["GET"])
def download():
    if not os.path.exists(DATA_CSV):
        return jsonify({"success": False, "error": "No CSV file found. Please run /scrape first."})
    return send_file(DATA_CSV, as_attachment=True)

@app.route("/")
def home():
    return "<h3>DSE Scraper API</h3><ul><li><a href='/scrape'>/scrape</a> - fetch live data</li><li><a href='/download'>/download</a> - download CSV</li></ul>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT env variable
    app.run(host="0.0.0.0", port=port)