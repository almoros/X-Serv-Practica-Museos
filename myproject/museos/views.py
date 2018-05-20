
import datetime
from .models import Museo, Usuario, Fecha, Comentario
from .parser import get_data
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt


# Lista de museos con url.
def lista_museos():
	museos = Museo.objects.all() # Extraigo todos los museos.
	# Genero la lista de museos.
	Lista_Museos = '<ul style="list-style-type: square">' # Listamos con formato cuadrado.

	for i in museos:
		Lista_Museos += i.Nombre
		Lista_Museos += '<li><a href="'  + i.Enlace + '">' + i.Nombre + '</a><br>'
		Lista_Museos += 'Dirección: ' + i.Clase_vial + ' ' + i.Nombre_via + '<br>'
		Lista_Museos += '<li><a href=http://127.0.0.1:8000/museos/'+ str(i.ident) + '>' + 'Más información</a><br>'
		Lista_Museos += "<br>"

	Lista_Museos += "</ul>"

	return(Lista_Museos)


# Lista de museos sin url.
def lista_museos2():
	museos = Museo.objects.all() # Extraigo todos los museos.
	museos_ordenados = museos.order_by("-Num_Comentario")[:5]
	# Genero la lista de museos.
	Lista_Museos2 = ''

	for i in museos_ordenados:

		if i.Num_Comentario != 0:
			Lista_Museos2 += '<li><a href="'  + i.Enlace + '">' + i.Nombre + '</a><br>'
			Lista_Museos2 += 'Dirección: ' + i.Clase_vial + ' ' + i.Nombre_via + '<br>'
			Lista_Museos2 += '<li><a href=http://127.0.0.1:8000/museos/'+ str(i.ident) + '>' + 'Más información</a><br>'
			Lista_Museos2 += "<br>"

	return(Lista_Museos2)


# Formulario para introducir Usuario y Contraseña.
def log ():
	salida = '<br><br><form action="login" method="POST">'
	salida += 'Usuario<br><input type="text" name="Usuario"><br>'
	salida += 'Contraseña<br><input type="password" name="Password">'
	salida += '<br><br><input type="submit" value="Entrar"><br><br>'
	salida += '</form>'

	return (salida)


# Listamos las páginas personales de cada uno de los usuarios, en la cual, guardarán sus selecciones de museos.
def Lista_Usuarios():
	usuarios = User.objects.all()
	Lista_Usuarios = '<H3>Lista de páginas de los usuarios: </H3><br>'

	for i in usuarios:
		Lista_Usuarios += 'Usuario: ' + i.username + '<br>'

		try:
			Lista_Usuarios +=  Usuario.objects.get(Nombre=i.id).Titulo_pagina
		except ObjectDoesNotExist:
			Lista_Usuarios += i.username + '<br>'

		Lista_Usuarios += '<li><a href=http://127.0.0.1:8000/'+ str(i.username) + '>' + 'Selección de museos</a><br><br>'
	Respuesta = Lista_Usuarios

	return(Respuesta)


# Formulario para buscar por nombre la página de usuario concreta.
def form_titulo():
	respuesta = '<br><br><form action="" method="POST">'
	respuesta += 'Nombre de la página <br><input type="text" name="Nombre"><br>'
	respuesta += '<input type="submit" value="Entrar"><br><br>'
	respuesta += '</form>'

	return (respuesta)


# Enlace que meteremos en el navigation de la plantilla en el botón TODOS.
def todos():
	respuesta = '<li><a href="/museos/"' + '>' + 'Todos los museos</a><br>'

	return(respuesta)


# Enlace que meteremos en el navigation de la plantilla en el botón ABOUT.
def red_about():
	respuesta = '<li><a href="/about/"' + '>' + 'About</a><br>'

	return(respuesta)


