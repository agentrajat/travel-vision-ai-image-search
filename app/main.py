from flask import Flask, request, jsonify, render_template
from ir_system import IRSystem

DATA_PATH = "./outputs/search-data.json"
IMG_DIR = "./images/"
INDEX_FILE = "./index-data.pkl"

app = Flask(__name__)
ir_system = None

def response(data):
    res = jsonify(data)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/initialize', methods=['GET'])
def initialize():
    global ir_system
    if ir_system is None:
        ir_system = IRSystem(search_data=DATA_PATH, image_dir=IMG_DIR, object_path=INDEX_FILE)
        status = "system initialized"
    else:
        status = "system already initialized"
    return response({'status': status})

@app.route('/search/<model>', methods=['GET'])
def search(model):
    query = request.args.get('q')
    return response(ir_system.search(query, model))

# @app.route('/documents', methods=['GET'])
# def fetch_documents():
#     docnos = request.args.get('docno')
#     docnos = docnos.split(',') if docnos else []
#     return response(ir_system.get_documents(docnos))

if __name__ == '__main__':
    app.run()