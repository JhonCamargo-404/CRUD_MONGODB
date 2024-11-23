from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId 

app = Flask(__name__)

client = MongoClient("mongodb+srv://jhonc:rA4s3iE1IdVCV8se@motosdb.oa6sa.mongodb.net/?retryWrites=true&w=majority&appName=motosDB")
db = client['motosDB']
motos_collection = db['motos']

@app.route('/')
def index():
    selected_makes = request.args.getlist('makes')
    query = {}
    if selected_makes:
        query['make'] = {'$in': selected_makes}
    page = int(request.args.get('page', 1))
    motos_per_page = 10
    total_motos = motos_collection.count_documents(query)
    motos = list(motos_collection.find(query).skip((page - 1) * motos_per_page).limit(motos_per_page))
    makes = motos_collection.distinct('make')
    total_pages = (total_motos + motos_per_page - 1) // motos_per_page

    return render_template(
        'index.html',
        motos=motos,
        page=page,
        total_pages=total_pages,
        makes=makes,
        selected_makes=selected_makes
    )

@app.route('/add', methods=['GET', 'POST'])
def add_moto():
    if request.method == 'POST':
        data = request.form.to_dict()
        motos_collection.insert_one(data)
        return redirect(url_for('index'))
    return render_template('add_moto.html')

@app.route('/edit/<object_id>', methods=['GET', 'POST'])
def edit_moto(object_id):
    moto = motos_collection.find_one({"_id": ObjectId(object_id)})
    if request.method == 'POST':
        updates = request.form.to_dict()
        motos_collection.update_one({"_id": ObjectId(object_id)}, {"$set": updates})
        return redirect(url_for('index'))
    return render_template('edit_moto.html', moto=moto)


@app.route('/delete/<object_id>', methods=['GET'])
def delete_moto(object_id):
    try:
        motos_collection.delete_one({"_id": ObjectId(object_id)})
        print(f"Eliminada moto con ObjectID: {object_id}")
    except Exception as e:
        print(f"Error al intentar eliminar la moto: {e}")
    return redirect(url_for('index'))

@app.route('/view/<object_id>', methods=['GET'])
def view_moto(object_id):
    moto = motos_collection.find_one({"_id": ObjectId(object_id)})
    return render_template('view_moto.html', moto=moto)


if __name__ == '__main__':
    app.run(debug=True)
