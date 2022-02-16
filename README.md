# Data Gathering & Visualization Project 4:



### Perfil eleitoreiro Brasileiro atual

###		Objetivo:

##### 				Parte 1

​					Extrair, Tratar e Armazenar os dados que estão hospedados na [API](https://dadosabertos.tse.jus.br/dataset/) do [TSE (Tribunal Superior Eleitoral)](https://www.tse.jus.br/) . 

##### 				Parte 2

​					Foi feito consulta e separação (em SQL) dos dados a serem utilizados para a criação da visualização com gráficos.



## 	A Pipeline: parte 1

##### Extração

​	Contendo uma imensidão de dados eleitoreiros, se é possível obter até mesmo resultados de eleições históricas (existem arquivos '.csv'  com os registros desde 1933). Com o objetivo de adquirir o maior volume de dados possível, comecei o trabalho para montar a pipeline em python, criando classes para cada tipo de informação. 

​	Começando pelos dados do eleitorado nacional foram requisições e mapeamento do html para obtenção das urls dos arquivos a serem baixados.

​	Após fazer a raspagem, o download (de arquivos .zips) e a extração dos csvs percebi que não seria tão simples. O volume de dados de 1994 a 2022 se mostrou relativamente grande, precisando de mais de 100gb para seu armazenamento.

​	Percebendo o quando doloroso seria para processar esse volume de dados, foi preciso mudar o foco para apenas os dias atuais. 

##### Tratamento e Carregamento

​	Com os dados relativamente limpos, foram preciso poucas alterações antes do carregamento para o banco de dados. 

​	Foi feita a retirada de colunas que não continham dados que pudessem vir a ser interessante e a mudança de nomes das colunas( por alguma razão com os nomes dos csvs o sql da erro e não consegue efetuar consultas de maneira simples e adequada).



##### Versão

​	Por conta do deadline o programa se mantêm em um estágio simples, com apenas o necessário para esse projeto. Futuramente atualizações serão feitas para melhoramento de segurança, otimização de desempenho e mais importante abrangência do conteúdo consultado.





## A Visualização: parte 2

#### Primeiro contato:	

​	Primeiramente percebi que as tabelas não continham de maneira individual cada perfil, mas agrupamentos de pessoas por determinadas características: Local(colégio eleitoral, zona, cidade e estado), faixa etária, sexo , estado civil.

​	Por conta desse agrupamento e provavelmente para o anonimato  dos eleitores, os dados se tornam em geral rasos e sem muita relevância individual.

 	Para uma analise mais profunda, por estar no inicio do ano eleitoral, se faz necessário o acompanhamento dos dados e o cruzamento com informações  

​	





 

