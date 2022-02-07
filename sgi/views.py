from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, View
from django import forms
from sgi.models import Grupo_Investigacion, User, Centro, Salon, Medio, Prestamo
from django.contrib.auth import login, authenticate
from sgi.forms import SignUpForm, SignUpExternForm, NewGroupForm, NewRoomForm, NewResourceForm, EstadoForm, \
EstadoGrupoForm, ValorMediosForm, RegisterPrestamoForm, DevolucionForm, BeneficiariosForm, PrestamosForm
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime


def debug(s):
    with open('/home/ernestico/Desktop/tmp.txt', 'w' ) as f:
        f.write(s)


class Home(View):
    def get(self, request):
        q = User.objects.filter(username=request.user.username)
        logged_user = None
        if q.exists():
            logged_user = q.first()
        return render(request, 'base.html', {'logged_user': logged_user})


@login_required
def signup_extern(request):
    logged_user = User.objects.get(username=request.user.username)
    if logged_user.user_role not in ['admin', 'jefe']:
        return render(request, 'error.html', {'message': 'Solo los administrados y jefes de grupos pueden agregar personal externo!!!', 'logged_user': logged_user})

    if request.method == 'POST':
        form = SignUpExternForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.f_ingreso = timezone.now()
            user.user_role = 'externo'
            user.save()
            return redirect('home')
    else:
        form = SignUpExternForm()
    return render(request, 'signup_extern.html', {'form': form, 'logged_user':logged_user})



@login_required
def signup(request):
    logged_user = User.objects.get(username=request.user.username)
    if logged_user.user_role != 'admin':
        return render(request, 'error.html', {'message': 'Solo los administradores pueden registrar nuevos usuarios!!!', 'logged_user': logged_user})

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.user_role != 'admin':
                grupo = Grupo_Investigacion.objects.get(nombg=request.POST['group_name'])
                user.grupo = grupo
            user.f_ingreso = timezone.now()
            user.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'logged_user':logged_user})


@login_required
def new_group(request):
    logged_user = User.objects.get(username=request.user.username)
    if logged_user.user_role != 'admin':
        return render(request, 'error.html', {'message': 'Solo los administradores pueden crear grupos!!!', 'logged_user': logged_user})

    if request.method == 'POST':
        form = NewGroupForm(request.POST)
        if form.is_valid():
            grupo = Grupo_Investigacion()
            grupo.nombg = form.cleaned_data['group_name']
            grupo.centro = Centro.objects.first()
            grupo.save()
            return redirect('home')
    else:
        form = NewGroupForm()
    return render(request, 'new_group.html', {'form': form, 'logged_user':logged_user})


@login_required
def new_room(request):
    logged_user = User.objects.get(username=request.user.username)
    if logged_user.user_role != 'admin':
        return render(request, 'error.html', {'message': 'Solo los administradores pueden registrar nuevos salones!!!', 'logged_user': logged_user})

    if request.method == 'POST':
        form = NewRoomForm(request.POST)
        if form.is_valid():
            salon = Salon()
            salon.nombs = form.cleaned_data['room_name']
            salon.save()
            return redirect('home')
    else:
        form = NewRoomForm()
    return render(request, 'new_room.html', {'form': form, 'logged_user':logged_user})


@login_required
def new_resource(request):
    logged_user = User.objects.get(username=request.user.username)
    if logged_user.user_role != 'admin':
        return render(request, 'error.html', {'message': 'Solo los administradores pueden agregar medios!!!', 'logged_user': logged_user})

    if request.method == 'POST':
        form = NewResourceForm(request.POST)
        if form.is_valid():
            medio = Medio()
            medio.INV = form.cleaned_data['INV']
            medio.descripcion = form.cleaned_data['descripcion']
            medio.garantia = form.cleaned_data['garantia']
            medio.valor = form.cleaned_data['valor']
            medio.salon = Salon.objects.get(nombs=request.POST['room'])
            medio.grupo = Grupo_Investigacion.objects.get(nombg=request.POST['group'])
            medio.save()
            return redirect('home')
    else:
        form = NewResourceForm()
    return render(request, 'new_resource.html', {'form': form, 'logged_user':logged_user})


