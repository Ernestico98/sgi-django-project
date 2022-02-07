from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from sgi.models import Grupo_Investigacion, User, Salon, Medio, Prestamo
from django.utils import timezone
from datetime import datetime


class SignUpForm(UserCreationForm):
    group_name = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'CI', 'address', 'user_role', 'group_name')

    def is_valid(self):
        valid = super(SignUpForm, self).is_valid()
        if self.data['user_role'] != 'admin' and self.data['group_name'] == '':
            self.errors['group_name'] = ['Not admin-user should belong to an investigation group']
            return False
        if not valid:
            return False
        return True

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        choices = [('', '')] + [(i['nombg'], i['nombg']) for i in Grupo_Investigacion.objects.values('nombg')]
        self.fields['group_name'].choices = choices


class SignUpExternForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'CI', 'address')


class NewGroupForm(forms.ModelForm):
    group_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Grupo_Investigacion
        fields = ('group_name',)


class NewRoomForm(forms.ModelForm):
    room_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Salon
        fields = ('room_name',)


class NewResourceForm(forms.ModelForm):
    room = forms.ChoiceField(choices=[], required=True)
    group = forms.ChoiceField(choices=[], required=True)

    class Meta:
        model = Medio
        fields = ('INV', 'descripcion', 'garantia', 'valor', 'room', 'group',)

    def __init__(self, *args, **kwargs):
        super(NewResourceForm, self).__init__(*args, **kwargs)
        choices_room = [('', '')] + [(i['nombs'], i['nombs']) for i in Salon.objects.values('nombs')]
        choices_group = [('', '')] + [(i['nombg'], i['nombg']) for i in Grupo_Investigacion.objects.values('nombg')]
        self.fields['room'].choices = choices_room
        self.fields['group'].choices = choices_group


class EstadoForm(forms.Form):
    grupo = forms.ChoiceField(choices=[], required=False)
    salon = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super(EstadoForm, self).__init__(*args, **kwargs)
        choices_room = [('', '')] + [(i['nombs'], i['nombs']) for i in Salon.objects.values('nombs')]
        choices_group = [('', '')] + [(i['nombg'], i['nombg']) for i in Grupo_Investigacion.objects.values('nombg')]
        self.fields['salon'].choices = choices_room
        self.fields['grupo'].choices = choices_group


class EstadoGrupoForm(forms.Form):
    salon = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super(EstadoGrupoForm, self).__init__(*args, **kwargs)
        choices_room = [('', '')] + [(i['nombs'], i['nombs']) for i in Salon.objects.values('nombs')]
        self.fields['salon'].choices = choices_room


class ValorMediosForm(forms.Form):
    filtrar_por = forms.ChoiceField(choices=[('grupo', 'Grupo'), ('salon', 'Salón')])


class RegisterPrestamoForm(forms.Form):
    CI = forms.IntegerField(required=True)
    descripcion = forms.CharField(max_length=100, required=False)
    INV = forms.CharField(max_length=20, required=False)
    f_devolucion = forms.DateField(required=False)

    def is_valid(self, *args, **kwargs):
        btn = kwargs['kwargs'].pop('btn')
        if not super(RegisterPrestamoForm, self).is_valid():
            return False

        ci = self.cleaned_data['CI']
        if ci < 10000000000 or ci > 99999999999:
            self.errors['CI'] = ['Inserte un número de carnet válido!!!']
            return False

        user = User.objects.filter(CI=self.data['CI'])
        if not user.exists():
            self.errors['CI'] = ['El usuario solicitado no existe!!!']
            return False

        user = user.first()
        t = timezone.now()
        q = Prestamo.objects.filter(user=user)
        q = q.filter(f_devolucion__lt=t)
        if q.exists():
            self.errors['CI'] = ['El usuario tiene préstamos atrasados']
            return False

        if btn == 'btn3':
            inv = self.data['INV']
            ok = True
            if not inv or not Medio.objects.filter(prestado=False, INV=inv).exists():
                self.errors['INV'] = ['El medio solicitado no está disponible']
                ok = False

            if not self.data['f_devolucion']:
                self.errors['f_devolucion'] = ['Debe insertar una fecha']
                ok = False
            else:
                f = self.data['f_devolucion'].split('-')
                y = int(f[0])
                m = int(f[1])
                d = int(f[2])
                t = timezone.now()
                if datetime(y, m, d) < datetime(t.year, t.month, t.day):

                    self.errors['f_devolucion'] = ['La fecha no debe ser anterior a la actual']
                    ok = False
            return ok
        return True

    def __init__(self, *args, **kwargs):
        super(RegisterPrestamoForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].disabled = True
        self.fields['INV'].disabled = True
        self.fields['f_devolucion'].disabled = True


class DevolucionForm(forms.Form):
    INV = forms.CharField(max_length=20)

    def is_valid(self):
        valid = super(DevolucionForm, self).is_valid()

        if not Medio.objects.filter(prestado=True, INV=self.data['INV']).exists():
            self.errors['INV'] = ['El medio ingresado no existe o no está prestado']
            return False
        return valid

class BeneficiariosForm(forms.Form):
    filtrar_por = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super(BeneficiariosForm, self).__init__(*args, **kwargs)
        choices = [('', ''), ('externo', 'Personal externo')] + [(i['nombg'], i['nombg']) for i in Grupo_Investigacion.objects.values('nombg')]
        self.fields['filtrar_por'].choices = choices


class PrestamosForm(forms.Form):
    filtrar_por = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super(PrestamosForm, self).__init__(*args, **kwargs)
        choices = [('', ''), ('externo', 'Personal externo')] + [(i['nombg'], i['nombg']) for i in Grupo_Investigacion.objects.values('nombg')]
        self.fields['filtrar_por'].choices = choices