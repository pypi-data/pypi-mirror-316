from django.urls import reverse

from utilities.testing import TestCase
from dcim.models import Site

from sop_infra.models import *


__all__ = (
    "SopInfraAPITestCase",
    "PrismaEndpointAPITestCase",
)


class InfraAPITestCaseMixin:

    user_permissions = ()
    model = None
    VIEW_PERM = None

    def get_action_url(self, action, instance=None):
        """reverse plugin api url with action"""
        url = f"plugins-api:sop_infra-api:{self.model._meta.model_name}-{action}"

        if instance is None:
            return reverse(url)

        return reverse(url, kwargs={"pk": instance.pk})

    def test_detail_no_perm(self):
        """get api object no perm"""
        instance = self.model.objects.first()
        url = self.get_action_url("detail", instance)

        response = self.client.get(url)
        self.assertHttpStatus(response, 403)

    def test_detail_perm(self):
        """get api object perm"""
        instance = self.model.objects.first()
        url = self.get_action_url("detail", instance)

        self.add_permissions(self.VIEW_PERM)
        response = self.client.get(url)
        self.assertHttpStatus(response, 200)

    def test_list_no_perm(self):
        """get api list no perm"""
        url = self.get_action_url("list")

        response = self.client.get(url)
        self.assertHttpStatus(response, 403)

    def test_list_perm(self):
        """get api list perm"""
        url = self.get_action_url("list")

        self.add_permissions(self.VIEW_PERM)
        response = self.client.get(url)
        self.assertHttpStatus(response, 200)
        self.assertEqual(len(response.data["results"]), 2)


class SopInfraAPITestCase(TestCase, InfraAPITestCaseMixin):

    model = SopInfra
    VIEW_PERM = "sop_infra.view_sopinfra"

    @classmethod
    def setUpTestData(cls):

        sites = (
            Site(name="site 1", slug="site-1", status="active"),
            Site(name="site 2", slug="site-2", status="retired"),
        )
        for site in sites:
            site.full_clean()
            site.save()


class PrismaEndpointAPITestCase(TestCase, InfraAPITestCaseMixin):

    model = PrismaEndpoint
    VIEW_PERM = "sop_infra.view_prismaendpoint"

    @classmethod
    def setUpTestData(cls):

        prisma = (
            PrismaEndpoint(name="salut", slug="salut"),
            PrismaEndpoint(name="salut2", slug="salut2"),
        )
        for prism in prisma:
            prism.full_clean()
            prism.save()