@login_required
def estado(request):
    logged_user = User.objects.get(username=request.user.username)
    if logged_user.user_role != 'admin':
        return render(request, 'error.html', {'message': 'Solo los administradores pueden ver el estado de todos los medios!!!', 'logged_user': logged_user})

    q = Medio.objects.all()
    medios = []
    if request.method == 'POST':
        form = EstadoForm(request.POST)
        header = ['INV', 'Descripción', 'Garantía', 'Prestado', 'Fecha. Entrada', 'Valor']
        if form.data['grupo'] != '':
            q = q.filter(grupo__nombg=form.data['grupo'])
        else:
            header.append('Grupo')
        if form.data['salon'] != '':
            q = q.filter(salon__nombs=form.data['salon'])
        else:
            header.append('Salon')
        for i in q:
            tmp = dict()
            tmp['INV'] = i.INV
            tmp['Descripción'] = i.descripcion
            tmp['Garantía'] = 'Si' if i.garantia else 'No'
            tmp['Prestado'] = 'Si' if i.prestado else 'No'
            tmp['Fecha. entrada'] = i.f_entrada
            tmp['Valor'] = i.valor
            if form.data['grupo'] == '':
                tmp['Grupo'] = i.grupo.nombg
            if form.data['salon'] == '':
                tmp['Salon'] = i.salon.nombs
            medios.append(tmp)
    else:
        header = ['INV', 'Descripción', 'Garantía', 'Prestado', 'Fecha. Entrada', 'Valor', 'Grupo', 'Salon']
        for i in q:
            tmp = dict()
            tmp['INV'] = i.INV
            tmp['Descripción'] = i.descripcion
            tmp['Garantía'] = 'Si' if i.garantia else 'No'
            tmp['Prestado'] = 'Si' if i.prestado else 'No'
            tmp['Fecha. entrada'] = i.f_entrada
            tmp['Valor'] = i.valor
            tmp['Grupo'] = i.grupo.nombg
            tmp['Salon'] = i.salon.nombs
            medios.append(tmp)
        form = EstadoForm()
    return render(request, 'estado.html', {'medios': medios, 'header': header, 'form': form, 'logged_user':logged_user})


@login_required
def estado_por_grupo(request, grupo_pk):
    logged_user = User.objects.get(username=request.user.username)
    role = logged_user.user_role
    if role == 'externo' or (role != 'admin' and logged_user.grupo.pk != int(grupo_pk)):
        return render(request, 'error.html', {'message': 'Solo los administradores o miembros de un grupo pueden ver el estado de los medios del grupo!!!', 'logged_user': logged_user})

    if not Grupo_Investigacion.objects.all().filter(pk=grupo_pk).exists():
        return render(request, 'error.html', {'message': 'El grupo solicitado no existe!!!', 'logged_user': logged_user})

    medios = []
    q = Medio.objects.all().filter(grupo__pk=grupo_pk)
    if request.method == 'POST':
        form = EstadoGrupoForm(request.POST)
        header = ['INV', 'Descripción', 'Garantía', 'Prestado', 'Fecha. Entrada', 'Valor']
        if form.data['salon'] != '':
            q = q.filter(salon__nombs=form.data['salon'])
        else:
            header.append('Salon')
        for i in q:
            tmp = dict()
            tmp['INV'] = i.INV
            tmp['Descripción'] = i.descripcion
            tmp['Garantía'] = 'Si' if i.garantia else 'No'
            tmp['Prestado'] = 'Si' if i.prestado else 'No'
            tmp['Fecha. entrada'] = i.f_entrada
            tmp['Valor'] = i.valor
            if form.data['salon'] == '':
                tmp['Salon'] = i.salon.nombs
            medios.append(tmp)
    else:
        form = EstadoGrupoForm()
        header = ['INV', 'Descripción', 'Garantía', 'Prestado', 'Fecha. Entrada', 'Valor', 'Salon']
        for i in q:
            tmp = dict()
            tmp['INV'] = i.INV
            tmp['Descripción'] = i.descripcion
            tmp['Garantía'] = 'Si' if i.garantia else 'No'
            tmp['Prestado'] = 'Si' if i.prestado else 'No'
            tmp['Fecha. entrada'] = i.f_entrada
            tmp['Valor'] = i.valor
            tmp['Salon'] = i.salon.nombs
            medios.append(tmp)
    nombre_grupo = Grupo_Investigacion.objects.get(pk=grupo_pk).nombg
    return render(request, 'estado_por_grupo.html', {'header': header, 'medios': medios,'form': form, 'grupo': nombre_grupo, 'logged_user':logged_user})


