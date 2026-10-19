# Teste controlado no Galaxy A15 — Smash Bros. 3DS

Não houve teste com ROM comercial ou telefone nesta entrega. Este procedimento permite investigar a causa sem atribuir tudo a shaders. Use somente seu jogo legalmente obtido e saves normais. Não compartilhe ROM, chaves ou saves que contenham dados pessoais.

## Antes de atualizar

Feche o Lite normalmente. Copie sua pasta de dados inteira (incluindo `sdmc`, `nand`, `config`, `states`, caches e `log`) para um backup externo à pasta usada pelo app. A pasta fica no local escolhido na configuração inicial. Não selecione nem altere a pasta do Azahar oficial. Não desinstale o Lite: instale o APK 0.2 sobre o 0.1. Mesmo pacote e certificado permitem atualização preservando dados; a interface não migra nem apaga saves. Prefira saves internos do jogo; save states podem depender da versão do núcleo. Nunca apague saves como tentativa de otimização.

## Condições constantes

Registre modelo/Android, RAM detectada no app/log, backend e versão do driver, versão/update do jogo, resolução 1×, velocidade 100%, CPU emulada 100%, mesmo save e cenário, brilho, taxa da tela, nível de bateria, temperatura inicial e se está carregando. Não carregue durante a comparação se isso mudar o aquecimento. Mantenha filtros pesados desligados e as demais opções iguais. Não force 60 FPS em cenas/jogos de 30. A tela de 90 Hz não muda a frequência nativa do jogo.

Use sessões de 120 segundos, três repetições por condição, com resfriamento entre elas. Alterne a ordem das versões para diminuir viés térmico. Cronometre separadamente o carregamento desde a abertura do título até uma tela definida. Anote FPS, velocidade real, memória e temperatura observada com a mesma ferramenta; a sobreposição do emulador fornece FPS/velocidade/frame time/RAM, não a temperatura de todas as partes do chip.

## Matriz

| Condição | Shaders assíncronos | Desativar olho direito | Finalidade |
|---|---|---|---|
| Estável | Não | Não | Referência conservadora; linear ligado |
| Equilibrado | Não | Não | Referência recomendada; linear desligado |
| Lite Turbo | Sim | Sim | Teste conjunto, somente após aceitar aviso |
| Equilibrado + teste somente shaders | Sim | Não | Isolar compilação assíncrona Vulkan |
| Equilibrado + teste somente um olho | Não | Sim | Isolar redução de renderização estereoscópica |

Aplique Equilibrado antes de cada teste isolado para restaurar as outras opções. As ações A/B alteram somente as duas opções experimentais; não mudam backend, filtros ou resolução. Reinicie o jogo após salvar cada alteração. Faça a matriz Vulkan primeiro. Depois repita Estável/Equilibrado e um olho no OpenGL ES; o teste de shaders assíncronos não é aplicável ao GLES. O Turbo no GLES conserva o ajuste assíncrono, mas esse backend não o utiliza.

## Os seis cenários

| Sessão | Ação reproduzível |
|---|---|
| Menu principal | Abrir as mesmas telas, na mesma ordem, com o mesmo intervalo entre toques |
| Seleção | Entrar na seleção de personagens a partir da mesma tela |
| Troca de lutadores | Percorrer uma lista fixa de personagens na mesma ordem e ritmo |
| Efeito inédito | No mesmo estágio/personagem, executar uma sequência definida uma primeira vez |
| Efeito repetido | Repetir exatamente a sequência anterior, sem mudar backend nem opções |
| Combate intenso | Mesmo estágio, número de lutadores, personagens, itens e duração; variação da IA limita a repetibilidade |

Compare a primeira exposição com a repetição, e uma nova abertura com cache em disco já preenchido. Uma cena inédita é apenas uma aproximação de cache frio: recursos podem ter sido usados anteriormente. Para uma comparação fria rigorosa, use uma cópia de dados de teste com backup, isolando somente o cache gráfico com o app fechado; não apague os dados do app nem a pasta inteira. Não há limpeza automática nesta atualização. Caches Vulkan/GLES são distintos e mudanças de driver podem invalidar o cache binário.

## Coletar e analisar

