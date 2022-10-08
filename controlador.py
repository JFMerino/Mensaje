import sqlite3

def validarUsuario(usuario, password):
    db=sqlite3.connect("mensajeria.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta = "select *from Usuarios where correo='"+usuario+"'and password='"+password+"'"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado

def listaDestinatarios(usuario):
    db=sqlite3.connect("mensajeria.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta = "select *from Usuarios where correo<>'"+usuario+"'"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado

def registrarUsuario(nombre,email, password,codigo):
    try:
        db=sqlite3.connect("mensajeria.s3db")
        db.row_factory=sqlite3.Row
        cursor=db.cursor()
        consulta="insert into usuarios (nombreusuario,correo, password, estado, codigoactivacion) values ('"+nombre+"','"+email+"','"+password+"','0','"+codigo+"')"
        cursor.execute(consulta)
        db.commit()
        return "Usuario Registrado"
    except:
        return "Por favor verifique el correo y o el nombre de usuario ya que estos ya existen"

def activarUsuario(codigo):
    db=sqlite3.connect("mensajeria.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="update Usuarios set estado='1' where codigoactivacion='"+codigo+"'"
    cursor.execute(consulta)
    db.commit()
    consulta2 = "select *from Usuarios where codigoactivacion='"+codigo+"' and estado='1'"
    cursor.execute(consulta2)
    resultado=cursor.fetchall()
    return resultado

def registrarMail(origen,destino,asunto,mensaje):
    db=sqlite3.connect("mensajeria.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="insert into mensajeria (asunto,mensaje,fecha,hora,id_usu_envia,id_usu_recibe,estado) values ('"+asunto+"','"+mensaje+"',DATE('now'),TIME('now'),'"+origen+"','"+destino+"','0')"
    cursor.execute(consulta)
    db.commit()
    return "1"

def verEnviados(correo):
    db=sqlite3.connect("mensajeria.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta = "select m.asunto, m.mensaje, m.fecha, m.hora, u.nombreusuario from Usuarios u, Mensajeria m where u.correo=m.id_usu_recibe and m.id_usu_envia='"+correo+"' order by fecha desc, hora desc"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado

def verRecibidos(correo):
    db=sqlite3.connect("mensajeria.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta = "select m.asunto, m.mensaje, m.fecha, m.hora, u.nombreusuario from Usuarios u, Mensajeria m where u.correo=m.id_usu_envia and m.id_usu_recibe='"+correo+"' order by fecha desc, hora desc"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado

def actualizarContraseña(passnew, correo):
    db=sqlite3.connect("mensajeria.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="update Usuarios set password='"+passnew+"' where correo='"+correo+"'"
    cursor.execute(consulta)
    db.commit()
    resultado=cursor.fetchall()
    return resultado
