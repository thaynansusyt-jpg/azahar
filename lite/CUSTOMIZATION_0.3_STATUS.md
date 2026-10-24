# Azahar Lite 0.3 — desenvolvimento, não release

Base recuperada: branch azahar-lite-apk02, commit b09d66caa8e5b9cd9c79585d5af46bdbf47712a9. Backup local azahar-lite-02-backup; branch anterior não alterada.

## Primeira implementação

Menu da emulação → opções dos controles → Opacidade por controle. Abrange A/B/X/Y, L/R/ZL/ZR, START/SELECT, D-Pad, Circle Pad, C-Stick, HOME, troca de telas, Turbo e Combo. Cada controle tem preferência persistente própria. Sem preferência própria herda a opacidade global existente. A prévia usa o refresh do overlay original; o caminho de leitura dos novos valores só roda ao reconstruir os controles, não em cada evento de toque. A transparência não muda a área de toque.

OK confirma. Cancelar, voltar ou tocar fora restaura a preferência anterior, inclusive a ausência de override. “Usar opacidade geral” remove somente o override selecionado. Os ajustes globais e o tamanho/movimento existentes foram conservados. Nenhum arquivo de save, loader, backend ou shader foi alterado.

## Validação executada

Parsing XML dos recursos Lite e menu: passou. git diff --check: passou. Revisão de correspondência dos IDs de controles e dos três inicializadores do overlay: feita. Não houve compilação Kotlin/Android, instalação, teste multitoque ou execução no A15/Smash. Essas verificações ainda são obrigatórias antes de distribuir um APK.

O ambiente anterior foi reiniciado; SDK/NDK, submódulos materializados, APK e chave da sessão anterior não estavam no diretório local recuperado. Isso não comprova falha da compilação 0.2: seu resultado final permanece não verificado nesta continuação.

## Ainda não implementado nesta etapa

Editor novo com salvar/cancelar, grid, undo/redo e limites; perfis nomeados/por jogo e importação/exportação; cores/estilos individuais; sistema de temas/skins; imagens/logotipos; transições configuráveis e personalização da biblioteca. As funções existentes no upstream não devem ser anunciadas como implementação nova completa desses requisitos.

Esta branch é uma etapa parcial de desenvolvimento. Não é uma entrega concluída da 0.3 e não há APK 0.3 verificado. Não desinstale sua versão atual nem altere sua pasta de saves para testar código não compilado.
