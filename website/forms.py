from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Gasto, MensagemContato, Meta, Saldo


class ISODateInput(forms.DateInput):
    input_type = "date"


class BaseStyledFormMixin:
    input_class = "form-control"

    def apply_bootstrap(self):
        for field in self.fields.values():
            widget = field.widget
            existing = widget.attrs.get("class", "")
            css_class = self.input_class

            if isinstance(widget, forms.CheckboxInput):
                css_class = "form-check-input"
            elif isinstance(widget, forms.Select):
                css_class = "form-select"

            widget.attrs["class"] = f"{existing} {css_class}".strip()
            widget.attrs.setdefault("placeholder", field.label)


class LoginForm(BaseStyledFormMixin, AuthenticationForm):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()


class CadastroForm(BaseStyledFormMixin, UserCreationForm):
    first_name = forms.CharField(label="Nome", max_length=150)
    last_name = forms.CharField(label="Sobrenome", max_length=150, required=False)
    email = forms.EmailField(label="E-mail")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Usuario"
        self.fields["password1"].label = "Senha"
        self.fields["password2"].label = "Confirmacao da senha"
        self.apply_bootstrap()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ContatoForm(BaseStyledFormMixin, forms.ModelForm):
    class Meta:
        model = MensagemContato
        fields = ("nome", "email", "assunto", "mensagem")
        widgets = {
            "mensagem": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()


class GastoForm(BaseStyledFormMixin, forms.ModelForm):
    data = forms.DateField(
        label="Data",
        input_formats=["%Y-%m-%d"],
        widget=ISODateInput(format="%Y-%m-%d"),
    )

    class Meta:
        model = Gasto
        fields = ("titulo", "categoria", "valor", "data", "recorrente", "observacao")
        widgets = {
            "observacao": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()


class MetaFinanceiraForm(BaseStyledFormMixin, forms.ModelForm):
    prazo = forms.DateField(
        label="Prazo",
        input_formats=["%Y-%m-%d"],
        widget=ISODateInput(format="%Y-%m-%d"),
    )

    class Meta:
        model = Meta
        fields = ("titulo", "descricao", "valor_alvo", "valor_atual", "prazo")
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()


class MetaAdicionarValorForm(BaseStyledFormMixin, forms.Form):
    valor_adicional = forms.DecimalField(
        label="Valor a adicionar",
        min_value=0.01,
        decimal_places=2,
        max_digits=10,
        widget=forms.NumberInput(attrs={"step": "0.01", "min": "0.01"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()


class SaldoForm(BaseStyledFormMixin, forms.ModelForm):
    valor = forms.DecimalField(
        label="Saldo atual",
        min_value=0,
        decimal_places=2,
        max_digits=12,
        widget=forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
    )

    class Meta:
        model = Saldo
        fields = ("valor",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()


class RelatorioFiltroForm(BaseStyledFormMixin, forms.Form):
    periodo = forms.ChoiceField(
        label="Periodo",
        choices=(
            ("30", "Ultimos 30 dias"),
            ("90", "Ultimos 90 dias"),
            ("180", "Ultimos 6 meses"),
        ),
    )
    categoria = forms.ChoiceField(
        label="Categoria",
        required=False,
        choices=(
            ("", "Todas as categorias"),
            *Gasto.Categoria.choices,
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
