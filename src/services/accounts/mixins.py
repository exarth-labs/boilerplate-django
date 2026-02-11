from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404

from src.core.mixins import (CoreListViewMixin, CoreDetailViewMixin, CoreCreateViewMixin,
    CoreUpdateViewMixin, CoreDeleteViewMixin)

""" ROLES MIXINS --------------------------------------------------------------------------------------------------- """


class SuperUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise Http404


class StaffMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise Http404



class GenericListViewMixin(CoreListViewMixin):
    permission_prefix = 'accounts'


class GenericDetailViewMixin(CoreDetailViewMixin):
    permission_prefix = 'accounts'


class GenericCreateViewMixin(CoreCreateViewMixin):
    permission_prefix = 'accounts'


class GenericUpdateViewMixin(CoreUpdateViewMixin):
    permission_prefix = 'accounts'


class GenericDeleteViewMixin(CoreDeleteViewMixin):
    permission_prefix = 'accounts'





