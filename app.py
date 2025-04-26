from flask import Flask, render_template, request, send_file
import os
from mistralai import Mistral

app = Flask(__name__)

api_key_mistral = "aKFEMuDwJOvtphHDDOrh2qbfRP7jEA1L"
SAVE_DIR = "saved"
os.makedirs(SAVE_DIR, exist_ok=True)

def create_documentation(project_desc):
    model = "mistral-large-latest"
    prompt = f"Based on the project description below, create structured markdown documentation...\n{project_desc}"
    
    client = Mistral(api_key=api_key_mistral)
    completion = client.chat.complete(model=model, messages=[{"role": "user", "content": prompt}])
    
    return completion.choices[0].message.content

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        project_desc = request.form["project_desc"]
        documentation = create_documentation(project_desc)
        
        filename = os.path.join(SAVE_DIR, "README.md")
        with open(filename, "w") as f:
            f.write(documentation)

        return render_template("result.html", documentation=documentation)
    return render_template("index.html")

@app.route("/download")
def download():
    filepath = os.path.join(SAVE_DIR, "README.md")
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
