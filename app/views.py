from django.shortcuts import render
from django.views import View
from .models import *

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

