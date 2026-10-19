# Azahar Lite 0.1 — Performance Edition (experimental)

**APK ARM64 compilado e assinado para teste.** A compilação local terminou com `BUILD SUCCESSFUL`, e o APK passou nas verificações de assinatura, pacote, arquitetura e biblioteca nativa. A primeira tentativa havia parado na rede; nesta continuação foram instalados SDK/NDK e JDK completos e configurado o proxy correto. Não houve teste de execução em celular nem medição de ganho de desempenho. O workflow não foi executado no GitHub.

## Base e licença

Base estável: Azahar **2126.2**, commit `219d743a1e698101fe1ab8bef43e6563126c3c27`, publicada em 8/10/2026. Fonte: https://github.com/azahar-emu/azahar/releases/tag/2126.2 . Branch local: `azahar-lite/0.1`. Fork independente, sem vínculo com os mantenedores originais. Créditos Citra/Azahar e dependências preservados. O arquivo raiz `license.txt` contém GPLv2; arquivos individuais também declaram GPLv2-ou-posterior ou GPLv3-ou-posterior. Respeite as licenças de cada componente e distribua o código correspondente, incluindo dependências, junto de futuros binários. As alterações novas conservam licenças compatíveis. Não foi enviado PR ao projeto original; este trabalho foi produzido com assistência de IA.

## O que foi implementado

- Identidade Azahar Lite, versão `0.1-performance`, pacote `org.azaharlite.emu`, ARM64 exclusivamente. Namespace JNI original preservado para manter o núcleo nativo funcionando.
- Menu **Configurações → Gráficos → Azahar Lite Performance**, com aplicação de perfis reais e restauração do Equilibrado. O Equilibrado corresponde aos padrões conservadores, com filtragem linear desligada em configurações novas. Não há seleção de perfil continuamente imposta: ajustes manuais posteriores prevalecem.
- Botão Azahar Lite Performance nas propriedades do jogo (pressione a capa). Persiste e aplica por título somente os campos pertencentes aos perfis. Outros ajustes continuam globais. Não troca backend com a janela gráfica já criada.
- Cache Vulkan: limite de leitura e de gravação de **64 MiB por arquivo de cache do driver**, validação adicional do tamanho do cabeçalho, serialização antes de abrir o arquivo de saída e tratamento de erro Vulkan. Em acesso por sistema de arquivos direto, grava arquivo temporário e renomeia para preservar o cache anterior. Com SAF, conserva a gravação direta porque `renameDocument` não garante substituição. Isso não é uma cota total de todos os caches.
- Relógio monotônico (`steady_clock`) para métricas e limitador, evitando descontinuidades causadas por correções do relógio do sistema. Sem alteração da velocidade de emulação ou da meta nativa de FPS.
- Correção do intervalo de iteradores da exportação CSV ao fechar uma sessão com cinco quadros ou menos.
- Diagnóstico opcional: CSV adicional de intervalos entre submissões de quadros do jogo. Armazena no máximo 36.000 amostras, com reserva de memória feita antes da jogatina. Analisador Python calcula média, p99, máximo e contagens de pausas.
- Pasta de dados marcada como pertencente ao Lite. A seleção normal rejeita uma pasta contendo `config`, `nand`, `sdmc` ou `states` de outro emulador. Preferências Android separadas pelo pacote. Nenhum save original foi acessado, importado ou alterado nesta sessão.
- Workflow `.github/workflows/azahar-lite.yml`: build ARM64, assinatura de teste padrão do Gradle, verificação com apksigner, pacote com aapt e presença de `lib/arm64-v8a/libcitra-android.so`.

## Perfis

| Opção | Estável | Equilibrado | Lite Turbo |
|---|---|---|---|
| Resolução | 1× nativa | 1× nativa | 1× nativa |
| Filtro de textura pesado | Desligado | Desligado | Desligado |
| Filtragem linear | Ligada | Desligada | Desligada |
| Cache em disco | Ligado | Ligado | Ligado |
| Multiplicação precisa de shader | Ligada | Ligada | Ligada |
| Shaders assíncronos | Desligados | Desligados | Ligados |
| Desativar olho direito | Não | Não | Sim |
| Profundidade 3D | 0 | 0 | 0 |
| Velocidade / CPU emulada | 100% / 100% | 100% / 100% | 100% / 100% |

Vulkan/OpenGL ES, VSync, otimização SPIR-V e apresentação assíncrona não são forçados pelos perfis. Compare-os no aparelho. A opção assíncrona já existente pode omitir objetos enquanto compila: Turbo exibe aviso e exige confirmação. Filtros leves podem fazer pouca diferença em 1×; não há promessa de redução perceptível das travadas.

## Instalar no Galaxy A15 quando houver APK validado

1. No GitHub Actions do seu repositório, execute **Azahar Lite ARM64**. Baixe o artefato somente se o build e as verificações passarem. Ele contém o APK e evidências de assinatura/pacote/hash.
2. Instale `app-vanilla-release.apk` permitindo instalação pelo aplicativo que abriu o arquivo. O pacote separado permite manter o Azahar oficial instalado.
3. Crie uma pasta vazia exclusiva, como `Documentos/AzaharLite`. Não selecione a pasta do Azahar original. O app não migra saves automaticamente.
4. Selecione separadamente sua pasta de jogos. `.3ds` e `.cci` descriptografados continuam no loader original; não foi recriado esse suporte. As mensagens originais de arquivo inválido/criptografado foram preservadas. Não há ROMs ou chaves nesta entrega.
5. Em idioma, use Português (Brasil), já traduzido no upstream. Aplique Equilibrado e encerre as configurações antes de abrir o jogo. Ative FPS, velocidade, frame time, RAM e temperatura no menu de sobreposição existente.
6. Para ajustes por jogo, abra as propriedades da capa → Azahar Lite Performance antes de iniciar. O botão de restaurar altera somente campos de desempenho; não apaga saves nem configurações inteiras.

A RAM é detectada pelo `ActivityManager`/MemoryUtil original e registrada no log; não foi presumida sua capacidade. A tela de 90 Hz não implica meta de 90 FPS. Caso note cadência irregular, compare 60 Hz e 90 Hz manualmente no mesmo cenário.

## Compilar

Em máquina com rede, JDK 17, SDK Android 35, build-tools 35.0.0, NDK 27.3.13750724 e CMake 3.30.3:

```bash
git submodule update --init --recursive
cd src/android
./gradlew --no-daemon assembleVanillaRelease
```

O wrapper fixa Gradle 8.14.5; AGP 8.13.2 e Kotlin 2.0.20 seguem a base. Dependências Maven, ferramentas e validation layers precisam de rede. O pacote completo inclui metadados Git, os commits do fork e os submódulos materializados nas revisões fixadas. Extraia preservando arquivos ocultos e permissões. A compilação desse pacote completo dispensa o primeiro comando de submódulos. O pacote menor contém patches para aplicar sobre a base oficial, sem duplicar as dependências.

Saída esperada: `src/android/app/build/outputs/apk/vanilla/release/app-vanilla-release.apk`. Sem `ANDROID_KEYSTORE_FILE`, o Gradle usa assinatura debug de teste inclusive na variante release. Guarde um keystore próprio para atualizações consistentes: runners novos podem gerar certificados diferentes. Nunca desinstale para resolver assinatura sem antes criar um backup.

O processo tem versões de ferramentas e base fixadas, mas NÃO é promessa de APK idêntico byte a byte: assinatura, metadados e dependências transitivas influenciam o resultado. O workflow ainda depende de validação real. As alterações foram publicadas em uma branch separada do fork do usuário: https://github.com/thaynansusyt-jpg/azahar/tree/azahar-lite-apk01 . O build desta entrega foi executado localmente, não pelo GitHub Actions.

## Evidências e limites