@login_required
def valor_medios(request):
    logged_user = User.objects.get(username=request.user.username)
    if logged_user.user_role != 'admin':
        return render(request, 'error.html', {'message': 'Esta pagina solo puede ser accedida por administradores!!!', 'logged_user': logged_user})

    def get_info_por_grupo():
        header = ['Grupo', 'Valor']
        body = []
        for grupo in Grupo_Investigacion.objects.all():
            body.append( [ grupo.nombg, Medio.objects.filter(grupo=grupo).aggregate(Sum('valor'))['valor__sum']] )
            if body[-1][1] is None:
                body[-1][1] = '0.00'
            else:
                body[-1][1] = '{:.2f}'.format(body[-1][1])
        return header, body

    def get_info_por_salon():
        header = ['Salón', 'Valor']
        body = []
        for salon in Salon.objects.all():
            body.append([salon.nombs, Medio.objects.filter(salon=salon).aggregate(Sum('valor'))['valor__sum']])
            if body[-1][1] is None:
                body[-1][1] = '0.00'
            else:
                body[-1][1] = '{:.2f}'.format(body[-1][1])
        return header, body

    if request.method == 'POST':
        form = ValorMediosForm(request.POST)
        if form.data['filtrar_por'] == 'grupo':
            header, body = get_info_por_grupo()
        else:
            header, body = get_info_por_salon()
    else:
        form = ValorMediosForm()
        header, body = get_info_por_grupo()
    sum = Medio.objects.all().aggregate(Sum('valor'))['valor__sum']
    sum = '{:.2f}'.format(sum)
    return render(request, 'valor_medios.html', {'form': form, 'sum': sum, 'header': header, 'body': body, 'logged_user':logged_user})


@login_required
def registrar_prestamo(request):
    logged_user = User.objects.get(username=request.user.username)
    if logged_user.user_role not in ['admin', 'jefe']:
        return render(request, 'error.html', {'message': 'Solo los administradores y los jefes de grupo pueden registrar préstamos!!!', 'logged_user': logged_user})

    objects = Medio.objects.filter(prestado=False)
    valid_btn1 = False
    valid_btn3 = False
    date_class = 'form-control'
    if request.method == 'POST':
        if 'btn_externo' in request.POST:
            return redirect('signup_extern')

        form = RegisterPrestamoForm(request.POST)
        if form.is_valid(kwargs={'btn': 'btn1'}):
            valid_btn1 = True
            user = User.objects.get(CI=form.data['CI'])
            form.fields['descripcion'].disabled = False
            form.fields['INV'].disabled = False
            form.fields['f_devolucion'].disabled = False

            if 'descripcion' in request.POST:
                desc = form.data['descripcion']
                objects = objects.filter(descripcion__contains=desc)

            if 'btn3' in request.POST:
                date_class = 'form-control is-invalid'

            if 'btn3' in request.POST and form.is_valid(kwargs={'btn': 'btn3'}):

                date_class += 'form-control is-valid'
                valid_btn3 = True
                inv = form.data['INV']
                medio = Medio.objects.get(INV=inv)

                #y, m, d = map ( int, form.data['f_devolucion'].split('-') )
                devolucion = form.data['f_devolucion']
                prestamo = Prestamo(user=user, medio=medio, f_devolucion=devolucion)
                prestamo.save()
                medio.prestado = True
                medio.save()
    else:
        form = RegisterPrestamoForm()

    header = ['INV', 'Descripción']
    body = []
    for i in objects:
        body.append( [i.INV, i.descripcion])
    return render(request, 'registrar_prestamo.html', {'date_class': date_class, 'form': form, 'valid_btn1': valid_btn1, 'valid_btn3': valid_btn3,'header': header, 'body': body, 'logged_user':logged_user})


