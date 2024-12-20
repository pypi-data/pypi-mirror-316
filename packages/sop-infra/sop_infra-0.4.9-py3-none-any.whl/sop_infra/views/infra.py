from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse

from utilities.views import register_model_view, ViewTab, ObjectPermissionRequiredMixin
from utilities.permissions import get_permission_for_model
from utilities.forms import restrict_form_fields
from netbox.views import generic
from dcim.models import Site

from sop_infra.forms import *
from sop_infra.tables import (
    SopInfraTable,
    SopInfraSizingTable,
    SopInfraMerakiTable,
    SopInfraClassificationTable,
)
from sop_infra.models import *
from sop_infra.filtersets import SopInfraFilterset
from sop_infra.utils import SopInfraRelatedModelsMixin, SopInfraRefreshMixin


__all__ = (
    "SopInfraTabView",
    "SopInfraAddView",
    "SopInfraEditView",
    "SopInfraListView",
    "SopInfraDeleteView",
    "SopInfraDetailView",
    "SopInfraRefreshView",
    "SopInfraRefreshNoForm",
    "SopInfraBulkEditView",
    "SopInfraBulkDeleteView",
    "SopInfraMerakiAddView",
    "SopInfraMerakiEditView",
    "SopInfraMerakiListView",
    "SopInfraPrismaAddView",
    "SopInfraPrismaEditView",
    "SopInfraSizingAddView",
    "SopInfraSizingEditView",
    "SopInfraSizingListView",
    "SopInfraClassificationAddView",
    "SopInfraClassificationEditView",
    "SopInfraClassificationListView",
)


@register_model_view(Site, name="infra")
class SopInfraTabView(View, ObjectPermissionRequiredMixin, SopInfraRelatedModelsMixin):
    """
    creates an "infrastructure" tab on the site page
    """

    tab = ViewTab(
        label=_("Infrastructure"), permission=get_permission_for_model(SopInfra, "view")
    )
    template_name: str = "sop_infra/tab/tab.html"
    queryset = SopInfra.objects.all()

    def get_extra_context(self, request, pk) -> dict:
        context: dict = {}

        site = get_object_or_404(Site, pk=pk)

        infra = SopInfra.objects.filter(site=site)

        if infra.exists():
            context["sop_infra"] = infra.first()
        else:
            context["sop_infra"] = SopInfra
        context["slave"], context["count_slave"] = self.get_slave_sites(infra)
        context["slave_infra"], context["count_slave_infra"] = self.get_slave_infra(
            infra
        )
        return {"object": site, "context": context}

    def get(self, request, pk):
        # additional permission security
        if not request.user.has_perm(get_permission_for_model(SopInfra, "view")):
            return self.handle_no_permission()
        return render(request, self.template_name, self.get_extra_context(request, pk))


# ____________________________
# SOP INFRA BASE MODEL VIEWS


class SopInfraDeleteView(generic.ObjectDeleteView):
    """
    deletes an existing SopInfra instance
    """

    queryset = SopInfra.objects.all()


class SopInfraEditView(generic.ObjectEditView):
    """
    edits an existing SopInfra instance
    """

    template_name: str = "sop_infra/tools/forms.html"
    queryset = SopInfra.objects.all()
    form = SopInfraForm

    def get_return_url(self, request, obj):
        if obj.site:
            return f"/dcim/sites/{obj.site.id}/infra"

    def get_extra_context(self, request, obj):
        context = super().get_extra_context(request, obj)
        if not obj:
            return context
        context["object_type"] = obj
        return context


