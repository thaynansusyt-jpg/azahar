# Azahar Lite — primeira versão experimental

Fork independente, criado com assistência de IA a pedido do mantenedor deste fork.
Não é uma versão oficial do Azahar ou do Azahar Plus. Preserva a licença GPL e os
créditos originais. Alterações deste fork não são propostas ao projeto original.

## O que esta versão implementa

- Aplicativo Android ARM64 com ID próprio `io.github.thaynansusyt.azaharlite`.
- Recomendações na aba de configurações: informações do aparelho, RAM física e
  disponível, alerta de pouca memória e aplicação explícita de um perfil conservador.
- Perfil: resolução 1×, 3D desligado, filtro e texturas personalizadas desligados,
  sem pré-carregar/dumpar texturas; JIT, shaders de hardware e cache de disco ligados.
  É um ponto de partida para aparelhos de até 4 GB, sem benchmark automático.
  CPU, API gráfica, precisão de shaders e configurações por jogo são preservados.
- Backup da configuração antes da primeira aplicação; restaurar repõe o arquivo
  inteiro, inclusive alterações feitas depois. O backup está associado à pasta usada.
- Resolução interna digitável de 1 a 3 em multiplicadores inteiros;
  1× é 400×240 superior e 320×240 inferior. O núcleo usa escala inteira: 0,5× ou
  dimensões arbitrárias exigem trabalho adicional no renderizador e não estão implementados.
- `.3ds` já é reconhecido no fork recebido, tanto no Android quanto no carregador.
  Não é necessário converter a extensão para `.cci`. Arquivos criptografados continuam
  sujeitos às limitações do núcleo: aceitar a extensão não adiciona descriptografia.
- Workflow Android gera APK de teste em Actions, sem publicar uma release automaticamente.
  Sem chave de release configurada, usa a assinatura de teste existente no projeto;
  guarde uma chave estável antes de distribuir atualizações públicas.
- Verificador de atualizações aponta para este fork.

## Gerar e instalar

Abra Actions → Azahar Lite Android → selecione a branch `azahar-lite` → Run workflow.
Ao terminar, baixe `Azahar-Lite-arm64-test` e extraia o APK. O pacote separado permite
instalar ao lado do Azahar. Selecione uma pasta de usuário própria para testes.

## Roteiro no celular

Compare a mesma versão-base e este fork, no mesmo aparelho, com o mesmo save,
mesmo backend e resolução 1×. Faça 5 minutos de aquecimento e 10 minutos de medição.
Anote velocidade de emulação (100% como objetivo), FPS, tempo de quadro, RAM,
temperatura, falhas gráficas, áudio e travamentos. Compare a primeira execução
compilando shaders e a segunda com cache aquecido separadamente. Jogos com alvo
30 FPS não devem ser avaliados como se precisassem atingir 60 FPS.

| Jogo | Cenário repetível | Resultado |
| --- | --- | --- |
| Pokémon X/Y e OR/AS (cada título separadamente) | Mesma cidade, rota e batalha | Pendente no aparelho |
| New Super Mario Bros. 2 | Mesma fase por 10 minutos | Pendente no aparelho |
| Super Mario 3D Land | Mesma fase, movimentos e câmera | Pendente no aparelho |
| Super Mario Maker for Nintendo 3DS | Mesma fase e editor | Pendente no aparelho |
| Super Smash Bros. for Nintendo 3DS | Mesmo cenário, lutadores e regras | Pendente no aparelho |

Não há ROMs incluídas, resultados de desempenho medidos, garantia de ganho de FPS,
ou otimizações profundas do núcleo nesta primeira etapa. A redução do APK para uma
arquitetura não reduz por si só a RAM usada durante a emulação.

## Menu simplificado

O Lite remove opções de VR, estereoscopia, filtros de aprimoramento e pacotes/dump
de texturas do menu gráfico. Também retira o submenu de depuração. Vulkan/OpenGL,
shaders assíncronos, precisão, cache de shaders e controles/layout/áudio permanecem.
A resolução passa a 1×–3×; 1× é recomendado. O carregador Android desativa os
recursos pesados mesmo em INIs importados e limita a resolução a essa faixa.
Não há medições de desempenho concluídas.
