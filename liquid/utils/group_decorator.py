from functools import wraps

from intranet.models import Group
from django.core.exceptions import PermissionDenied

def check_group_admin(groups,request):
   groups.append('Top4')
   user_groups = request.user.groupmember_set.filter(is_admin__exact=True).filter(group__name__in=groups)
   if not user_groups:
      raise PermissionDenied()
      return fales
   return True

def group_admin_required(groups=[]):    
   def decorator(func):
      def inner_decorator(request,*args, **kwargs):
         if check_group_admin(groups,request):
            return func(request, *args, **kwargs)
      return wraps(func)(inner_decorator)
   return decorator
   
def specific_group_admin_required(row):
   def decorator(func):
      def inner_decorator(request,*args, **kwargs):
         g = Group.objects.get(id=kwargs[row])
         groups = [g.name]
         if check_group_admin(groups,request):
            return func(request, *args, **kwargs)
      return wraps(func)(inner_decorator)
   return decorator