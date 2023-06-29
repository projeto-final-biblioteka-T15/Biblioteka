# projeto-final

Introdução
O objetivo desse desafio é construir uma aplicação que faz a gestão de uma biblioteca.

Produto Mínimo Viável (MVP)
Diagrama de Entidade e Relacionamento Conceitual
https://live.staticflickr.com/65535/52922742543_51d2d9c6a3_o.png

Empréstimo de Livros

Cada livro só poderá ser emprestado por um período fixo de tempo. Se desejarem desenvolver algo mais complexo, deem uma olhada na seção Modo Hard.

Devolução de Livros

Todos os livros emprestados deverão ter uma data de retorno.
Deverá ser criada uma lógica onde, se a devolução cair em um fim de semana (sábado ou domingo), a data de retorno deverá ser modificada para ser no próximo dia útil.
Caso o estudante não devolva o livro até o prazo estipulado, deverá ser impedido (bloqueado) de solicitar outros empréstimos.

Bloqueio de Novos Empréstimos

Se um estudante não efetuar a devolução dos livros no prazo estipulado, ele não poderá emprestar mais livros até completar a devolução dos anteriores. Após completar as devoluções pendentes, o bloqueio deve permanecer por alguns dias.

Usuários

O sistema deve permitir o cadastro de usuários. Deve haver, no mínimo, 2 tipos de usuários:

- Estudante.
- Colaborador da biblioteca.

Deve ser possível também usuários não autenticados acessarem a plataforma para visualizar informações sobre os livros, como disponibilidade, título, etc.

Funcionalidades permitidas aos estudantes:

De maneira geral, ao acessar a plataforma, um estudante pode:

Ver seu próprio histórico de livros emprestados.
Obter informações sobre livros.

"Seguir" um livro a fim de receber notificações no email conforme a disponibilidade/status do livro.

Funcionalidades permitidas aos colaboradores:
De maneira geral, ao acessar a plataforma, um colaborador pode:

- Cadastrar novos livros.
- Emprestar livros.
- Verificar o histórico de empréstimo de cada estudante.
- Verificar status do estudante (se está bloqueado não pode emprestar uma nova cópia durante determinado tempo).
- Extras
- Sistema de avaliações de livros
- Feed com livros recentes adicionados à biblioteca.

Front end responsivo.

Além de receber mensagens sobre livros que estão sendo "seguidos", o usuário também deverá receber mensagens de cobrança, caso algum livro não tenha sido devolvido no prazo estipulado.

Adicionar multa de devolução tardia do livro.

Adicionar envio de lembrete um dia antes de chegar na data máxima do prazo de devolução.

Modo Hard

Implementar uma regra de negócio que regula o tempo máximo de empréstimo de um determinado cópia. Por exemplo, se um livro tem muitos seguidores, ele só poderá ser emprestado por um período menor.

Adaptar o sistema de maneira que ele possa ser utilizado por várias bibliotecas, simultaneamente. 🏛️
