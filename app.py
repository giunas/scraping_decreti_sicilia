from flask import Flask, render_template, request, send_file
from scraping import scrape_sicilia

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/scrape", methods=["POST"])
def scrape():
    inizio = request.form["inizio"]
    fine = request.form["fine"]
    csv_path = scrape_sicilia(inizio, fine)
    return send_file(csv_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