# Pie de página donde indicamos el enlace en el cual obtenemos los datos a través de un arhivo XML.
# Ocultamos el enlace original por estética de la página web. Lo indexamos con Saber mas...
def footer():
	url = 'https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default'
	pie_pagina = '<html><body><p><p style="text-align:center;">Esta aplicación utiliza datos del portal de datos abiertos de la ciudad de Madrid. © Copyright'\
			   + '</p></p></body></html>' + '<a href="' + url + '"><p style="text-align:center;"> Saber más...</p></a>'

	return pie_pagina


@csrf_exempt


def logearse (request):
	usuario = request.POST['Usuario']
	contraseña = request.POST['Password']
	user = authenticate(username=usuario, password=contraseña)
	result = request.user.is_authenticated()

	if user is not None:
		login(request, user)
		return redirect('/')
	else:
		Log = log()
		Texto = 'Usuario inválido'
		Templates = get_template('error.html')
		# Introducimos las variables deseadas en la plantilla para renderizar.
		c = Context({'Texto': Texto, 'Log': Log})
		renderizado = Templates.render(c)

		return HttpResponse(renderizado)


def mylogout(request):
    logout(request)

    return redirect('/')


def logeado(request):

	if request.user.is_authenticated:
		Respuesta = '<li><a href=http://127.0.0.1:8000/>' + 'Logout</a><br>'
	else:
		Respuesta = log()

	return(Respuesta)


@csrf_exempt


def museos(request):
	pie_pagina = footer() # El footer tiene ke estar en todas las páginas.
	imagen_principal = '<img src="/static/img/prado1.jpg"/>'
	Templates = get_template("fork.html")
	# Formulario para poder filtrar por distritos.
	Formulario = ''

	if request.user.is_authenticated():
		Formulario = "<br><span class='.t-center'><H6> Usuario: " + str(request.user) + ". " + "<a href='/logout'>Logout</a></H6></span>"
		Formulario += '<form action="" method="POST">'
		Formulario += '<br><br><br><br><br><br><H4>Distrito:</H4> <input type="text" name="Distrito">'
		Formulario += '<input type="submit" value="Filtrar">'
		Formulario += "<br>"
		Formulario += "<br>"

	Lista = lista_museos ()

	# Si recibimos POST es que he filtrado por distrito.
	if request.method == "POST":
		Distrito_filtrado = request.POST['Distrito']
		Distrito_filtrado = Distrito_filtrado.upper()

		if Distrito_filtrado == '':
			Lista = ("No ha introducido ningún distrito, vuelva a intentarlo" + "<br>"  + Lista)
		else:
			museos = Museo.objects.all()
			Lista_Filtrada = ""

			for i in museos:

				if Distrito_filtrado == i.Distrito:
					Distrito = i.Distrito
					Lista_Filtrada += '<li>' + i.Nombre + '</li>'
					Lista_Filtrada += '<a href="'  + i.Enlace + '">' + i.Enlace + '</a>'
					Lista_Filtrada += "<br>"
					Lista_Filtrada += "<br>"

			# Si no coincide el distrito introducido con ninguno de los existentes, mostramos el mensaje de error.
			if Lista_Filtrada == '':
				Lista = ("No hay ningún museo en ese distrito o no existe el mismo, introduzca otro." +"<br>" + Lista)
			else:
				Lista = "<br>Lista de museos en " + Distrito + "<br><br> "+ Lista_Filtrada

	# Introducimos las variables deseadas en la plantilla para renderizar.
	c = Context({'Formulario': Formulario, 'Lista': Lista})
	renderizado = Templates.render(c)

	return HttpResponse(renderizado)
	return HttpResponse(Formulario + Lista)


@csrf_exempt