class SopInfraAddView(generic.ObjectEditView):
    """
    adds a new SopInfra instance
    if the request is from the site page,
    -> the site id is passed as an argument (pk)
    """

    queryset = SopInfra.objects.all()
    form = SopInfraForm

    def get_object(self, **kwargs):
        """ """
        if "pk" in kwargs:
            site = get_object_or_404(Site, pk=kwargs["pk"])
            obj = self.queryset.model
            return obj(site=site)
        return super().get_object(**kwargs)

    def alter_object(self, obj, request, args, kwargs):
        """ """
        if "pk" in kwargs:
            site = get_object_or_404(Site, pk=kwargs["pk"])
            obj = self.queryset.model
            return obj(site=site)
        return super().alter_object(obj, request, args, kwargs)

    def get_return_url(self, request, obj):
        try:
            return f"/dcim/sites/{obj.site.id}/infra"
        except:
            return f"/plugins/sop_infra/list"


# ____________________________
# CLASSIFICATION ADD/EDIT


class SopInfraClassificationAddView(generic.ObjectEditView):
    """
    only adds classification objects in a SopInfra instance
    """

    template_name: str = "sop_infra/tools/forms.html"
    queryset = SopInfra.objects.all()
    form = SopInfraClassificationForm

    def get_object(self, **kwargs):
        """ """
        if "pk" in kwargs:
            site = get_object_or_404(Site, pk=kwargs["pk"])
            obj = self.queryset.model
            return obj(site=site)
        return super().get_object(**kwargs)

    def alter_object(self, obj, request, args, kwargs):
        """ """
        if "pk" in kwargs:
            site = get_object_or_404(Site, pk=kwargs["pk"])
            obj = self.queryset.model
            return obj(site=site)
        return super().alter_object(obj, request, args, kwargs)

    def get_return_url(self, request, obj):
        try:
            if obj.site:
                return f"/dcim/sites/{obj.site.id}/infra"
        except:
            return f"/plugins/sop_infra/class/list"

    def get_extra_context(self, request, obj) -> dict:
        context = super().get_extra_context(request, obj)
        context["object_type"] = "Classification"
        return context


class SopInfraClassificationEditView(generic.ObjectEditView):
    """
    only edits classification objects in a sopinfra instance
    """

    template_name: str = "sop_infra/tools/forms.html"
    queryset = SopInfra.objects.all()
    form = SopInfraClassificationForm

    def get_return_url(self, request, obj):
        if obj.site:
            return f"/dcim/sites/{obj.site.id}/infra"

    def get_extra_context(self, request, obj) -> dict:
        context = super().get_extra_context(request, obj)
        context["object_type"] = "Classification"
        if obj and obj.site:
            context["site"] = obj.site
        return context


# ____________________________
# MERAKI SDWAN ADD/EDIT


class SopInfraMerakiAddView(generic.ObjectEditView):
    """
    only adds meraki sdwan objects in a sopinfra instance
    """

    template_name: str = "sop_infra/tools/forms.html"
    queryset = SopInfra.objects.all()
    form = SopInfraMerakiForm

    def get_object(self, **kwargs):
        """ """
        if "pk" in kwargs:
            site = get_object_or_404(Site, pk=kwargs["pk"])
            obj = self.queryset.model
            return obj(site=site)
        return super().get_object(**kwargs)

    def alter_object(self, obj, request, args, kwargs):
        """ """
        if "pk" in kwargs:
            site = get_object_or_404(Site, pk=kwargs["pk"])
            obj = self.queryset.model
            return obj(site=site)
        return super().alter_object(obj, request, args, kwargs)

    def get_return_url(self, request, obj):
        try:
            if obj.site:
                return f"/dcim/sites/{obj.site.id}/infra"
        except:
            return f"/plugins/sop_infra/meraki/list"

    def get_extra_context(self, request, obj) -> dict:
        context = super().get_extra_context(request, obj)
        context["object_type"] = "Meraki SDWAN"
        return context


class SopInfraMerakiEditView(generic.ObjectEditView):
    """
    only edits meraki sdwan objects in a sopinfra instance
    """

    template_name: str = "sop_infra/tools/forms.html"
    queryset = SopInfra.objects.all()
    form = SopInfraMerakiForm

    def get_return_url(self, request, obj):
        if obj.site:
            return f"/dcim/sites/{obj.site.id}/infra"

    def get_extra_context(self, request, obj) -> dict:
        context = super().get_extra_context(request, obj)
        context["object_type"] = "Meraki SDWAN"
        if obj and obj.site:
            context["site"] = obj.site
        return context


