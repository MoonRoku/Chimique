import g4f
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
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
            elif i == 6:
                js_code += f', "campo4": "{value}"'
                
        js_code += "},\n" if(j < len(data)-1) else "}\n"
    
    js_code += "]\n"
    return js_code

class IndexView(View):
    def get(self, request):
        produtos = Produto.objects.all()
        produtos_parser = python_to_javascript(list(produtos.values_list()))
        return render(request, 'index.html', {'produtos': produtos_parser })

    def post(self, request):
        pass

class SenhaView(View):
    def get(self, request):
        form = SenhaForm()
        return render(request, 'senha.html', {'form':form})
    def post(self, request):
        form = SenhaForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('usuario')
            senha = form.cleaned_data.get('senha')
            
            if(usuario == 'admin' and senha == 'admin'):
                administra = True
            else:
                administra = False
            
            request.session['ADM'] = administra
            if(administra == True):
                return redirect('lista')
        return render(request, 'senha.html', {'form':form, 'ADM':administra})
    
def get_suggestions(request):
    termo = request.GET.get('term', '')
    if termo:
        produtos = Produto.objects.filter(nome__icontains=termo)[:4]
        suggestions = [produto.nome for produto in produtos]
    else:
        suggestions = []
    return JsonResponse(suggestions, safe=False)
    
def pesquisar_produto(request):
    termo_pesquisa = request.GET.get('termo_pesquisa')

    if termo_pesquisa:
        produtos = Produto.objects.filter(nome__icontains=termo_pesquisa)
    else:
        produtos = Produto.objects.none()

    return render(request, 'resultado_pesquisa.html', {'produtos': produtos, 'termo_pesquisa': termo_pesquisa})

class registrar_produto(View):
    def get(self, request):
        if(request.session.get('ADM') == True):
            form = ProdutoForm
            return render(request, 'registrar_produto.html', {'form': form})
        else:
            return redirect('senha')
    def post(self, request):
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

        return render(request, 'registrar_produto.html', {'form': form})

class listaView(View):
    def get(self, request):
        if(request.session.get('ADM') == True):
            produtos = Produto.objects.all()
            return render(request, 'lista.html', {'produtos': produtos })
        else:
            return redirect('senha')
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
            
            sysprompt = f'Você é um especialista em química'
            sysprompt = f'Você responde em português'
            prompt = f"Qual a mistura dos compostos: {composto1}"

            try:
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_35_turbo,
                    messages=[
                        {"role": "system", "content": sysprompt},
                        {"role": "user", "content": prompt}
                    ]
                )
                
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