def museos_id(request, recurso):
	Templates = get_template("fork.html")

	try:
		museo = Museo.objects.get(ident=recurso)
		Nombre = museo.Nombre
		Nombre_via = museo.Nombre_via
		Via = museo.Clase_vial
		Numero = museo.Numero
		Localidad = museo.Numero
		Provincia = museo.Provincia
		Cod_Postal = museo.Cod_Postal
		Barrio = museo.Barrio
		Distrito = museo.Distrito
		Coord_X = museo.Coord_X
		Coord_Y = museo.Coord_Y
		Enlace = museo.Enlace
		Descripcion = museo.Descripcion
		Accesibilidad = museo.Accesibilidad
		Telefono = museo.Telefono
		Email = museo.Email

		if Accesibilidad == 1:
			Acces = "Accesible"
		else:
			Acces = "No Accesible"
		Logout=''

		if request.user.is_authenticated():
			Logout = "<span class='.t-center Log'> Usuario: " + str(request.user) + ". " + "<a href='/logout'>Logout</a></span><br>"
		Respuesta = "<p><H4>Esta es la página con la información del museo: </H4>" +'<a href="'  + Enlace + '">' + Nombre + '</a>' + "</br></p>"
		Respuesta += "Descripción: " + Descripcion + "<br>"
		Respuesta += "<br>"
		Respuesta += "Barrio: " + Barrio + "<br>"
		Respuesta += "<br>"
		Respuesta += "Distrito: " + Distrito + "<br>"
		Respuesta += "<br>"
		Respuesta += "Accesibilidad: " + Acces + "<br>"
		Respuesta += "<br>"
		Respuesta += "Telefono: " + Telefono + "<br>"
		Respuesta += "<br>"
		Respuesta += "Email: " + Email + "<br>"
		Formulario = ''

		if request.user.is_authenticated():
			Formulario += '<form action="" method="POST">'
			Formulario += '<br>Comentario: <input type="text" name="Comentario">'
			Formulario += ""
			Formulario += '<input type="submit" value="Comentar">'
			Formulario += "<br>"
			Formulario += "<br>"

		Respuesta += Formulario

		if request.method == "POST":
			comentario = request.POST['Comentario']
			museo = Museo.objects.get(ident=recurso)
			museo.Num_Comentario = museo.Num_Comentario + 1
			museo.save()
			p = Comentario(Museo=museo, Texto=comentario)
			p.save()

		Lista_Comentarios = Comentario.objects.all()
		Respuesta += '<H4>Comentarios realizados sobre el museo: </H4><br>'

		for i in Lista_Comentarios:

			if museo == i.Museo:
				Respuesta += i.Texto
				Respuesta += '<br><br>'

		# Introducimos las variables deseadas en la plantilla para renderizar.
		c = Context({'Formulario': Logout,'Lista': Respuesta})
		renderizado = Templates.render(c)

		return HttpResponse(renderizado)
		return HttpResponse(Respuesta)

	except ObjectDoesNotExist:

		return HttpResponse("No hay coincidencia con ningún museo")


@csrf_exempt


