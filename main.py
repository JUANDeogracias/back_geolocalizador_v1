from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, UsuarioDB, DispositivoDB, RegistroDB
from models import Usuario, Dispositivo, Registro
from uuid import uuid4
from typing import List

app = FastAPI()

# Dependencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''--------------------- USUARIOS ---------------------'''

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/api/usuarios/", response_model=List[Usuario])
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(UsuarioDB).all()

@app.post("/api/usuarios/", response_model=Usuario)
def crear_usuario(usuario: Usuario, db: Session = Depends(get_db)):
    nuevo_usuario = UsuarioDB(id=str(uuid4()), username=usuario.username, password=usuario.password, email=usuario.email)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@app.get("/api/usuarios/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: str, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.delete("/api/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: str, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado"}

'''--------------------- DISPOSITIVOS ---------------------'''

@app.get("/api/dispositivos/", response_model=List[Dispositivo])
def obtener_dispositivos(db: Session = Depends(get_db)):
    return db.query(DispositivoDB).all()

@app.post("/api/dispositivos/", response_model=Dispositivo)
def crear_dispositivo(dispositivo: Dispositivo, db: Session = Depends(get_db)):
    usuario_existente = db.query(UsuarioDB).filter(UsuarioDB.id == dispositivo.usuario_id).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    nuevo_dispositivo = DispositivoDB(id=str(uuid4()), active=dispositivo.active, usuario_id=dispositivo.usuario_id)
    db.add(nuevo_dispositivo)
    db.commit()
    db.refresh(nuevo_dispositivo)
    return nuevo_dispositivo

@app.get("/api/dispositivos/{dispositivo_id}", response_model=Dispositivo)
def obtener_dispositivo(dispositivo_id: str, db: Session = Depends(get_db)):
    dispositivo = db.query(DispositivoDB).filter(DispositivoDB.id == dispositivo_id).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return dispositivo

'''--------------------- REGISTROS ---------------------'''

@app.get("/api/registros/", response_model=List[Registro])
def obtener_registros(db: Session = Depends(get_db)):
    return db.query(RegistroDB).all()

@app.post("/api/registros/", response_model=Registro)
def crear_registro(registro: Registro, db: Session = Depends(get_db)):
    dispositivo_existente = db.query(DispositivoDB).filter(DispositivoDB.id == registro.dispositivo_id).first()
    if not dispositivo_existente:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    nuevo_registro = RegistroDB(id=str(uuid4()), fecha=registro.fecha, coordenadas=registro.coordenadas, dispositivo_id=registro.dispositivo_id)
    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)
    return nuevo_registro

@app.get("/api/registros/{registro_id}", response_model=Registro)
def obtener_registro(registro_id: str, db: Session = Depends(get_db)):
    registro = db.query(RegistroDB).filter(RegistroDB.id == registro_id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro