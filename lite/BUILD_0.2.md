# Azahar Lite 0.2 — Performance Boost Edition

Continuação da versão 0.1, com base Azahar 2126.2. Fonte anterior preservada em `azahar-lite-apk01`; antes das modificações também foi criado um backup Git local completo e mantidos o APK/fonte/chave 0.1 recuperados; atualização em https://github.com/thaynansusyt-jpg/azahar/tree/azahar-lite-apk02 . Fork independente; créditos, GPL e submódulos originais preservados. Esta atualização foi produzida com assistência de IA.

**Estado da entrega:** compilação Android em andamento. Os resultados finais do APK serão registrados após verificar o arquivo efetivamente produzido. Não houve execução em Samsung Galaxy A15 nem uso de ROM comercial nesta sessão. O relato de melhora na 0.1 é feedback do usuário, sem benchmark comparável registrado.

## Mudanças reais de 0.1 para 0.2

| Área | Implementação | Justificativa e limite |
|---|---|---|
| Publicação de shaders/pipelines Vulkan | `AsyncHandle::IsDone` usa acquire e `MarkDone` usa release; notificação fora do mutex; retorno rápido quando pronto | O worker escreve o módulo/handle antes de publicar conclusão. O leitor precisa adquirir essa publicação. Evita entrar no mutex para recursos prontos, sem retirar a espera por recursos pendentes. Não demonstra redução de pausas no aparelho |
| Reuso do buffer Vulkan | Busca binária seleciona a última watch necessária e espera uma vez pelo seu tick | Dentro da mesma volta do buffer, endereços e ticks são não decrescentes; completar o último tick cobre os anteriores na mesma fila. Mantém cursor/limite/tick final do algoritmo anterior, com menos chamadas de espera. Não altera barreiras nem remove dependências CPU/GPU |
| Fallback de fence Vulkan | Retorna antes do mutex quando o tick já completou | Usa a leitura acquire de `IsFree` já existente; caminho de espera continua protegido por mutex/condvar |
| Diagnóstico opt-in | CSV por intervalo do jogo com contadores/tempos de espera de shader, pipeline, decode/upload, buffer, GPU, caminho de shader/link GLES e IOFile | Diferencia hipóteses para os efeitos e menus. Sem alocação por amostra após reserva; limite de 36.000 intervalos; cerca de 6,6 MiB adicionais quando habilitado. Escopos sobrepostos não podem ser somados como frame time |
| Exportação | Nome de sessão inclui segundos e contador monotônico | Evita que sessões rápidas no mesmo minuto sobrescrevam o CSV anterior |
| Testes A/B na interface | Ações independentes de shaders assíncronos e um olho, com aviso antes de aplicar | Alteram somente as duas opções experimentais. Conservam demais opções, perfis e ajustes por jogo; não trocam backend automaticamente |
| Build | Código de versão 2; `0.2-performance-boost-vanilla`; CMake compila alvo `citra-android` e dependências, com testes nativos upstream fora do APK | Reduz trabalho de build desnecessário. Limite de quatro compiladores e um linker é só na máquina de build; não limita threads de emulação no telefone |

O teste de contrato compara todos os arquivos usados por `GenerateSCMRev.cmake` com o commit 0.1 `8fb0faab5ae73c0034ffcf6dcfaa9f70c9ead5e5`. O hash de versão do cache de shaders permanece **a5e22ca9777f1d06cb9c90cd01878d7b**. Nenhum formato, gerador ou versão do cache foi alterado nesta atualização. Compatibilidade do cache binário do driver ainda depende do dispositivo/driver. A proteção de gravação e o limite de 64 MiB por arquivo da 0.1 permanecem; não é uma cota total de todos os caches.

## O que a inspeção encontrou — e o que ainda falta medir

O código já possui cache persistente e compilação em workers Vulkan. A opção assíncrona modifica o comportamento de espera/omissão de desenhos; não cria um sistema fictício de pré-compilação. No rasterizador Vulkan, desenhos com até seis vértices continuam podendo aguardar pipelines, mesmo com async ligado: remover essa proteção pode prejudicar interfaces e não foi feito.

No GLES, consultas de shaders podem compilar/gravar cache na primeira utilização; o caminho de persistência faz flush síncrono. Isso é uma hipótese de custo de I/O, não uma causa confirmada do Smash. A atualização instrumenta o caminho existente; não adia a persistência sem uma implementação e validação próprias.

Texturas normais já usam staging reutilizável. O vetor de decode visto no caminho de hash legado é de texturas personalizadas, portanto não seria correto alterá-lo e anunciar ganho nos menus normais. O grande buffer Vulkan não foi reduzido arbitrariamente: uma redução poderia aumentar voltas e esperas. Não foram alterados precisão, relógio da CPU emulada, JIT, VSync, apresentação assíncrona, SPIR-V, afinidade de threads ou limites térmicos sem evidência de benefício no aparelho.

Essas mudanças reduzem trabalho redundante e corrigem sincronização. Não tornam gratuita a compilação de um novo efeito nem o processamento gráfico real. A causa dominante das quedas bruscas permanece não identificada até coletar dados do dispositivo. Não há promessa de FPS ou porcentagem de ganho.

## Shaders assíncronos e olho direito

**Somente shaders assíncronos (Vulkan):** permite que certos desenhos cujo pipeline ainda não esteja pronto sejam omitidos enquanto a compilação continua. Pode reduzir esperas de primeira utilização, mas causar objetos/efeitos ausentes temporariamente, flickering e maior disputa de CPU entre compilação e emulação. Não é o mesmo que apresentação assíncrona e não acelera automaticamente o GLES. A interface exige escolher Vulkan explicitamente antes do teste.

**Somente um olho:** evita a renderização do segundo olho em situações compatíveis. Em 2D com profundidade zero pode reduzir trabalho gráfico; a economia varia por jogo/caminho. Não é compilação de shader. Pode afetar 3D estereoscópico e efeitos que dependam da segunda vista. O aviso recomenda profundidade zero e inspeção visual.

Estável/Equilibrado continuam com ambas desligadas. Turbo continua com ambas ligadas, sujeito ao aviso já existente. Para descobrir qual ajuda: aplique Equilibrado e depois um único teste A/B, salve e reinicie o jogo. Restaurar Equilibrado desfaz ambos. O teste separado não modifica automaticamente a profundidade: confirme que está em zero antes de usar um olho.

## Instalar preservando saves

1. Feche o Lite e faça uma cópia completa de sua pasta de dados para fora da pasta ativa.
2. Instale o APK 0.2 sobre o Lite 0.1. Não desinstale nem limpe os dados. O pacote continua `org.azaharlite.emu`, distinto do Azahar oficial.
3. Ao abrir, mantenha a pasta Lite que já utiliza e confira um save normal do jogo. Não selecione a pasta de dados do Azahar oficial.
4. Comece com Equilibrado, resolução 1× e velocidade/CPU emulada 100%. Mantenha o backend que já funciona; compare Vulkan/GLES em sessões separadas.
5. Se o instalador relatar conflito de assinatura, interrompa a instalação e preserve os dados: não desinstale para contornar o erro.

A chave original de teste foi recuperada antes do build. A confirmação do certificado do APK final será registrada abaixo. Não há importação, migração ou exclusão automática de saves/configurações/cache nesta atualização. Os loaders e o scanner de jogos da 0.1 foram mantidos, incluindo `.3ds` e `.cci` válidos e descriptografados. Saves normais são preferíveis a save states para alternar versões. O núcleo upstream permanece na mesma base, mas isso não garante compatibilidade universal de estados.

## Reproduzir o build

Ferramentas: JDK 17, Gradle 8.14.5 (wrapper), AGP 8.13.2, Kotlin 2.0.20, SDK 35, build-tools 35.0.0, NDK 27.3.13750724, CMake 3.30.3. Necessita rede para ferramentas/dependências. Sem promessa de reprodutibilidade binária byte a byte.

```bash
git clone --branch azahar-lite-apk02 --recurse-submodules https://github.com/thaynansusyt-jpg/azahar.git
cd azahar
sdkmanager 'platforms;android-35' 'build-tools;35.0.0' 'ndk;27.3.13750724' 'cmake;3.30.3'
g++ -std=c++20 -O2 -pthread -Isrc lite/tests/synchronization.cpp -o /tmp/lite-sync
/tmp/lite-sync
python3 -m unittest discover -s lite/tests -v
cd src/android
./gradlew --no-daemon --max-workers=2 assembleVanillaRelease
```

Para atualizar uma instalação existente, o build precisa usar a mesma chave. A entrega local restaura o keystore original de teste em `~/.android/debug.keystore` antes de compilar. Não publique a chave no código. O workflow aceita secret `AZAHAR_LITE_KEYSTORE_BASE64` contendo esse keystore de teste; sem ele, um runner pode criar outro certificado e o APK não atualizará a instalação existente. As credenciais padrão desse keystore de teste seguem a configuração debug do Gradle. Para produção, defina uma política própria de assinatura.

O workflow `.github/workflows/azahar-lite.yml` compila e verifica o APK, executa os testes do host e disponibiliza artefatos. A execução do workflow é separada do build local. A API do GitHub retornou zero runs para o commit de código publicado nesta sessão; portanto o workflow não foi validado por execução e não é apresentado como build concluído.

## Evidências

- Stress C++: 250 publicações com quatro leitores (incluindo leitura direta de `IsDone`), sem falhas de payload.
- Equivalência do buffer: 5.000 sequências geradas, 100 pedidos cada, comparando cursor, limite e último tick com o laço original; passou. Inclui limites duplicados, ticks iguais, intervalos esgotados e pedidos fora da faixa. Teste de algoritmo, não benchmark de GPU.
- Contrato de relógio monotônico C++: passou.
- Oito testes Python: passaram (média/p99, entrada inválida, 30 FPS nativos, CSV antigo/novo, contadores e versão do cache).
- Recursos XML padrão/PT-BR: parse e nomes únicos passaram; a compilação Android valida referências.
- Logs em `lite/evidence/0.2/`.

| Comparação 0.1 versus 0.2 no Smash/A15 | Resultado disponível |
|---|---|
| FPS médio / velocidade real | Não medidos |
| Média/p99/máximo dos intervalos | Não medidos |
| Pausas percebidas e duração | Não medidas |
| Carregamento, RAM e temperatura | Não medidos |
| Cache frio versus aquecido | Não medido |
| Compatibilidade visual Turbo / testes isolados | Não executada em dispositivo |

Execute [SMASH_TEST_0.2.md](SMASH_TEST_0.2.md) para os seis cenários e a matriz de perfis/backends. O analisador aceita os CSV da 0.1 para permitir comparação consistente. Não mede scanout, não altera FPS, áudio ou velocidade para esconder pausas. Regressões no aparelho exigem restaurar Equilibrado e analisar os registros; testes de host não excluem problemas do driver Mali.

Para repetir as verificações de atualização com os dois APKs reais:

```bash
python3 lite/tools/verify_update.py Azahar_Lite_0.1_ARM64.apk Azahar_Lite_0.2_ARM64.apk --build-tools "$ANDROID_HOME/build-tools/35.0.0"
```

O script verifica assinaturas, certificado igual, pacote, incremento de versão, ZIP, alinhamento, arquitetura das bibliotecas e símbolo JNI de execução do núcleo. Não substitui abrir o app e executar um título no telefone.