# ____________________________
# SIZING ADD/EDIT


class SopInfraSizingAddView(generic.ObjectEditView):
    """
    only adds sizing objects in a sopinfra instance
    """

    template_name: str = "sop_infra/tools/forms.html"
    queryset = SopInfra.objects.all()
    form = SopInfraSizingForm

    def get_object(self, **kwargs):
        """ """
        if "pk" in kwargs:
            site = get_object_or_404(Site, pk=kwargs["pk"])
            obj = self.queryset.model
            return obj(site=site)
        return super().get_object(**kwargs)

    def alter_object(self, obj, request, args, kwargs):
        """ """
        if "pk" in kwargs:
            site = get_object_or_404(Site, pk=kwargs["pk"])
            obj = self.queryset.model
            return obj(site=site)
        return super().alter_object(obj, request, args, kwargs)

    def get_return_url(self, request, obj):
        try:
            if obj.site:
                return f"/dcim/sites/{obj.site.id}/infra"
        except:
            return f"/plugins/sop_infra/sizing/list"

    def get_extra_context(self, request, obj) -> dict:
        context = super().get_extra_context(request, obj)
        context["object_type"] = "Sizing"
        return context


class SopInfraSizingEditView(generic.ObjectEditView):
    """
    only edits sizing objects in a sopinfra instance
    """

    template_name: str = "sop_infra/tools/forms.html"
    queryset = SopInfra.objects.all()
    form = SopInfraSizingForm

    def get_return_url(self, request, obj):
        if obj.site:
            return f"/dcim/sites/{obj.site.id}/infra"

    def get_extra_context(self, request, obj) -> dict:
        context = super().get_extra_context(request, obj)
        context["object_type"] = "Sizing"
        if obj and obj.site:
            context["site"] = obj.site
        return context


# ____________________________
# DETAIL VIEW


class SopInfraDetailView(generic.ObjectView):
    """
    detail view with changelog and journal
    """

    queryset = SopInfra.objects.all()


# ____________________________
# LIST VIEWS


class SopInfraClassificationListView(generic.ObjectListView):
    """
    list view of all sopinfra - classification related instances
    """

    template_name: str = "sop_infra/tools/tables.html"
    queryset = SopInfra.objects.all()
    table = SopInfraClassificationTable
    filterset_form = SopInfraClassificationFilterForm
    filterset = SopInfraFilterset

    def get_extra_context(self, request) -> dict:
        """add context for title"""
        context = super().get_extra_context(request)
        context["title"] = "Classification"
        return context


class SopInfraSizingListView(generic.ObjectListView):
    """
    list view of all sopinfra - sizing related instances
    """

    template_name: str = "sop_infra/tools/tables.html"
    queryset = SopInfra.objects.all()
    table = SopInfraSizingTable
    filterset = SopInfraFilterset
    filterset_form = SopInfraSizingFilterForm

    def get_extra_context(self, request) -> dict:
        """add context for title"""
        context = super().get_extra_context(request)
        context["title"] = "Sizing"
        return context


class SopInfraMerakiListView(generic.ObjectListView):
    """
    list view of all sopinfra - meraki sdwan related instances
    """

    template_name: str = "sop_infra/tools/tables.html"
    queryset = SopInfra.objects.all()
    table = SopInfraMerakiTable
    filterset = SopInfraFilterset
    filterset_form = SopInfraMerakiFilterForm

    def get_extra_context(self, request) -> dict:
        """add context for title"""
        context = super().get_extra_context(request)
        context["title"] = "Meraki SDWAN"
        return context


class SopInfraListView(generic.ObjectListView):
    """list of all SopInfra objects and instances"""

    queryset = SopInfra.objects.all()
    table = SopInfraTable
    filterset = SopInfraFilterset
    filterset_form = SopInfraFilterForm


