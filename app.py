from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Setting database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    harga = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {"id": self.id, "nama": self.nama, "harga": self.harga, "created_at": self.created_at}


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method =='GET':
        data_menu = Menu.query.all()
        return {'menu': [menu.to_dict() for menu in data_menu]}

    if request.method == 'POST':
        data = request.json
        new_menu = Menu(nama=data['nama'], harga=data['harga'], created_at=datetime.now())
        db.session.add(new_menu)
        db.session.commit()
        return {'message': 'Menu berhasil ditambahkan'}
    
    return {'message': 'Method tidak diizinkan'}, 405   

    
@app.route('/menu/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def menu_id(id):
    if request.method == 'GET':
        data_menu = Menu.query.filter_by(id=id).first()
        if data_menu:
            return data_menu.to_dict()
        return {'message': 'Menu tidak ditemukan'}, 404
    
    if request.method == 'PUT':
        data = request.json
        menu = Menu.query.filter_by(id=id).first()
        if menu:
            menu.nama = data['nama']
            menu.harga = data['harga']
            db.session.commit()
            return {'message': 'Menu berhasil diubah'}
        return {'message': 'Menu tidak ditemukan'}, 404
    
    if request.method == 'PATCH':
        data = request.json
        menu = Menu.query.filter_by(id=id).first()
        if menu:
            if 'nama' in data:
                menu.nama = data['nama']
            if 'harga' in data:
                menu.harga = data['harga']
            db.session.commit()
            return {'message': 'Menu berhasil diubah'}
        return {'message': 'Menu tidak ditemukan'}, 404

    if request.method == 'DELETE':
        menu = Menu.query.filter_by(id=id).first()
        if menu:
            db.session.delete(menu)
            db.session.commit()
            return {'message': 'Menu berhasil dihapus'}
        return {'message': 'Menu tidak ditemukan'}, 404
    

    
    return {'message': 'Method tidak diizinkan'}, 405


if __name__ == '__main__':
    import os
    os.environ['FLASK_ENV'] = 'development'
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8001, debug=True)