HELPER_MESSAGE_PT1 = '''```diff
- SELECTION_HELPER
AJUDA DE SELEÇÕES
```
**O que são seleções?** Para o gapigo seleções são esses quadradinhos do discord onde é possível colocar cores, mas como isso é um saco fazer manualmente, o gapigo criou esse "programa" no bot dele para ajudar a formatar seleções. Para fazer isso, existe 5 opções válidas: **seleção básica, criar seleção, deletar seleção, modificar seleção e pegar seleção salva**

**seleção básica**
cores disponíveis: ['y', 'o', 'l', 'r', 'b', 'g']
(yellow, orange, light green, red, blue, green)
*$sel -[cor] mensagem*
ou
*$sel -[cor] mensagem -b corpo*
exemplo:
$sel -l mensagem -b corpo
```diff
+ Mensagem
Corpo
```

**criar seleção**
para salvar uma seleção e depois pegá-la no **pegar seleção salva**

*$sel --new [paramêtros]*

__parâmetros obrigatórios de configuração__
-n nome
||define um nome para a salvar a seleção||
-c [cor] (cores disponíveis: ['y', 'o', 'l', 'r', 'b', 'g'])
||define uma cor para seleção||

__parâmetros obrigatórios de conteúdo__
-m mensagem
||define uma mensagem rápida para seleção||
-t title -b body
||define um título colorido com um corpo (body) não colorido para seleção||

(OBS: ou você usa mensagem, ou você usa title/body, caso tenha os dois dará erro. Se você for usar -t é obrigatório especificar um body (corpo, ou conteúdo não colorido) com -b)

__parâmetros opcionais de configuração__
-p
||De 'private'. Define se a mensagem salva será privada. Se for, apenas o usuário que a criou pode modificá-la e usá-la.||
-d
||De 'delete'. Define se o bot deletará a última mensagem quando for mandar a seleção, ou seja, a mensagem que você usou para chamá-lo.||
(OBS: parâmetros opcionais de configuração são usados sozinhos, já que eles definem variáveis booleanas de True ou False)

Exemplos:
$sel --new -c o -m Mensagem exemplo -n laranja -p -d
```css
[ Mensagem exemplo ]
```

$sel --new -d -p -c r -t Titulo da mensagem -b Corpo da mensagem -n titulo_vermelho
```diff
- Titulo da mensagem
Corpo da mensagem
```
'''
HELPER_MESSAGE_PT2 = '''
**deletar seleção**
para apagar uma seleção salva (é necessário ter acesso àquela seleção caso ela seja privada)

$sel --del nome_selecao

**modificar seleção**
para modificar uma seleção existente
usa os mesmos parâmetros do **criar seleção**

*$sel --mod [paramêtros]*

**pegar seleção salva**
para pegar uma seleção salva

*$sel nome_selecao_salva*

'''