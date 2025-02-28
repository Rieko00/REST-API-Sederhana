from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Setting database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telp = db.Column(db.String(15), nullable=False)
    alamat = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "email": self.email,
            "telp": self.telp,
            "alamat": self.alamat,
            "created_at": self.created_at
        }

@app.route('/docs')
def docs():
    return render_template('docs.html')

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        data_users = Users.query.all()
        return {'users': [user.to_dict() for user in data_users]}

    if request.method == 'POST':
        data = request.json
        new_user = Users(nama=data['nama'], email=data['email'], telp=data['telp'], alamat=data['alamat'], created_at=datetime.now())
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User berhasil ditambahkan'}

    return {'message': 'Method tidak diizinkan'}, 405

@app.route('/users/<id>', methods=['GET', 'DELETE'])
def users_id(id):
    if request.method == 'GET':
        data_user = Users.query.filter_by(id=id).first()
        if data_user:
            return data_user.to_dict()
        return {'message': 'User tidak ditemukan'}, 404

    if request.method == 'DELETE':
        user = Users.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User berhasil dihapus'}
        return {'message': 'User tidak ditemukan'}, 404

    return {'message': 'Method tidak diizinkan'}, 405


if __name__ == '__main__':
    import os
    os.environ['FLASK_ENV'] = 'development'
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8001, debug=True)