@login_required
def registrar_devolucion(request):
    logged_user = User.objects.get(username=request.user.username)
    if logged_user.user_role not in ['admin', 'jefe']:
        return render(request, 'error.html',
            {'message': 'Solo los administradores y los jefes de grupo pueden registrar devoluciones!!!', 'logged_user': logged_user})

    if request.method == 'POST':
        form = DevolucionForm(request.POST)
        if form.is_valid():
            medio = Medio.objects.get(INV=form.data['INV'])
            medio.prestado = False
            medio.prestamo.delete()
            medio.save()
    else:
        form = DevolucionForm()
    return render(request, 'registrar_devolucion.html', {'form': form, 'logged_user':logged_user})


@login_required
def beneficiarios(request):
    logged_user = User.objects.get(username=request.user.username)
    if logged_user.user_role not in ['admin']:
        return render(request, 'error.html',
                      {'message': 'Solo los administradores pueden acceder a esta página!!!', 'logged_user': logged_user})

    header = ['CI', 'Nombres', 'Apellidos', 'Dirección', 'Préstamos Actuales', 'Atrasados']
    body = []
    users = User.objects.all()
    for user in users:
        cntp = Prestamo.objects.filter(user=user).count()
        cntp_atrasados = Prestamo.objects.filter(user=user, f_devolucion__lt=timezone.now()).count()
        if cntp > 0:
            body.append([user.CI, user.first_name, user.last_name, user.address, str(cntp),
                         str(cntp_atrasados)])

    if request.method == 'POST':
        form = BeneficiariosForm(request.POST)
        w = form.data['filtrar_por']

        if w == 'externo':
            header = ['CI', 'Nombres', 'Apellidos', 'Dirección', 'Préstamos Actuales', 'Atrasados']
            body = []
            users = User.objects.filter(user_role='externo')
            for user in users:
                cntp = Prestamo.objects.filter(user=user).count()
                cntp_atrasados = Prestamo.objects.filter(user=user, f_devolucion__lt=timezone.now()).count()
                if cntp > 0:
                    body.append([user.CI, user.first_name, user.last_name, user.address, str(cntp), str(cntp_atrasados)] )
        elif w != '':
            header = ['CI', 'Nombres', 'Apellidos', 'Dirección', 'Préstamos Actuales', 'Atrasados']
            body = []
            users = User.objects.exclude(user_role='externo').filter(grupo__nombg=w)
            for user in users:
                cntp = Prestamo.objects.filter(user=user).count()
                cntp_atrasados = Prestamo.objects.filter(user=user, f_devolucion__lt=timezone.now()).count()
                if cntp > 0:
                    body.append([user.CI, user.first_name, user.last_name, user.address, str(cntp), str(cntp_atrasados)])
    else:
        form = BeneficiariosForm()

    return render(request, 'beneficiarios.html', {'form': form, 'header': header, 'body': body, 'logged_user':logged_user})


@login_required
def beneficiarios_por_grupo(request, grupo_pk):
    logged_user = User.objects.get(username=request.user.username)
    if logged_user.user_role not in ['admin', 'jefe']:
        return render(request, 'error.html',
                      {'message': 'Solo los administradores y los jefes pueden acceder a esta página!!!', 'logged_user': logged_user})

    if logged_user.user_role == 'jefe' and logged_user.grupo.pk != int(grupo_pk):
        return render(request, 'error.html',
                      {'message': 'Usted no es el jefe de este grupo. No tiene acceso a la página solicitada!!!', 'logged_user': logged_user})

    if not Grupo_Investigacion.objects.all().filter(pk=grupo_pk).exists():
        return render(request, 'error.html', {'message': 'El grupo solicitado no existe!!!'})

    header = ['CI', 'Nombres', 'Apellidos', 'Dirección', 'Préstamos actuales', 'Atrasados']
    body = []

    grupo = Grupo_Investigacion.objects.get(pk=grupo_pk)
    users = User.objects.exclude(user_role='externo').filter(grupo=grupo)
    for user in users:
        cntp = Prestamo.objects.filter(user=user).count()
        cntp_atrasados = Prestamo.objects.filter(user=user, f_devolucion__lt=timezone.now()).count()
        if cntp > 0:
            body.append([user.CI, user.first_name, user.last_name, user.address, str(cntp), str(cntp_atrasados)])

    return render(request, 'beneficiarios_por_grupo.html', {'header': header, 'body': body, 'grupo': grupo.nombg, 'logged_user':logged_user})