| Verificação | Resultado nesta sessão |
|---|---|
| Clone/base estável e histórico | Feitos localmente |
| Compilação original | Bloqueada antes de compilar: download Gradle sem rede |
| Compilação modificada | BUILD SUCCESSFUL, 55 tarefas Gradle, 2.183 passos nativos |
| Testes Python do analisador | 4 passaram, dados sintéticos identificados como testes |
| Contrato C++ dos relógios | `g++ -std=c++20 -fsyntax-only -Isrc lite/tests/clock_contract.cpp` passou |
| XML de recursos Android | Parsing passou |
| APK/assinatura/biblioteca | APK 29.016.099 bytes; assinatura v2 válida; pacote org.azaharlite.emu; oito bibliotecas AArch64 e núcleo JNI verificados |
| Samsung A15/GPU Mali/emulação real | Não disponíveis para teste |
| FPS/p99/RAM/temperatura/carregamento | Sem resultados medidos |

Logs em `lite/evidence`. Os testes Python validam o analisador, não a execução do emulador. O check de cabeçalho C++ não substitui build nativo/Android.

Limitações: compatibilidade visual do Turbo e títulos específicos ainda não testada; otimização de sincronização GPU/CPU, priorização de threads e renderização assíncrona não foi alterada sem medições; não há nova política de eviction global para caches; obter os dados Vulkan ainda pode alocar memória antes da checagem de gravação; a coleta não mede apresentação física/scanout. O CSV upstream mede processamento de quadros do sistema, não FPS visível. A coleta nova mede submissões do jogo, pode incluir pausas do usuário e não substitui Perfetto. Não chama FPS de processamento de CPU.

## Comparar desempenho no celular

Faça backup antes. Use o mesmo título legalmente obtido, versão/update, save normal, cenário, backend, 1×, velocidade 100%, temperatura inicial, brilho e duração de 120 segundos. Execute três repetições por condição: original/Lite × Vulkan/OpenGL ES × cache frio/aquecido. Comece com Equilibrado; teste Turbo separadamente. Não compare Turbo com configurações diferentes atribuindo todo o ganho ao código.

Para cache frio, use uma pasta de dados nova separada; não apague a pasta de saves. Para cache aquecido, repita o mesmo percurso. Ative diagnóstico **antes** de abrir o jogo e saia normalmente para exportar em `log`. Desative nos testes finais se quiser avaliar a sobrecarga da coleta. O limite de 36.000 intervalos equivale a aproximadamente dez minutos a 60 FPS. Os primeiros cinco intervalos podem ser descartados no analisador; pausas, menus e transições devem ser excluídos por escolher um percurso controlado.

```bash
python3 lite/tools/analyze_frames.py caminho.csv.game-intervals.csv --budget-ms 33.333333
# Para um jogo nativamente 60 FPS: --budget-ms 16.666667
python3 -m unittest discover -s lite/tests -v
```

Registre FPS médio e velocidade pela sobreposição/log, média e p99 pelo CSV, travadas >2× do orçamento, duração de carregamento cronometrada, RAM e temperatura pela sobreposição/Android. Para consumo aproximado: `adb shell dumpsys meminfo org.azaharlite.emu`; use o pacote do original ao comparar. Perfetto com eventos de agendamento/apresentação é necessário para atribuir as pausas a compilação, CPU/GPU, armazenamento ou escalonamento. Não há coleta inventada destes valores.

## Saves e backups

Com o emulador fechado, copie a pasta exclusiva inteira para outro local pelo gerenciador de arquivos. A cópia completa inclui `sdmc`, `nand`, configurações e estados; confira que a cópia abre antes de trocar versões. Não importe nem compartilhe diretórios entre os dois emuladores. Importação de saves exige sua ação deliberada e deve ser testada em uma cópia. Saves normais do jogo são preferíveis; save states podem ser incompatíveis entre versões, builds e backends, mesmo se a extensão coincidir. Nenhuma rotina de perfil/cache desta versão exclui saves.
