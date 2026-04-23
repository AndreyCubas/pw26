from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Meta, Saldo


class SaldoViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="teste",
            password="senha123forte",
        )
        self.client.force_login(self.user)

    def test_cria_saldo_para_usuario_logado(self):
        response = self.client.post(reverse("saldo_novo"), {"valor": "1500.50"})

        self.assertRedirects(response, reverse("saldo"))
        saldo = Saldo.objects.get(usuario=self.user)
        self.assertEqual(saldo.valor, Decimal("1500.50"))

    def test_exibe_saldo_cadastrado_na_pagina(self):
        Saldo.objects.create(usuario=self.user, valor=Decimal("2500.00"))

        response = self.client.get(reverse("saldo"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2.500,00")


class MetaAdicionarValorViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="meta_user",
            password="senha123forte",
        )
        self.client.force_login(self.user)
        self.meta = Meta.objects.create(
            usuario=self.user,
            titulo="Reserva de emergencia",
            valor_alvo=Decimal("5000.00"),
            valor_atual=Decimal("1000.00"),
            prazo="2026-12-31",
        )

    def test_adiciona_valor_sem_editar_meta_completa(self):
        response = self.client.post(
            reverse("meta_adicionar_valor", args=[self.meta.pk]),
            {"valor_adicional": "250.50"},
        )

        self.assertRedirects(response, reverse("metas"))
        self.meta.refresh_from_db()
        self.assertEqual(self.meta.valor_atual, Decimal("1250.50"))
