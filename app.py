from flask import Flask, jsonify, send_file, request, abort, Response
import os
from scraper import collect_from_dsebd

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY", "oLRg35Z-0i2wX5-nEN9hw7xd0WIdap_S6ZvuVQZPoaw")

def require_api_key():
    key = request.args.get("key") or request.headers.get("x-api-key")
    if key != API_KEY:
        abort(401, description="Unauthorized: Invalid or missing API key")

@app.route("/scrape", methods=["POST"])
def scrape():
    require_api_key()
    fmt = request.json.get("format", "json")  # default = json

    try:
        df = collect_from_dsebd()
        
        if fmt == "csv":
            csv_data = df.to_csv(index=False)
            return Response(
                csv_data,
                mimetype="text/csv",
            )
        else:
            print('json will be returned')
            json_data = df.to_json(orient="records")
            return Response(
                json_data,
                mimetype="application/json",
            )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/download", methods=["POST"])
def download():
    require_api_key()
    df = collect_from_dsebd()
    data_csv = df.to_csv(index=False)
    return send_file(data_csv, as_attachment=True)

@app.route("/")
def home():
    return ("<h3>DSE Scraper API</h3>"
            )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT env variable
    app.run(host="0.0.0.0", port=port)