from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from .models import Circunscripcion, Mesa, Resultado, Partido
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from .forms import MesaForm
# Create your views here.

#no se usa esa view
def newUser(request):
	if request.method == 'POST':
		form=UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			usuario = User.objects.get(username=form.cleaned_data['username'])
			user = UserProfile(usuario=usuario)
			user.save()
			return render(request, 'gracias.html', {'usuario': usuario})
	else:
		#si el method es GET, instanciamos un objeto RegistroUsuario vacio
		form=UserCreationForm()
	# Y mostramos los datos
	return render(request, 'registro.html', {'form':form})

def acceso(request):
	if  request.user.is_authenticated():
		return redirect('index')
	mensaje=''
	if request.method == 'POST':
		form = AuthenticationForm(request.POST)
		if form.is_valid:
			usuario = request.POST['username']
			password=request.POST['password']
			acceso=authenticate(username=usuario, password=password)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return redirect('index')
				else:
					return render(request, 'eleccion/no_activo.html')
			else:
				return render(request, 'eleccion/no_usuario.html')
	else:
		form = AuthenticationForm()
	return render(request, 'eleccion/login.html', {'form': form})

@login_required(login_url= 'login')
def VistaLogout(request):
	logout(request)
	return render(request, 'eleccion/logout.html')

class Index(TemplateView):
	template_name = "eleccion/index.html"

class GestionPartido(CreateView):
	template_name = "eleccion/formulario.html"
	model = Partido
	fields = ('nombre',)
	success_url = reverse_lazy('partido_listar_url')

	def get_context_data(self, **kwargs):
		#obtenemos el contextode la clase base
		context = super(GestionPartido, self).get_context_data(**kwargs)
		#anyadimos nuevas variables de contexto al diccionario
		context['titulo'] = 'Crear Partido'
		context['nombre_btn'] = 'Crear'
		#devolvemos el contexto
		return context

class PartidoListar(ListView):
	template_name = "eleccion/partido_listar.html"
	model = Partido

	def get_context_data(self, **kwargs):
		context = super(PartidoListar, self).get_context_data(**kwargs)
		context['partido_list'] = Partido.objects.all()[:10]
		return context

class PartidoDelete(DeleteView):
	template_name = "eleccion/partido_eliminar.html"
	model = Partido
	success_url = reverse_lazy('partido_listar_url')

	def dispatch(self, request, *args, **kwargs):
		if not request.user.has_perm('eleccion.delete_partido'):
			return redirect('login')
		return super(PartidoDelete, self).dispatch(request, *args, **kwargs)


class CircunscripcionLista(ListView):
	model = Circunscripcion
	template_name = "eleccion/circunscripcion.html"

	def get_context_data(self, **kwargs):
		context = super(CircunscripcionLista, self).get_context_data(**kwargs)
		context['object_list'] = Circunscripcion.objects.all()[:10]
		return context
		
class CircunscripcionCrear(CreateView):
	template_name = "eleccion/formulario.html"
	model = Circunscripcion
	fields = ('nombre', 'nEscanos')
	success_url = reverse_lazy('circunscripcion_url')

	def get_context_data(self, **kwargs):
		#obtenemos el contextode la clase base
		context = super(CircunscripcionCrear, self).get_context_data(**kwargs)
		#anyadimos nuevas variables de contexto al diccionario
		context['titulo'] = 'Crear Circunscripcion'
		context['nombre_btn'] = 'Crear'
		#devolvemos el contexto
		return context

class CircunscripcionDetalle(DetailView):
	model = Circunscripcion
	template_name = 'eleccion/vistaDetallada.html'

	def get_context_data(self, **kwargs):
		context = super(CircunscripcionDetalle, self).get_context_data(**kwargs)
		context['listadoMesas'] = Mesa.objects.filter(circunscripcion=self.kwargs['pk'])
		return context

class CircunscripcionEditar(UpdateView):
	template_name = 'eleccion/formulario.html'
	model = Circunscripcion
	fields = ('nombre', 'nEscanos')
	success_url = reverse_lazy('circunscripcion_url')

	def get_context_data(self, **kwargs):
		context = super(CircunscripcionEditar, self).get_context_data(**kwargs)
		context['titulo'] = 'Editar Circunscripcion'
		context['nombre_btn'] = 'Editar'
		return context

	def dispatch(self, request, *args, **kwargs):
		if not request.user.has_perm('eleccion.change_circunscripcion'):
			return redirect('circunscripcion_url')
		return super(CircunscripcionEditar,self).dispatch(request, *args, **kwargs)

