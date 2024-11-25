# SchoolSimilar

SchoolSimilar é um código criação de redes para análise 
de similaridades entre escolas do meio urbano e rural.

## Como funciona

1. Ao incluir arquivos .xlsx no diretório do código, é possível gerar redes
   associando Perfil, IDEB e  Subgrupo.
2. Ao executar o código, ele varrerá o diretório em busca de arquivos .xlsx.
   Estando esses no formato requerido para a análise,
   o algoritmo irá gerar as respectivas redes na pasta de Resultados.
3. Para visualização, recomendamos a aplicação ouestware.gitlab.io/retina/ 

## Como usar

### Python e Jupyter Lab

Para execução e visualização do código fonte será necessário ter instalado a linguagem Python (versão minima: 3.7), o gerenciador 
de bibliotecas Pip3 e o Jupyter Lab para visualização dos arquivos .ipynb

<details><summary><b>Instruções</b></summary>

1. Instale uma versão recente do Python para seu sistema operacional:

    ```sh
    https://www.python.org/downloads/
    ```
2. Instale uma versão recente do Pip3 para seu sistema operacional:

    ```sh
    https://pypi.org/project/pip/
    ```
3. Instale uma versão recente do Jupyter-Lab para seu sistema operacional:

    ```sh
    https://jupyter.org/install
    ```
3. Com tudo instalado, utilize o terminal para rodar os seguintes comandos:

    ```sh
    pip3 install pandas
    ```
    e
    ```sh
    pip3 install networkx
    ```
    
Agora, com seus arquivos .xlsx na pasta do projeto, abra o arquivo networkbuilder.ipynb e execute todas as celulas.

</details>

## Visualização

Com os arquivos de redes (.gexf) gerados na pasta Resultados, 
você poderá visualizar o formato da rede pela aplicação:
    ```
    ouestware.gitlab.io/retina/
    ```
