from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'origem', 'imagem', 'compostos', 'categoria']
        
    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class': 'texto'})
        self.fields['origem'].widget.attrs.update({'class': 'texto'})
        self.fields['imagem'].widget.attrs.update({'class': 'texto'})
        self.fields['compostos'].widget.attrs.update({'class': 'texto'})
        self.fields['categoria'].widget.attrs.update({'class': 'texto'})

class MixCompostosForm(forms.Form):
    composto1 = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'class': 'texto', 'rows': 4, 'cols': 40})
    )