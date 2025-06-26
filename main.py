from flask import Flask, render_template, request, send_file
import os, csv
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    internal_file = request.files['internal_file']
    provider_file = request.files['provider_file']

    internal_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(internal_file.filename))
    provider_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(provider_file.filename))

    internal_file.save(internal_path)
    provider_file.save(provider_path)

    with open(internal_path, 'r') as f1, open(provider_path, 'r') as f2:
        internal_reader = list(csv.DictReader(f1))
        provider_reader = list(csv.DictReader(f2))

    internal_refs = {row['transaction_reference']: row for row in internal_reader}
    provider_refs = {row['transaction_reference']: row for row in provider_reader}

    matched, internal_only, provider_only = [], [], []

    for ref, int_txn in internal_refs.items():
        if ref in provider_refs:
            prov_txn = provider_refs[ref]
            if int_txn['amount'] == prov_txn['amount'] and int_txn['status'] == prov_txn['status']:
                matched.append(int_txn)
            else:
                mismatch = int_txn.copy()
                mismatch['provider_amount'] = prov_txn['amount']
                mismatch['provider_status'] = prov_txn['status']
                matched.append(mismatch)
        else:
            internal_only.append(int_txn)

    for ref, prov_txn in provider_refs.items():
        if ref not in internal_refs:
            provider_only.append(prov_txn)

    save_to_csv('matched.csv', matched)
    save_to_csv('internal_only.csv', internal_only)
    save_to_csv('provider_only.csv', provider_only)

    return render_template("index.html", matched=matched, internal_only=internal_only, provider_only=provider_only)

@app.route('/download/<category>')
def download_csv(category):
    file_map = {
        'matched': 'matched.csv',
        'internal': 'internal_only.csv',
        'provider': 'provider_only.csv'
    }
    if category in file_map:
        return send_file(file_map[category], as_attachment=True)
    return 'File not found', 404

def save_to_csv(filename, data):
    if not data:
        return
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
