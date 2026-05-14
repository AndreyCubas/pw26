from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView

from .forms import (
    CadastroForm,
    ContatoForm,
    DELETE_GASTO,
    DELETE_META,
    DELETE_SALDO,
    DeleteShellContextMixin,
    FormShellContextMixin,
    GastoForm,
    LoginForm,
    MetaAdicionarValorForm,
    MetaFinanceiraForm,
    RelatorioFiltroForm,
    SaldoForm,
    SHELL_CADASTRO,
    SHELL_CONTATO,
    SHELL_GASTO_CREATE,
    SHELL_GASTO_UPDATE,
    SHELL_LOGIN,
    SHELL_META_ADD_VALOR,
    SHELL_META_CREATE,
    SHELL_META_UPDATE,
    SHELL_SALDO_CREATE,
    SHELL_SALDO_UPDATE,
    TEMPLATE_CONFIRM_DELETE,
    TEMPLATE_FORM_SHELL,
)
from .models import Gasto, Meta, Saldo
from .services import build_dashboard_context


class AuthPageMixin(LoginRequiredMixin):
    login_url = reverse_lazy("login")


class BasePageMixin:
    page_title = "Painel financeiro"
    page_subtitle = "Acompanhe indicadores, metas e gastos em um unico fluxo."
    show_sidebar = True
    # Quando show_sidebar é False, o modelo usa .auth-wrapper (max-width 560px) para login/cadastro.
    # Landing pages devem definir True para ocupar a largura do painel.
    skip_auth_wrapper = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("page_title", self.page_title)
        context.setdefault("page_subtitle", self.page_subtitle)
        context.setdefault("show_sidebar", self.show_sidebar)
        context.setdefault("skip_auth_wrapper", self.skip_auth_wrapper)
        return context


class DashboardView(AuthPageMixin, BasePageMixin, TemplateView):
    template_name = "website/dashboard.html"
    page_title = "Dashboard"
    page_subtitle = "Visao geral da sua saude financeira com cards, tabela e graficos."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(build_dashboard_context(self.request.user))
        return context