class SopInfraRefreshView(View, SopInfraRefreshMixin, ObjectPermissionRequiredMixin):
    """
    refresh targeted sopinfra computed values
    """

    form = SopInfraRefreshForm
    template_name: str = "sop_infra/tools/refresh_form.html"

    def get(self, request, *args, **kwargs):

        # additional security
        if not request.user.has_perm(get_permission_for_model(SopInfra, "change")):
            return self.handle_no_permission()

        restrict_form_fields(self.form(), request.user)

        return render(
            request,
            self.template_name,
            {
                "form": self.form(),
                "return_url": reverse("plugins:sop_infra:sizing_list"),
            },
        )

    def post(self, request, *args, **kwargs):

        # additional security
        if not request.user.has_perm(get_permission_for_model(SopInfra, "change")):
            return self.handle_no_permission()

        return_url = reverse("plugins:sop_infra:sizing_list")
        form = self.form(data=request.POST, files=request.FILES)
        if form.is_valid():
            data: dict = form.cleaned_data
            return_url = data["return_url"]
            self.refresh_infra(data["infra"])
            return redirect(return_url)

        return render(
            request, self.template_name, {"form": self.form(), "return_url": return_url}
        )


class SopInfraRefreshNoForm(View, SopInfraRefreshMixin, ObjectPermissionRequiredMixin):

    def get_return_url(self, pk) -> str:

        return f"/dcim/sites/{pk}/infra/"

    def get(self, request, *args, **kwargs):

        # additional security
        if not request.user.has_perm(get_permission_for_model(SopInfra, "change")):
            return self.handle_no_permission()

        pk = request.GET.get("qs")
        self.refresh_infra(SopInfra.objects.filter(site__pk=pk))
        return redirect(self.get_return_url(pk))


# ____________________________
# bulk views


class SopInfraBulkEditView(generic.BulkEditView):

    queryset = SopInfra.objects.all()
    form = SopInfraForm
    table = SopInfraTable
    filterset = SopInfraFilterset
    filterset_form = SopInfraFilterForm


class SopInfraBulkDeleteView(generic.BulkDeleteView):

    queryset = SopInfra.objects.all()
    table = SopInfraTable
    filterset = SopInfraFilterset
    filterset_form = SopInfraFilterForm


# ____________________________
# Infra Prisma views


class SopInfraPrismaAddView(generic.ObjectEditView):

    template_name: str = "sop_infra/tools/forms.html"
    queryset = SopInfra.objects.all()
    form = SopInfraPrismaForm

    def get_object(self, **kwargs):
        """ """
        if "pk" in kwargs:
            site = get_object_or_404(Site, pk=kwargs["pk"])
            obj = self.queryset.model
            return obj(site=site)
        return super().get_object(**kwargs)

    def alter_object(self, obj, request, args, kwargs):
        """ """
        if "pk" in kwargs:
            site = get_object_or_404(Site, pk=kwargs["pk"])
            obj = self.queryset.model
            return obj(site=site)
        return super().alter_object(obj, request, args, kwargs)

    def get_return_url(self, request, obj):
        try:
            if obj.site:
                return f"/dcim/sites/{obj.site.id}/infra"
        except:
            return f"/plugins/sop_infra/sop_infra/list"

    def get_extra_context(self, request, obj) -> dict:
        context = super().get_extra_context(request, obj)
        context["object_type"] = "Infra PRISMA"
        return context


class SopInfraPrismaEditView(generic.ObjectEditView):

    template_name: str = "sop_infra/tools/forms.html"
    queryset = SopInfra.objects.all()
    form = SopInfraPrismaForm

    def get_return_url(self, request, obj):
        if obj.site:
            return f"/dcim/sites/{obj.site.id}/infra"

    def get_extra_context(self, request, obj) -> dict:
        context = super().get_extra_context(request, obj)
        context["object_type"] = "Infra PRISMA"
        if obj and obj.site:
            context["site"] = obj.site
        return context
