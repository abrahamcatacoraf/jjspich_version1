from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from functools import wraps

def solo_admin(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (
            request.user.is_superuser or
            request.user.groups.filter(name='Administrador').exists()
        ):
            return view_func(request, *args, **kwargs)
        return redirect('sin_permiso')
    return wrapper

def admin_o_recepcionista(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (
            request.user.is_superuser or
            request.user.groups.filter(
                name__in=['Administrador', 'Recepcionista']
            ).exists()
        ):
            return view_func(request, *args, **kwargs)
        return redirect('sin_permiso')
    return wrapper