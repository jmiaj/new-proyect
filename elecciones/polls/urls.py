from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.Index.as_view(), name = 'index'),
	url(r'^login/$', views.acceso, name = 'login'),
	url(r'^logout/$', views.VistaLogout, name = 'logout'),
	url(r'^registro/$', views.newUser, name = 'registro'),


	url(r'^circunscripcion/$', views.CircunscripcionLista.as_view(), name = 'circunscripcion_url'),
	url(r'^circunscripcion/crear/$', views.CircunscripcionCrear.as_view(), name = 'circunscripcion_crear_url'),
	url(r'^circunscripcion/vistaDetallada/(?P<pk>.*)$', views.CircunscripcionDetalle.as_view(), name = 'circunscripcion_detalle_url'),
	url(r'^circunscripcion/editar/(?P<pk>.*)$', views.CircunscripcionEditar.as_view(), name = 'circunscripcion_editar_url'),
	url(r'^circunscripcion/eliminar/(?P<pk>.*)$', views.CircunscripcionEliminar.as_view(), name = 'circunscripcion_eliminar_url'),


	url(r'^mesa/$', views.MesaLista, name='mesa_url'),
    url(r'^mesa/vistaDetalladaMesa/(?P<pk>.*)$', views.MesaDetalle, name='mesa_detalle_url'),
   	url(r'^mesa/crear/$', views.MesaCrear, name='mesa_crear_url'),
    url(r'^mesa/editar/(?P<pk>.*)$', views.MesaEditar, name='mesa_editar_url'),
    url(r'^mesa/eliminar/(?P<pk>.*)$', views.MesaEliminar, name = 'mesa_eliminar_url'),


   	url(r'^resultado/$', views.ResultadoLista.as_view(), name='resultado_url'),
    url(r'^resultado/crear/$', views.ResultadoCrear.as_view(), name='resultado_crear_url'),
    url(r'^resultado/eliminar/(?P<pk>.*)$', views.ResultadoEliminar.as_view(), name = 'resultado_eliminar_url'),
	url(r'^resultado/editar/(?P<pk>.*)$', views.ResultadoEditar.as_view(), name = 'resultado_editar_url'),


	url(r'^partido/listar/$', views.PartidoListar.as_view(), name = 'partido_listar_url'),
	url(r'^partido/crear/$', views.GestionPartido.as_view(), name='partido_crear_url'),
    url(r'^partido/eliminar/(?P<pk>.*)$', views.PartidoDelete.as_view(), name = 'partido_eliminar_url'),
]