def usuario(request, peticion):
	Templates = get_template("pag_usuario.html")
	Titulo_Pagina = ''

	if request.user.is_authenticated():
		Titulo_Pagina = "<span class='.t-center'> Usuario: " + str(request.user) + ". " + "<a href='/logout'>Logout</a></span>"
		Titulo_Pagina += form_titulo()

	today = datetime.datetime.today()
	user = User.objects.get(username=peticion)

	# Si recibimos POST es que he saleccionado museo.
	if request.method == "POST":
		usuario = User.objects.get(username=peticion)
		key = request.body.decode('utf-8').split('=')[0]

		if key == 'Titulo':
			Titulo = request.POST[key]

			try:
				usuario = Usuario.objects.get(Nombre=user)
				usuario.Titulo_pagina = Titulo
				usuario.Tamano = '15'
				usuario.save()
			except ObjectDoesNotExist:
				p = Usuario(Nombre=user, Titulo_pagina = Titulo, Tamano=15)
				p.save()

		elif key == 'Seleccion':
			nombre_museo = request.POST[key]
			lista_usuario = Fecha.objects.all()

			try:
				museo = Museo.objects.get(Nombre=nombre_museo)
				Encontrado = False

				for i in lista_usuario:

					if str(i.Usuario) == str(peticion): # Si el museo ya se encuentra en seleccionados no lo añado.

						if nombre_museo == i.Museo.Nombre:
							Encontrado = True

				if Encontrado == False: # Por el contrario, si no está dentro de seleccionados, lo añado.
					p = Fecha(Museo=museo, Usuario=usuario, Fecha=today)
					p.save()

			except ObjectDoesNotExist:

				return('')

		elif key == 'Tamano':
			Tamano = request.POST['Tamano']
			Color = request.POST['Color']

			try:
				# Compruebo si exite el usuario.
				username = Usuario.objects.get(Nombre=user)
			except:
				# Si no existe, lo creo.
				p = Usuario(Nombre=user)
				p.save()
				username = Usuario.objects.get(Nombre=user)

			if Tamano == '':
				Tamano = '12'; # Tamaño por defecto con el que sacamos la página de usuario.

			username.Tamano = Tamano
			username.Color = Color
			username.save()

	if request.user.is_authenticated():

		if peticion == str(request.user):
			Templates = get_template('pag_usuario.html')

			try:
				Respuesta = Usuario.objects.get(Nombre=user).Titulo_pagina
			except ObjectDoesNotExist:
				Respuesta = 'Página principal de ' + str(user) + ': Página de ' + str(user) + '<br><br>'

		else:
			Respuesta = 'Página de ' + peticion + '<br>'

	else:
		Respuesta = 'Titulo de página: Pagina de ' + peticion + '<br>'
	Formulario = ''
	# Creo la lista de museos que ha seleccionado el usuario.
	Respuesta += '<br> Museos seleccionados por el Usuario ' + str(user) + '<br>'
	usuario = User.objects.get(username=peticion)
	lista_usuario = Fecha.objects.filter(Usuario=usuario)
	paginator = Paginator(lista_usuario,5)
	pag = request.GET.get('page')

	try:
		museos_selec = paginator.page(pag)
	except PageNotAnInteger:
		museos_selec = paginator.page(1)
	except:
		museos_selec = paginator.page(paginator.num_pages)

	for i in museos_selec:
		Formulario += '<br>'
		Formulario += '<li><a href="'  + i.Museo.Enlace + '">' + i.Museo.Nombre + '</a><br>'
		Formulario += 'Dirección: ' + i.Museo.Clase_vial + ' ' + i.Museo.Nombre_via + '<br>'
		Formulario += 'Fecha: ' + str(i.Fecha) + '<br>'
		Formulario += '<li><a href=http://127.0.0.1:8000/museos/'+ str(i.Museo.ident) + '>' + 'Más información</a><br>'

	Respuesta += Formulario + '<br><br>'

	# Creo la lista de todos los museos que se pueden seleccionar para incluir en la lista de usuario.
	Respuesta2=''

	if request.user.is_authenticated():

		if str(request.user) == str(peticion):
			Respuesta2 = '<br><br><form action="" method="POST">'
			Respuesta2 += 'Modifica tamaño de letra <br><input type="text" name="Tamano"><br><br>'
			Respuesta2 += 'Modifica color de letra <br><input type="color" name="Color"><br><br>'
			Respuesta2 += '<input type="submit" value="Modificar"><br><br><br>'
			Respuesta2 += '</form>'
			Respuesta2 += '<H2>Lista de museos</H2><br>'

	museos = Museo.objects.all()

	Lista_Museos = ''
	Boton = ''

	for i in museos:
		Respuesta2 += '<li type="square">' + i.Nombre + '</li>'
		Respuesta2 += "<br>"

		if request.user.is_authenticated():

			if str(request.user) == str(peticion):
				Respuesta2 += '<form action="" method="POST">'
				Respuesta2 += '<button type="submit" name="Seleccion" value="' + i.Nombre + '">Seleccionar</button><br>'
				Respuesta2 += "<br>"
		else:
			Respuesta2 += '<br>'
	# Introducimos las variables deseadas en la plantilla para renderizar.
	c = Context({'Lista': Respuesta, 'museos_selec': museos_selec, 'Lista2': Respuesta2, 'Titulo_Pagina': Titulo_Pagina})
	renderizado = Templates.render(c) # Renderizamos.

	return HttpResponse(renderizado)


