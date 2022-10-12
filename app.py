from flask import Flask, render_template, request
import hashlib
import controlador
from datetime import datetime
import envioemail

app = Flask(__name__)

email_origen=""

@app.route("/")
def inicio():
    return render_template("login.html")

@app.route("/VerificarUsuario",methods=["GET","POST"])
def VerificarUsuario():
    if request.method=="POST":
        user=request.form["txtusuario"]
        user=user.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        passw = request.form["txtpass"]
        passw = passw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        passw2 = passw.encode()
        passw2 =hashlib.sha384(passw2).hexdigest()

        global email_origen

        respuesta = controlador.validarUsuario(user, passw2)
        if len(respuesta)==0:
            email_origen=""
            mensaje= "ERROR DE AUTENTICACION.!!!! por favor verifique el correo y la contraseña"
            return render_template("informacion.html",data=mensaje)
            
        else:
            email_origen=user
            respuesta2=controlador.listaDestinatarios(user)
            return render_template("principal.html",data=respuesta2)

@app.route("/RegistrarUsuario",methods=["GET","POST"])
def RegistrarUsuario():
    if request.method=="POST":
        name=request.form["txtnombre"]
        name=name.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        email=request.form["txtusuarioregistro"]
        email=email.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        passw = request.form["txtpassregistro"]
        passw=passw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        passw2 = passw.encode()
        passw2 =hashlib.sha384(passw2).hexdigest()

        code = datetime.now()
        codigo2=str(code)
        codigo2 = codigo2.replace("-","")
        codigo2 = codigo2.replace(" ","")
        codigo2 = codigo2.replace(":","")
        codigo2 = codigo2.replace(".","")
        codigo = codigo2.encode()
        codigo = hashlib.sha224(codigo).hexdigest()
        respuesta = controlador.registrarUsuario(name,email,passw2,codigo)
        mensajeEmail = "Sr(a) "+name+", su codigo de activacion es :\n\n"+codigo+"\n\n"
        asunto = "Codigo de activacion"
        envioemail.enviar(email,asunto,mensajeEmail)
        #mensaje= "El usuario "+name+", se ha registrado satisfactoriamente"
        return render_template("informacion.html",data=respuesta)


@app.route("/enviarMail",methods=["GET","POST"])
def enviarMail():
    if request.method=="POST":
        asunto=request.form["asunto"]
        asunto=asunto.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        destino=request.form["destino"]
        destino=destino.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        mensaje=request.form["mensaje"]
        mensaje=mensaje.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        
        controlador.registrarMail(email_origen,destino,asunto,mensaje)
        
        asunto2="Mensaje Nuevo"
        mensaje2="Sr usuario usted recibio un nuevo mensaje.\n\n Recuerde ingresar a la plataforma para visualizar el mensaje en el historial."
        envioemail.enviar(destino,asunto2,mensaje2) 
        
        return "Email Enviado Satisfactoriamente" 

@app.route("/historialEnviados",methods=["GET","POST"])
def historialEnviados():
    if request.method=="POST":
        resultado = controlador.verEnviados(email_origen)
        return render_template("respuesta.html",data=resultado)

@app.route("/historialRecibido",methods=["GET","POST"])
def historialRecibido():
    if request.method=="POST":
        resultado = controlador.verRecibidos(email_origen)
        return render_template("respuesta.html",data=resultado)

@app.route("/activarUsuario",methods=["GET","POST"])
def activarUsuario():
    if request.method=="POST":
        codigo=request.form["txtcodigo"]
        codigo=codigo.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        
        respuesta=controlador.activarUsuario(codigo)

        if len(respuesta)==0:
            mensaje = "El codigo de activacion es invalido"
        else:
            mensaje = "El usuario fue activado exitosamente"

        return render_template("informacion.html",data=mensaje)


@app.route("/actualizarP",methods=["GET","POST"])
def actualizarP():
    if request.method=="POST":
        passw=request.form["pass"]
        passw=passw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        passw2 = passw.encode()
        passw2 =hashlib.sha384(passw2).hexdigest()
        
        controlador.actualizarContraseña(passw2,email_origen)
        return "Contraseña actualizada correctamente"

@app.route("/olvideContraseña",methods=["GET","POST"])
def olvideContraseña():
    if request.method=="POST":
        correo = request.form["txtcorreo"]
        correo=correo.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        code = datetime.now()
        codigo2=str(code)
        codigo2 = codigo2.replace("-","")
        codigo2 = codigo2.replace(" ","")
        codigo2 = codigo2.replace(":","")
        codigo2 = codigo2.replace(".","")
        codigo = codigo2.encode()
        codigo = hashlib.sha384(codigo).hexdigest()
        respuesta = controlador.olvideContraseña(correo)
        if len(respuesta)==0:
            return render_template("informacion.html",data="El correo electronico no existe, por favor verifiquelo e intente nuevamente")
        else:
            controlador.actualizarContraseña(codigo,correo)
            mensajeEmail = "Su nueva contraseña temporal es:\n\n"+codigo2+"\n\n"
            asunto = "Nueva contraseña"
            envioemail.enviar(correo,asunto,mensajeEmail)
            return render_template("informacion.html",data=respuesta)