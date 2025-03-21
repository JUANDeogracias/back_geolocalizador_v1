from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from database import SessionLocal, UsuarioDB, DispositivoDB, RegistroDB
from models import Usuario, Dispositivo, Registro
from uuid import uuid4
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

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
    nuevo_usuario = UsuarioDB(username=usuario.username, password=usuario.password, email=usuario.email)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@app.get("/api/usuarios/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
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

    nuevo_dispositivo = DispositivoDB(active=dispositivo.active, nombre=dispositivo.nombre, usuario_id=dispositivo.usuario_id)
    db.add(nuevo_dispositivo)
    db.commit()
    db.refresh(nuevo_dispositivo)
    return nuevo_dispositivo

# Obtener dispositivo por id (ahora el id es un entero)
@app.get("/api/dispositivos/{dispositivo_id}", response_model=Dispositivo)
def obtener_dispositivo(dispositivo_id: int, db: Session = Depends(get_db)):
    dispositivo = db.query(DispositivoDB).filter(DispositivoDB.id == dispositivo_id).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return dispositivo

@app.get("/api/registros/dispositivo/{dispositivo_id}", response_model=List[Registro])
def obtener_registros_por_dispositivo(dispositivo_id: int, db: Session = Depends(get_db)):
    # Consultamos los registros filtrados por el dispositivo_id
    registros = db.query(RegistroDB).filter(RegistroDB.dispositivo_id == dispositivo_id).all()

    if not registros:
        raise HTTPException(status_code=404, detail="No se encontraron registros para este dispositivo")

    return registros

@app.get("/api/registros/dispositivo_1/{dispositivo_id}", response_model=List[Registro])
def obtener_registros_por_dispositivo(dispositivo_id: int, db: Session = Depends(get_db)):
    # Consultamos los registros filtrados por el dispositivo_id
    registros = db.query(RegistroDB).filter(RegistroDB.dispositivo_id == dispositivo_id).first()

    if not registros:
        raise HTTPException(status_code=404, detail="No se encontraron registros para este dispositivo")

    return registros

'''--------------------- REGISTROS ---------------------'''

@app.get("/api/registros/", response_model=List[Registro])
def obtener_registros(db: Session = Depends(get_db)):
    return db.query(RegistroDB).all()

@app.post("/api/registros/", response_model=Registro)
def crear_registro(registro: Registro, db: Session = Depends(get_db)):
    dispositivo_existente = db.query(DispositivoDB).filter(DispositivoDB.id == registro.dispositivo_id).first()
    if not dispositivo_existente:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    nuevo_registro = RegistroDB(fecha=registro.fecha, coordenadas=registro.coordenadas, dispositivo_id=registro.dispositivo_id)
    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)
    return nuevo_registro

# Obtener registro por id (ahora el id es un entero)
@app.get("/api/registros/{registro_id}", response_model=Registro)
def obtener_registro(registro_id: int, db: Session = Depends(get_db)):
    registro = db.query(RegistroDB).filter(RegistroDB.id == registro_id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro