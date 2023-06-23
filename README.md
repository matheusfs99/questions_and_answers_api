# Plataforma de perguntas e respostas:
## API para uma plataforma de perguntas e respostas, onde os usuários pode fazer perguntas, responder a perguntas e votar nas melhores respostas. 
## Implemente recursos como sistema de pontuação e pesquisa avançada.

######################################################################

### Escopo:
 - uma atividade é possível inserir várias perguntas
 - cada pergunta pode ter várias respostas, mas apenas 1 correta
 
### Como deve funcionar:
 - um usuário professor pode criar a atividade com as perguntas e respostas
 - a atividade pode ser gerada para vários usuários aluno
 - cada usuário aluno terá a atividade relacionada ao seu id
 - as respostas da atividade de cada aluno é relacionada ao id da atividade do aluno e é salva

### Extras:
 - as questões e suas respostas estarão destribuidas de forma randomica para cada aluno
 - ao finalizar a atividade, já é gerada a nota do aluno