class GastosView(AuthPageMixin, BasePageMixin, ListView):
    model = Gasto
    template_name = "website/gastos.html"
    context_object_name = "gastos"
    page_title = "Gastos"
    page_subtitle = "Tabela com os principais lancamentos e distribuicao por categoria."

    def get_queryset(self):
        return Gasto.objects.filter(usuario=self.request.user).order_by("-data", "-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dashboard_ctx = build_dashboard_context(self.request.user)
        dashboard_ctx.pop("gastos", None)
        context.update(dashboard_ctx)
        context["gastos"] = context["object_list"]
        return context


class MetasView(AuthPageMixin, BasePageMixin, TemplateView):
    template_name = "website/metas.html"
    page_title = "Metas"
    page_subtitle = "Metas financeiras com progresso, prazo e valor restante."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(build_dashboard_context(self.request.user))
        return context


class RelatoriosView(AuthPageMixin, BasePageMixin, FormView):
    template_name = "website/relatorios.html"
    form_class = RelatorioFiltroForm
    success_url = reverse_lazy("relatorios")
    page_title = "Relatorios"
    page_subtitle = "Filtros, indicadores e comparativos para apoiar suas decisoes."

    def get_initial(self):
        return {"periodo": "90", "categoria": ""}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "GET" and self.request.GET:
            initial = self.get_initial()
            data = self.request.GET.copy()
            if "periodo" not in data:
                data["periodo"] = initial.get("periodo", "90")
            if "categoria" not in data:
                data["categoria"] = initial.get("categoria", "")
            kwargs["data"] = data
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        initial = self.get_initial()
        periodo_dias = int(initial.get("periodo", "90"))
        categoria = initial.get("categoria") or None
        if categoria == "":
            categoria = None

        if form.is_bound and form.is_valid():
            periodo_dias = int(form.cleaned_data["periodo"])
            categoria = form.cleaned_data.get("categoria") or None
            if categoria == "":
                categoria = None

        context.update(
            build_dashboard_context(
                self.request.user,
                periodo_dias=periodo_dias,
                categoria=categoria,
            )
        )
        return context


class RecursosView(AuthPageMixin, BasePageMixin, TemplateView):
    template_name = "website/recursos.html"
    page_title = "Recursos"
    page_subtitle = "Biblioteca de funcionalidades inspirada nos componentes do diagrama."


class SobreView(BasePageMixin, TemplateView):
    template_name = "website/sobre.html"
    page_title = "Arquitetura da plataforma"
    page_subtitle = "Resumo de como os modulos Django foram organizados a partir do diagrama."


class ContatoView(FormShellContextMixin, BasePageMixin, FormView):
    template_name = TEMPLATE_FORM_SHELL
    form_class = ContatoForm
    form_shell_config = SHELL_CONTATO
    success_url = reverse_lazy("contato")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Mensagem enviada com sucesso.")
        return super().form_valid(form)


class UsuarioLoginView(FormShellContextMixin, BasePageMixin, DjangoLoginView):
    template_name = TEMPLATE_FORM_SHELL
    form_class = LoginForm
    form_shell_config = SHELL_LOGIN
    redirect_authenticated_user = True
    show_sidebar = False


class CadastroView(FormShellContextMixin, BasePageMixin, FormView):
    template_name = TEMPLATE_FORM_SHELL
    form_class = CadastroForm
    form_shell_config = SHELL_CADASTRO
    success_url = reverse_lazy("dashboard")
    show_sidebar = False

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Conta criada com sucesso.")
        return super().form_valid(form)


class UsuarioLogoutView(DjangoLogoutView):
    next_page = reverse_lazy("login")


class GastoUserMixin(AuthPageMixin):
    model = Gasto

    def get_queryset(self):
        return Gasto.objects.filter(usuario=self.request.user)


class GastoCreateView(FormShellContextMixin, AuthPageMixin, BasePageMixin, CreateView):
    model = Gasto
    form_class = GastoForm
    template_name = TEMPLATE_FORM_SHELL
    form_shell_config = SHELL_GASTO_CREATE

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Gasto registrado com sucesso.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("gastos")


class GastoUpdateView(FormShellContextMixin, GastoUserMixin, BasePageMixin, UpdateView):
    form_class = GastoForm
    template_name = TEMPLATE_FORM_SHELL
    form_shell_config = SHELL_GASTO_UPDATE

    def form_valid(self, form):
        messages.success(self.request, "Gasto atualizado com sucesso.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("gastos")


class GastoDeleteView(DeleteShellContextMixin, GastoUserMixin, BasePageMixin, DeleteView):
    template_name = TEMPLATE_CONFIRM_DELETE
    delete_shell_config = DELETE_GASTO
    context_object_name = "gasto"
    success_url = reverse_lazy("gastos")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Gasto excluido com sucesso.")
        return super().delete(request, *args, **kwargs)


class GastoDetailView(GastoUserMixin, BasePageMixin, DetailView):
    template_name = "website/gasto_detail.html"
    context_object_name = "gasto"
    page_title = "Detalhe do gasto"
    page_subtitle = "Consulte os dados deste lancamento."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        g = self.object
        context["page_title"] = g.titulo
        context["page_subtitle"] = f"{g.get_categoria_display()} · {g.data.strftime('%d/%m/%Y')}"
        return context


class MetaUserMixin(AuthPageMixin):
    model = Meta

    def get_queryset(self):
        return Meta.objects.filter(usuario=self.request.user)


class MetaCreateView(FormShellContextMixin, AuthPageMixin, BasePageMixin, CreateView):
    model = Meta
    form_class = MetaFinanceiraForm
    template_name = TEMPLATE_FORM_SHELL
    form_shell_config = SHELL_META_CREATE

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Meta criada com sucesso.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("metas")


class MetaUpdateView(FormShellContextMixin, MetaUserMixin, BasePageMixin, UpdateView):
    form_class = MetaFinanceiraForm
    template_name = TEMPLATE_FORM_SHELL
    form_shell_config = SHELL_META_UPDATE

    def form_valid(self, form):
        messages.success(self.request, "Meta atualizada com sucesso.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("metas")


class MetaAdicionarValorView(FormShellContextMixin, MetaUserMixin, BasePageMixin, SingleObjectMixin, FormView):
    form_class = MetaAdicionarValorForm
    template_name = TEMPLATE_FORM_SHELL
    form_shell_config = SHELL_META_ADD_VALOR
    context_object_name = "meta"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta"] = self.object
        return context

    def form_valid(self, form):
        self.object.valor_atual += form.cleaned_data["valor_adicional"]
        self.object.save(update_fields=["valor_atual", "updated_at"])
        messages.success(self.request, "Valor adicionado a meta com sucesso.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("metas")


class MetaDeleteView(DeleteShellContextMixin, MetaUserMixin, BasePageMixin, DeleteView):
    template_name = TEMPLATE_CONFIRM_DELETE
    delete_shell_config = DELETE_META
    context_object_name = "meta"
    success_url = reverse_lazy("metas")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Meta excluida com sucesso.")
        return super().delete(request, *args, **kwargs)


class SaldoUserMixin(AuthPageMixin):
    model = Saldo

    def get_queryset(self):
        return Saldo.objects.filter(usuario=self.request.user)


class SaldoView(AuthPageMixin, BasePageMixin, TemplateView):
    template_name = "website/saldo.html"
    page_title = "Saldo"
    page_subtitle = "Cadastre e acompanhe o saldo atual disponivel na sua conta."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["saldo"] = Saldo.objects.filter(usuario=self.request.user).first()
        return context


class SaldoCreateView(FormShellContextMixin, AuthPageMixin, BasePageMixin, CreateView):
    model = Saldo
    form_class = SaldoForm
    template_name = TEMPLATE_FORM_SHELL
    form_shell_config = SHELL_SALDO_CREATE

    def dispatch(self, request, *args, **kwargs):
        if Saldo.objects.filter(usuario=request.user).exists():
            messages.info(request, "Voce ja possui um saldo cadastrado.")
            return redirect("saldo")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Saldo cadastrado com sucesso.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("saldo")


class SaldoUpdateView(FormShellContextMixin, SaldoUserMixin, BasePageMixin, UpdateView):
    form_class = SaldoForm
    template_name = TEMPLATE_FORM_SHELL
    form_shell_config = SHELL_SALDO_UPDATE

    def form_valid(self, form):
        messages.success(self.request, "Saldo atualizado com sucesso.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("saldo")


class SaldoDeleteView(DeleteShellContextMixin, SaldoUserMixin, BasePageMixin, DeleteView):
    template_name = TEMPLATE_CONFIRM_DELETE
    delete_shell_config = DELETE_SALDO
    context_object_name = "saldo"
    success_url = reverse_lazy("saldo")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Saldo excluido com sucesso.")
        return super().delete(request, *args, **kwargs)


class InicioView(BasePageMixin, TemplateView):
    template_name = "website/inicio.html"
    page_title = "Início"
    page_subtitle = ""
    show_sidebar = False
    skip_auth_wrapper = True
