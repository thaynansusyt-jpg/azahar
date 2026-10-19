# Azahar Lite 0.1 — APK ARM64 de teste

APK compilado em 19/10/2026. O build concluiu com **BUILD SUCCESSFUL em 28m41s**, 55 tarefas Gradle e 2.183 passos nativos. Não houve execução em telefone ou jogo nesta sessão.

## Instalação no Galaxy A15

1. Abra `Azahar_Lite_0.1_ARM64.apk` no Android e autorize a instalação pelo aplicativo usado para abrir o arquivo, se solicitado.
2. Abra **Azahar Lite** e crie/selecione uma pasta vazia exclusiva, por exemplo `Documentos/AzaharLite`. Não selecione a pasta de dados do emulador original.
3. Escolha sua pasta de jogos separadamente. O loader original mantém `.3ds` e `.cci` válidos e descriptografados. O APK não inclui jogos ou chaves.
4. Abra Configurações → Gráficos → Azahar Lite Performance e aplique **Equilibrado**. Saia das configurações antes de iniciar o jogo.
5. Para ajustes por título, pressione a capa do jogo e abra Azahar Lite Performance nas propriedades. Lite Turbo avisa antes de ativar shaders assíncronos e desativar o olho direito.

O pacote é `org.azaharlite.emu`, distinto do oficial, permitindo instalação paralela. Nenhum save foi importado automaticamente. Para backup, feche o app e copie sua pasta de dados inteira para outro local. Save states podem não ser compatíveis entre versões; prefira saves normais do jogo.

## Verificações efetivamente concluídas

| Item | Resultado |
|---|---|
| Build | Release Android/ARM64, concluído |
| Versão | `0.1-performance-vanilla`, código 1 |
| Identidade | Nome Azahar Lite; pacote org.azaharlite.emu |
| Arquitetura | Todas as oito bibliotecas nativas são ELF64/AArch64 |
| Núcleo de emulação | `lib/arm64-v8a/libcitra-android.so`, 39.323.504 bytes no APK |
| Entrada JNI para executar jogo | Presente no núcleo nativo |
| Assinatura | APK Signature Scheme v2, RSA 2048, certificado Android Debug |
| Integridade ZIP | Passou |
| Alinhamento do pacote | `zipalign -c -P 16 4` passou |
| Compatibilidade declarada | Android 10/API 29 ou posterior; compilado com SDK 35 |
| Tamanho | 29.016.099 bytes, aproximadamente 27,7 MiB |
| Execução no Galaxy A15 | Não testada |
| FPS, p99, fluidez e temperatura | Não medidos em dispositivo |

SHA-256 do APK:

`21ebf7ad37f1a9d17286efd4d8a7eb7aa52c7d755998a0c9c7d191e09a0079cf`

SHA-256 do certificado público de teste:

`6f574d6239be250bc8bffbbe880ed3d8736bf18c5a5d723ef9041bce2ad6d68f`

A assinatura é para testes; futuras atualizações instaladas sobre esta versão precisam conservar a mesma chave. Não é uma assinatura de publicação na Play Store.

## Código e modificações

Base Azahar 2126.2, commit `219d743a1e698101fe1ab8bef43e6563126c3c27`. Código do fork: https://github.com/thaynansusyt-jpg/azahar/tree/azahar-lite-apk01 . Créditos e licenças originais foram preservados; os submódulos estão fixados nas revisões da base.

Esta versão contém os três perfis com parâmetros reais, persistência dos campos de desempenho por título, identidade/pacote separados, pasta própria, limite por arquivo do cache do driver Vulkan, melhorias de gravação do cache, relógio monotônico e diagnóstico opcional de intervalos de quadros. O build foi limitado a dois processos de compilação C++ para controlar RAM; esse limite não restringe as threads de emulação no celular.

O relatório ZIP inclui o log de build bem-sucedido, assinatura, metadados, estrutura do APK e alinhamento. Os quatro testes Python do analisador e o teste C++ dos relógios haviam passado na etapa anterior; a compilação atual também verificou os arquivos C++/Kotlin modificados.

## Limite desta validação

Compilar e verificar o APK não demonstra que um jogo iniciou nem que as travadinhas diminuíram. O próximo teste é no aparelho: mesmo jogo, save normal, cenário, backend, resolução 1× e velocidade 100%; compare cache frio e aquecido. Use a sobreposição original para FPS, velocidade, frame time e memória. A coleta opcional do Lite permite analisar intervalos de submissão do jogo, sem medir a apresentação física da tela. Não foram inventados resultados de benchmark.