def Cambio (request):
	# Si el usuario está logueado extraigo el tamaño y el color de sus variables.
	if request.user.is_authenticated():
		user = User.objects.get(username=request.user)
		usuario = Usuario.objects.get(Nombre=user)
		Tamano = str(usuario.Tamano) + 'px'
		Color = usuario.Color
	# Si no es así, pongo un tamaño y un color por defecto.
	else:
		Tamano = '13px'
		Color = '#613A17'

	css = get_template('usuario.css')
	# Introducimos las variables deseadas en la plantilla para renderizar.
	c = Context({'Tamano': Tamano, 'Color': Color})
	renderizado = css.render(c)

	return HttpResponse(renderizado,content_type='text/css')


@csrf_exempt


def pag_ppal (request):
	Listado = Museo.objects.all()

	if len(Listado) == 0:
		get_data()

	if request.user.is_authenticated():
		Log = 'Página de ' + str(request.user) + '<br>'
		Log += "<span class='.t-center'> Usuario: " + str(request.user) + ". " + "<a href='/logout'>Logout</a></span>"
	else:
		Log = log()

	pie_pagina = footer() # El footer tiene ke estar en todas las páginas.
	imagen_principal = '<img src="/static/img/prado1.jpg"/>'
	Templates = get_template("index.html")
	# Extraigo todos los museos.
	Lista = lista_museos2()
	Respuesta = Log + Lista
	Todos = todos()
	About = red_about()
	# Solo cogemos las páginas de los usuarios.
	Usuarios = Lista_Usuarios()
	Respuesta = Log + Lista + Usuarios

	# Botón para los museos accesibles.
	Boton = '<br><form action="" method="POST">'
	Boton += '<button type="submit" name="Accesibles" value= "Accesibles">Accesibles</button><br>'
	Boton += "<br>"

	Lista_Accesibles = ''

	if request.method == "POST":
		key = request.body.decode('utf-8').split('=')[0]
		value = request.body.decode('utf-8').split('=')[1]

		if key == 'Accesibles':
			Respuesta = Log + Usuarios + '<br>'
			museos_accesibles = Museo.objects.filter(Accesibilidad=1) # Listamos los que son accesibles.

			if value == 'No':
				Lista_Accesibles += Lista
				Boton = '<br><form action="" method="POST">'
				Boton += '<button type="submit" name="Accesibles" value= "Accesibles">Accesibles</button><br>'
				Boton += "<br>"
			else:
				Boton = '<br><form action="" method="POST">'
				Boton += '<button type="submit" name="Accesibles" value= "No">Más comentados</button><br>'
				Boton += "<br>"
				# Borramos la lista para rehacerla con los accesibles.
				Lista = 'Listado de los museos accesibles: '

				for i in museos_accesibles:
					Lista += '<li><a href="'  + i.Enlace + '">' + i.Nombre + '</a><br>'
					Lista += 'Dirección: ' + i.Clase_vial + ' ' + i.Nombre_via + '<br>'
					Lista += '<li><a href=http://127.0.0.1:8000/museos/'+ str(i.ident) + '>' + 'Más información</a><br>'
					Lista += "<br>"

		elif key == 'Todos':
			redirect(museos)

	Respuesta += Lista_Accesibles + Boton
	Respuesta += Todos
	Respuesta += About
	# Introducimos las variables deseadas en la plantilla para renderizar.
	c = Context({'Log': Log, 'Lista': Lista, 'Usuarios': Usuarios,"Boton":Boton, 'footer': pie_pagina})
	renderizado = Templates.render(c)
	return HttpResponse(renderizado) # Renderizamos.

	return HttpResponse(Respuesta)


