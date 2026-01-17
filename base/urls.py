from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import ListaPokemon, CrearPokemon, DetallePokemon, UploadedImage, administrador, ejecutar_rpa, dashboard, \
    cargar_excel, metricas_grafico_1, metricas_grafico_2, resumen_base_vs_fallidos, metricas_total_dia, \
    resumen_contactos, vista_campanas, ejecutar_campana, corregir_nombres_en_modelo, ver_metricas, clasificador_view, \
    ejecutar_completado, eliminar_reunion
from base.views import registro_usuario

urlpatterns = [path('', CrearPokemon.as_view(), name='inicio'),
               path('pokemon', ListaPokemon.as_view(), name='pokemon'),
               path('crear-pokemon', CrearPokemon.as_view(), name='crear-pokemon'),
               path('pokemon/<int:pk>', DetallePokemon.as_view(), name='pokemon'),
               path('maquinas/', views.manage_maquinas, name='manage_maquinas'),
               path('roles/', views.manage_roles, name='manage_roles'),
               path('personas/', views.manage_personas, name='manage_personas'),
               path('ubicaciones/', views.manage_ubicaciones, name='manage_ubicaciones'),
               path('atributos/', views.manage_atributos, name='manage_atributos'),
               path('tipos_inventario/', views.manage_tipos_inventario, name='manage_tipos_inventario'),
               path('planes_inventario/', views.manage_planes_inventario, name='manage_planes_inventario'),
               path('recursos/', views.recurso_list, name='recurso_list'),
               path('recursos/nuevo/', views.recurso_create, name='recurso_create'),
               path('recursos/<int:pk>/editar/', views.recurso_update, name='recurso_update'),
               path('recursos/<int:pk>/eliminar/', views.recurso_delete, name='recurso_delete'),
               path('upload/', views.upload_image, name='upload_image'),
               path("administrador/", administrador, name="administrador"),
               path("dashboard/", dashboard, name="dashboard"),  # Ruta para el panel
               path("ejecutar-rpa/", ejecutar_rpa, name="ejecutar_rpa"),  # ✅ Verificar que la ruta está bien definida
               path("cargar-excel/", cargar_excel, name="cargar_excel"),
               path('contactos/', views.vista_contactos, name='vista_contactos'),
               path('contactos/eliminar_multiples/', views.eliminar_multiples, name='eliminar_multiples'),
               path('contactos/editar/<int:contacto_id>/', views.editar_contacto, name='editar_contacto'),
               path('contactos/eliminar/<int:contacto_id>/', views.eliminar_contacto, name='eliminar_contacto'),
               path("campanas/", vista_campanas, name="vista_campanas"),
               path("campanas/ejecutar/", ejecutar_campana, name="ejecutar_campana"),
               path("campanas/<int:campana_id>/editar/", views.editar_campana, name="editar_campana"),
               path("campanas/<int:campana_id>/eliminar/", views.eliminar_campana, name="eliminar_campana"),
               path('corregir-nombres-modelo/', corregir_nombres_en_modelo, name='corregir_nombres_modelo'),
               path('campañas/<int:campaña_id>/metricas/', ver_metricas, name='ver_metricas'),

               path('impulso/', views.lista_iniciativas, name='lista_iniciativas'),
               path('impulso/crear/', views.crear_iniciativa, name='crear_iniciativa'),
               path('impulso/<int:iniciativa_id>/', views.detalle_iniciativa, name='detalle_iniciativa'),
               path('impulso/<int:iniciativa_id>/plan/', views.vista_plan, name='vista_plan'),
               path('impulso/tarea/<int:tarea_id>/completar/', views.actualizar_estado_tarea, name='actualizar_estado_tarea'),
               path('impulso/fase/<int:fase_id>/', views.vista_fase_detalle, name='vista_fase_detalle'),
               path('impulso/gantt/', views.gantt_general, name='gantt_general'),
               path('impulso/iniciativa/<int:pk>/editar/', views.editar_iniciativa, name='editar_iniciativa'),
               path('impulso/iniciativa/<int:pk>/eliminar/', views.eliminar_iniciativa, name='eliminar_iniciativa'),
               path('tarea/<int:pk>/editar/', views.editar_tarea, name='editar_tarea'),
               path('impulso/crear/personalizada/', views.crear_iniciativa_personalizada, name='crear_iniciativa_personalizada'),
               path('fase/crear/<int:iniciativa_id>/', views.crear_fase, name='crear_fase'),
               path('tarea/crear/<int:iniciativa_id>/', views.crear_tarea_suelta, name='crear_tarea_suelta'),
               path('tarea/crear/fase/<int:fase_id>/', views.crear_tarea_en_fase, name='crear_tarea_en_fase'),
               path('fase/editar/<int:fase_id>/', views.editar_fase, name='editar_fase'),
               path('tarea/<int:tarea_id>/completar/', views.marcar_tarea_completada, name='marcar_tarea_completada'),


    path('procesos/nuevo/', views.crear_proceso, name='crear_proceso'),
    path('procesos/<int:proceso_id>/', views.ver_proceso, name='ver_proceso'),
    path('procesos/', views.lista_procesos, name='lista_procesos'),
    path('procesos/<int:proceso_id>/agregar-hito/', views.agregar_hito, name='agregar_hito'),
    path('procesos/<int:proceso_id>/editar/', views.editar_proceso, name='editar_proceso'),
    path('procesos/hito/<int:hito_id>/editar/', views.editar_hito, name='editar_hito'),
    path('procesos/<int:proceso_id>/cerrar/', views.cerrar_proceso, name='cerrar_proceso'),
    path('procesos/<int:proceso_id>/eliminar/', views.eliminar_proceso, name='eliminar_proceso'),


    path('clasificador/', clasificador_view, name='clasificador_excel'),



    path('agenda/nuevo/', views.registrar_evento, name='registrar_evento'),
    path('agenda/mia/', views.mi_agenda, name='mi_agenda'),
    path('comunidad/feed/', views.feed_comunitario, name='feed_comunitario'),

    path('campanas/<int:campana_id>/panel/', views.panel_campana, name='panel_campana'),

    path('feed/reaccion/<int:publicacion_id>/<str:tipo>/', views.dar_reaccion, name='dar_reaccion'),
    path('feed/publicar/', views.publicar_en_feed, name='publicar_en_feed'),
    path('feed/comunitario/', views.feed_comunitario, name='feed_comunitario'),


    path('usuario/metas/', views.panel_metas_usuario, name='panel_metas_usuario'),
    path('fase/<int:fase_id>/completar/', views.completar_fase, name='completar_fase'),



    path('api/tareas/', views.tareas_json, name='tareas_json'),


    path('rpa/open/', views.panel_open_to_work, name='panel_open_to_work'),


path("metricas/exitos-dia/", metricas_grafico_2),
path("metricas/resumen/", resumen_base_vs_fallidos),
path("metricas/total-dia/", metricas_total_dia),
path("metricas/resumen-contactos/", resumen_contactos),




    path('login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', registro_usuario, name='registro'),


    path('tarea/eliminar/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('fase/eliminar/<int:fase_id>/', views.eliminar_fase, name='eliminar_fase'),
    path('fase/<int:fase_id>/replicar/', views.replicar_fase, name='replicar_fase'),
    path('tareas/reordenar/<int:fase_id>/', views.reordenar_tareas, name='reordenar_tareas'),



    path('rpa/completar/', ejecutar_completado, name='completar_contactos'),
    path('contactos/respuesta/<int:contacto_id>/', views.registrar_respuesta, name='registrar_respuesta'),
    path('actualizar-estatus/<int:id>/', views.actualizar_estatus, name='actualizar_estatus'),


    path('flujo/', views.flujo_ventas, name='flujo_ventas'),
    path('actualizar_etapa/<int:contacto_id>/<str:etapa>/', views.actualizar_etapa, name='actualizar_etapa'),
    path('crear_reunion/', views.crear_reunion, name='crear_reunion'),
    path('contactos_con_reuniones/', views.contactos_con_reuniones, name='contactos_con_reuniones'),

    path('reuniones/eliminar/', eliminar_reunion, name='eliminar_reunion'),
path('impulso/panel-avance/', views.panel_avance, name='panel_avance'),








]




# ✅ Para servir archivos multimedia en modo DEBUG

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