@login_required
def prestamos(request):
    logged_user = User.objects.get(username=request.user.username)
    if logged_user.user_role not in ['admin']:
        return render(request, 'error.html',
                      {'message': 'Solo los administradores pueden acceder a esta página!!!', 'logged_user': logged_user})

    header = ['INV', 'Descripción', 'CI', 'Nombres', 'Apellidos', 'Fecha. Devolución', 'Atrasado']
    body = []
    for p in Prestamo.objects.all():
        body.append([
            p.medio.INV,
            p.medio.descripcion,
            p.user.CI,
            p.user.first_name,
            p.user.last_name,
            p.f_devolucion,
            'Si' if p.f_devolucion < timezone.now() else 'No',
        ])

    if request.method == 'POST':
        form = PrestamosForm(request.POST)

        if form.data['filtrar_por'] == 'externo':
            body = []
            for p in Prestamo.objects.all():
                if p.user.user_role == 'externo':
                    body.append([
                        p.medio.INV,
                        p.medio.descripcion,
                        p.user.CI,
                        p.user.first_name,
                        p.user.last_name,
                        p.f_devolucion,
                        'Si' if p.f_devolucion < timezone.now() else 'No',
                    ])
        elif form.data['filtrar_por'] != '':
            body = []
            for p in Prestamo.objects.all():
                if p.medio.grupo.nombg == form.data['filtrar_por']:
                    body.append([
                        p.medio.INV,
                        p.medio.descripcion,
                        p.user.CI,
                        p.user.first_name,
                        p.user.last_name,
                        p.f_devolucion,
                        'Si' if p.f_devolucion < timezone.now() else 'No',
                    ])
    else:
        form = PrestamosForm()

    return render(request, 'prestamos.html', {'form': form, 'body': body, 'header': header, 'logged_user':logged_user})


@login_required
def prestamos_por_grupo(request, grupo_pk):
    logged_user = User.objects.get(username=request.user.username)
    if logged_user.user_role not in ['admin', 'jefe']:
        return render(request, 'error.html',
                      {'message': 'Solo los administradores y los jefes pueden acceder a esta página!!!', 'logged_user': logged_user})

    if logged_user.user_role == 'jefe' and logged_user.grupo.pk != int(grupo_pk):
        return render(request, 'error.html',
                      {'message': 'Usted no es el jefe de este grupo. No tiene acceso a la página solicitada!!!', 'logged_user': logged_user})

    if not Grupo_Investigacion.objects.all().filter(pk=grupo_pk).exists():
        return render(request, 'error.html', {'message': 'El grupo solicitado no existe!!!'})

    header = ['INV', 'Descripción', 'CI', 'Nombres', 'Apellidos', 'Fecha. Devolución', 'Atrasado']
    body = []
    grupo = Grupo_Investigacion.objects.get(pk=grupo_pk)
    for p in Prestamo.objects.all():
        if p.medio.grupo == grupo:
            body.append([
                p.medio.INV,
                p.medio.descripcion,
                p.user.CI,
                p.user.first_name,
                p.user.last_name,
                p.f_devolucion,
                'Si' if p.f_devolucion < timezone.now() else 'No',
            ])

    return render(request, 'prestamos_por_grupo.html', {'header':header, 'body': body, 'grupo':grupo.nombg, 'logged_user':logged_user})