1. Antes de abrir o jogo, ative **Gráficos → Azahar Lite Performance → Registrar tempos de quadro para diagnóstico**. A coleta tem custo adicional; compare sessões com a mesma condição de diagnóstico. Depois dos testes, desligue-a para jogar.
2. Abra o título, execute um cenário e saia normalmente da emulação para gravar o CSV. Encerramento forçado pode perder a sessão.
3. Na subpasta `log` da pasta de dados do Lite, copie os arquivos `.lite-trace.csv` (0.2) ou `.game-intervals.csv` (0.1) para o computador. O comando “compartilhar log” original pode compartilhar somente o log textual; nesse caso copie o CSV pelo gerenciador de arquivos. Não edite o arquivo dentro da pasta ativa do emulador.
4. Rotule cada cópia com versão/perfil/backend/cenário/frio-ou-quente/repetição. Guarde os CSV originais.
5. Rode no computador, na raiz do código:

```bash
python3 lite/tools/analyze_smash_trace.py caminho/sessao.lite-trace.csv --budget-ms 16.667 --label 02-equilibrado-vulkan-menu-r1
python3 lite/tools/analyze_smash_trace.py caminho/sessao.game-intervals.csv --budget-ms 16.667 --label 01-equilibrado-vulkan-menu-r1
```

Escolha `--budget-ms 33.333` se o cenário efetivamente produzir 30 quadros/s. O padrão ignora cinco intervalos iniciais; use a mesma regra em todas as sessões. Para medir boot não descarte o trecho inicial e cronometre também a tela de destino.

O resultado informa média, p99 nearest-rank, máximo, duração amostrada, intervalos acima de 2× o orçamento/50/100 ms e frequência de submissão. Isso não é medição de apresentação física da tela. O CSV original sem sufixo mede processamento do quadro do sistema; não o compare com intervalos entre submissões do jogo.

## Interpretar sem confundir correlação com causa

- `shader_wait`: tempo de chamadas que precisaram entrar na espera de um shader/pipeline Vulkan. Inclui aquisição do mutex; não é tempo puro do compilador.
- `pipeline_build`: tentativas de construir pipeline Vulkan, incluindo sondagem do cache do driver e espera dos estágios. Pode executar em worker e se sobrepor ao quadro.
- `gl_shader_path`: consultas/compilação/gravação do shader VS/FS no OpenGL, incluindo acertos do cache. `gl_program_link` cobre criação/link e gravação do programa não separável na primeira utilização.
- `texture_load`: caminho de carregar uma superfície do cache gráfico, incluindo staging, decode e upload. `texture_decode` e `texture_upload` detalham trechos internos; upload mede trabalho de CPU/submissão, não duração de execução na GPU.
- `stream_reuse_wait`: espera por uma região do buffer Vulkan antes de reutilizá-la. `gpu_wait`: espera efetiva do semáforo/fence quando o tick conhecido ainda não completou.
- `storage_read/write`: chamadas `IOFile`, incluindo acesso por descritor SAF quando passa por esses métodos; não captura todo acesso do Android/provider, fsync nem bytes transferidos.

Os contadores são cumulativos por processo e exportados como diferenças por intervalo, atribuídos quando um escopo termina. Os snapshots entre categorias não são simultâneos. Categorias se sobrepõem e workers rodam em paralelo: NÃO some os tempos para calcular o frame time nem trate uma correlação como prova causal. A coleta limita-se a 36.000 intervalos por sessão (cerca de dez minutos a 60 Hz); a reserva adicional é aproximadamente 6,6 MiB. Não amostra memória/velocidade/temperatura automaticamente: registre esses itens separadamente. Pausas do usuário e background também entram nos intervalos.

Pausas que diminuem ao repetir, acompanhadas de esperas de pipeline, justificam investigar compilação. Pausas persistentes com decode/upload alto sugerem investigar recursos gráficos. Esperas GPU altas podem refletir carga do efeito, driver ou dependências necessárias. Nenhuma categoria elevada não exclui JIT da CPU emulada, descompressão do jogo, coleta de memória do Android ou throttling. Para atribuição temporal mais precisa, use Perfetto/Android GPU Inspector quando suportado pelo dispositivo, sem root e sem alterar o jogo.

Registre regressões visuais (efeito ausente, flicker, olho errado), áudio e travamentos em cada condição. Se houver regressão, restaure Equilibrado, reinicie o jogo e mantenha o CSV correspondente. Um único ensaio favorável não demonstra ganho geral.