class CircunscripcionEliminar(DeleteView):
	template_name = 'eleccion/eliminar.html'
	model = Circunscripcion
	success_url = reverse_lazy('circunscripcion_url')

	def dispatch(self, request, *args, **kwargs):
		if not request.user.has_perm('eleccion.delete_circunscripcion'):
			return redirect('login')
		return super(CircunscripcionEliminar, self).dispatch(request, *args, **kwargs)

#def CircunscripcionDelete(request, pk):
#	circunscripcion = Circunscripcion.objects.get(pk = pk)
#	if request.method == 'POST':
#		circunscripcion.delete()
#		return redirect('circunscripcion_url')
#	return render(request, 'eleccion/eliminar.html', { 'circunscripcion': circunscripcion })

def MesaDetalle(request, pk):
	mesa = Mesa.objects.get(pk= pk)
	return render(request, 'eleccion/vistaDetalladaMesa.html', { 'mesa': mesa })		

def MesaLista(request):
	mesa = Mesa.objects.all()[:10]
	return render(request,'eleccion/mesa.html', {'listadoMesa': mesa})

@login_required(login_url='login')
def MesaCrear(request):
	if request.method == 'POST':
		form = MesaForm(request.POST)
		if form.is_valid():
			mesa = form.save(commit=False)
			mesa.save()
			return redirect('mesa_url')
	else:
		form = MesaForm()
		return render(request,'eleccion/formulario.html', {'form': form, 'titulo': "Crear Mesa", 'nombre_btn': "Crear"})

@login_required(login_url='login')
def MesaEditar(request, pk):
	mesa = get_object_or_404(Mesa, pk=pk)
	if request.method == "POST":
		form = MesaForm(request.POST, instance=mesa)
		if form.is_valid():
			mesa = form.save(commit=False)
			mesa.save()
			return redirect('mesa_url')
	else:
		form = MesaForm(instance=mesa)
	return render(request, 'eleccion/formulario.html', {'form': form, 'titulo':"Editar Mesa", 'nombre_btn':"Editar"})

@login_required(login_url='login')
def MesaEliminar(request, pk):
	mesa = Mesa.objects.get(pk = pk)
	if request.method == 'POST':
		mesa.delete()
		return redirect('mesa_url')
	return render(request, 'eleccion/mesa_eliminar.html', {'mesa':mesa})



class ResultadoCrear(CreateView):
	template_name = 'eleccion/formulario.html'
	model = Resultado
	fields = ('partido', 'mesa', 'votos')
	success_url = reverse_lazy('resultado_url')

	def get_context_data(self, **kwargs):
	#obtener el contexto de la clase
		context = super(ResultadoCrear, self).get_context_data(**kwargs)
	#anyadimos nuevas variables de contexto al diccionario
		context['titulo'] = 'Crear Resultado'
		context['nombre_btn'] = 'Crear'
	#devolvemos el contexto
		return context

class ResultadoLista(ListView):
	model = Resultado
	template_name = "eleccion/resultado.html"

	def get_context_data(self, **kwargs):
		context = super(ResultadoLista, self).get_context_data(**kwargs)
		context['result_list'] = Resultado.objects.all()[:10]
		return context

class ResultadoEliminar(DeleteView):
	template_name = 'eleccion/eliminar_resultado.html'
	model = Resultado
	success_url = reverse_lazy('resultado_url')
	
	def get_context_data(self, **kwargs):
		context = super(ResultadoEliminar, self).get_context_data(**kwargs)
		context['titulo'] = 'Eliminar resultado'
		context['nombre_btn'] = 'Eliminar'
		return context

	def dispatch(self, request, *args, **kwargs):
		if not request.user.has_perm('eleccion.delete_resultado'):
			return redirect('login')
		return super(ResultadoEliminar,self).dispatch(request, *args, **kwargs)

class ResultadoEditar(UpdateView):
	template_name = 'eleccion/resultado_editar.html'
	model = Resultado
	fields = ('mesa', 'partido', 'votos')
	success_url = reverse_lazy('resultado_url')

	def get_context_data(self, **kwargs):
		context = super(ResultadoEditar, self).get_context_data(**kwargs)
		context['titulo'] = 'Editar Resultado'
		context['nombre_btn'] = 'Editar'
		return context

	def dispatch(self, request, *args, **kwargs):
		if not request.user.has_perms('eleccion.change_resultado'):
			return redirect('login')
		return super(ResultadoEditar, self).dispatch(request, *args, **kwargs)