def about(request):
	pie_pagina = footer() # El footer tiene ke estar en todas las páginas.
	Templates = get_template("about.html")
	cuerpo =  u'<span><H4>Práctica realizada por Javier Almorós Fernandez.</H4></span>'
	cuerpo += u'<span><H5>Grado en Ingeniería de Sistemas de Telecomunicación.</H5></span><br>'
	cuerpo += u'<span><FONT FACE="verdana">FUNCIONALIDAD:</FONT></span>'
	cuerpo += '<br><ul style="list-style-type: circle">'
	cuerpo += u'<li><H6>El enlace http://127.0.0.1:8000/ es la página principal de sitio web. Nos muestra los museos con mayor número de comentarios en orden descendente además de una lista con las paginas personales de los usuarios logueados. Tiene incluida el formulario para hacer login y los botones "TODOS", "ABOUT" y "ACCESIBLES" que se especifican en la práctica.</H6></li>'
	cuerpo += u'<li><H6>El enlace http://127.0.0.1:8000/usuario_x muestra la pagina personal del usuario_x,los museos seleccionados por él y la lista de los museos seleccionables. Además se muestra un formulario para cambiar tanto el título de la página en cuestión como para modificar el tamaño y el color de la letra de la página.</H6></li>'
	cuerpo += '<li><H6>El enlace http://127.0.0.1:8000/museos muestra una lista de todos los museos de Madrid. Además añadimos un formulario que nos permite filtrar museos por el distrito en el que se encuentran.</H6></li>'
	cuerpo += u'<li><H6>El enlace http://127.0.0.1:8000/museos/id muestra la página de información del museo_x, donde podemos consultar tanto el distrito como barrio en el que se encuentra, su teléfono, su e-mail y una descripción del mismo. Además podemos tanto ver como agregar comentarios al museo a través de esta interfaz.</H6></li>'
	cuerpo += u'<li><H6>Como funcionalidades opcionales se ha implementado la inclusión de un favicon del sitio web y añadir números de páginas según cuántos museos seleccionados haya en /usuario_x para que su lectura resulte más cómoda.</H6></li>'
	cuerpo += u'<li><H6>He decidido incluir el enlace "Saber mas..." que nos lleva a la página de donde recogemos el XML de la Comunidad de Madrid en el footer de ese modo y no el enlace original por cuidar la estética de la página.</H6></li></ul>'
	# Introducimos las variables deseadas en la plantilla para renderizar.
	c = Context({'cuerpo': cuerpo, 'footer': pie_pagina})
	renderizado = Templates.render(c) # Renderizamos.

	return HttpResponse(renderizado)


def XML (request,peticion):

	user = User.objects.get(username=peticion)
	try:
		usuario = Usuario.objects.get(Nombre=user)
		lista_usuario = Fecha.objects.filter(Usuario=usuario.Nombre)
		xml = "<?xml version='1.0' encoding='UTF-8' ?>"
		xml += "<data><usuario name='" + str(request.user) +"'>"
		for i in lista_usuario:
			museo = i.Museo
			xml += '<nombre name="' + museo.Nombre + '">'
			xml += '<address>' + museo.Clase_vial + ' ' + museo.Nombre_via + ' ' + str(museo.Numero) + '</address>'
			xml += '<Localidad>' + museo.Localidad + '</Localidad>'
			xml += '<Provincia>' + museo.Provincia + '</Provincia>'
			xml += '<Codigo-Postal>' + str(museo.Cod_Postal) + '</Codigo-Postal>'
			xml += '<Barrio>' + museo.Barrio + '</Barrio>'
			xml += '<Distrito>' + museo.Distrito + '</Distrito>'
			xml += '<CoordX>' + str(museo.Coord_X) + '</CoordX>'
			xml += '<CoordY>' + str(museo.Coord_Y) + '</CoordY>'
			xml += '<Descripccion>' + museo.Descripcion + '</Descripccion>'
			xml += '<Accesibilidad>' + str(museo.Accesibilidad) + '</Accesibilidad>'
			xml += '</nombre>'
		xml += '</usuario></data>'
	except ObjectDoesNotExist:
		print('')
	return HttpResponse(xml, content_type="text/xml")
