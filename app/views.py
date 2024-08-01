import g4f
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from config.settings import OPENAI_API_KEY
from .models import *
from .forms import *


def python_to_javascript(data):
    js_code = "["
    
    for j, tup in enumerate(data):
        js_code += "    {"
        for i, value in enumerate(tup):
            if i == 0:
                js_code += f'"id": {value}'
            elif i == 1:
                js_code += f', "nome": "{value}"'
            elif i == 2:
                js_code += f', "tipo": "{value}"'
            elif i == 3:
                js_code += f', "campo1": "{value}"'
            elif i == 4:
                js_code += f', "campo2": "{value}"'
            elif i == 5:
                js_code += f', "campo3": "{value}"'
                
        js_code += "},\n" if(j < len(data)-1) else "}\n"
    
    js_code += "]\n"
    return js_code

class IndexView(View):
    def get(self, request):
        produtos = Produto.objects.all()
        produtos_parser = python_to_javascript(list(produtos.values_list()))
        print(produtos_parser)
        return render(request, 'index.html', {'produtos': produtos_parser })

    def post(self, request):
        pass
    
def pesquisar_produto(request):
    termo_pesquisa = request.GET.get('termo_pesquisa')

    if termo_pesquisa:
        produtos = Produto.objects.filter(nome__icontains=termo_pesquisa)
    else:
        produtos = Produto.objects.none()

    return render(request, 'resultado_pesquisa.html', {'produtos': produtos, 'termo_pesquisa': termo_pesquisa})

def registrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            nome = form.cleaned_data.get('nome')
            
            produto_existente = Produto.objects.filter(nome=nome).first()
            
            if produto_existente:
                produto_existente.origem = form.cleaned_data.get('origem', produto_existente.origem)
                produto_existente.compostos = form.cleaned_data.get('compostos', produto_existente.compostos)
                produto_existente.categoria = form.cleaned_data.get('categoria', produto_existente.categoria)
                
                if 'imagem' in request.FILES:
                    produto_existente.imagem = request.FILES['imagem']
                
                produto_existente.save()
            else:
                form.save()
            
            return redirect('index')
    else:
        form = ProdutoForm()
    
    context = {
        'form': form,
    }
    return render(request, 'registrar_produto.html', context)

class listaView(View):
    def get(self, request):
        produtos = Produto.objects.all()
        return render(request, 'lista.html', {'produtos': produtos })
    
class deleteProduto(View):
    def get(self, request, id, *args, **kwargs):
        produtos = Produto.objects.get(id = id)
        produtos.delete()
        return redirect('lista')
    

def misturar_compostos(request):
    if request.method == 'POST':
        form = MixCompostosForm(request.POST)
        if form.is_valid():
            composto1 = form.cleaned_data['composto1']
            composto2 = form.cleaned_data['composto2']
            
            sysprompt = f"Você é um especialista em química // Você responde qual o resultado de misturas químicas // Você fala português // no final da resposta você informa o nome da mistura, origem e categoria"
            prompt = f"Qual a mistura dos compostos: {composto1} + {composto2}"

            try:
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_35_turbo,
                    messages=[
                        {"role": "system", "content": sysprompt},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                # Ajuste no acesso ao conteúdo da resposta
                resultado = response
            except Exception as e:
                resultado = f"Ocorreu um erro ao chamar a API: {e}"
            print(resultado)

            context = {
                'resultado': resultado,
                'form': form
            }

            return render(request, 'resultado_mistura.html', context)
    else:
        form = MixCompostosForm()

    return render(request, 'misturar_compostos.html', {'form': form})