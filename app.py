from flask import Flask, jsonify, send_file, request, abort, Response, render_template, after_this_request
import os
from scraper import collect_from_dsebd
from datetime import datetime
import io

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")

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

@app.route("/download")
def download():
    df = collect_from_dsebd()
    # Create an in-memory buffer
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    # Dynamically generate filename
    filename = datetime.now().strftime("stocks_%Y%m%d%H%M.csv")


    @after_this_request
    def cleanup(response):
        buffer.close()
        return response

    # Send the buffer as a downloadable file
    return send_file(
        io.BytesIO(buffer.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename  # works in Flask 2.0+
    )

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT env variable
    app.run(host="0.0.0.0", port=port, debug=True)