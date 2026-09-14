# 📋 BRIEFING - Projeto Controle AC via ESP32 IR

## 🎯 OBJETIVO ATUAL
Criar código sender completo com WiFi e interface web para controlar ar-condicionado via IR.

---

## 📂 ESTRUTURA DO PROJETO

**Diretório Base**: `c:\Users\victo\OneDrive\Documentos\PlatformIO\Projects\controle_ar_morpheus`

```
controle_ar_morpheus/
├── platformio.ini          # Config: ESP32 DevKit v1, IRremoteESP8266
├── src/
│   └── main.cpp           # ARQUIVO PRINCIPAL (atualmente em modo receiver)
├── CODIGOS_CAPTURADOS.md  # TODOS os 15 códigos temperatura + botões
├── ANALISE_RESULTADO.md   # Análise que provou: protocolo proprietário
└── analise_padrao.py      # Script Python análise (já executado)
```

---

## 🔧 HARDWARE CONFIGURADO

- **Placa**: ESP32 DevKit v1
- **GPIO 14**: IR Receiver (TSOP4838) - para capturar sinais
- **GPIO 15**: IR LED Transmitter - para enviar comandos ao AC
- **Biblioteca**: IRremoteESP8266 v2.8.6 (via GitHub)
- **Serial**: 115200 baud, porta COM10

---

## ✅ O QUE JÁ ESTÁ PRONTO

### 1. Códigos IR Capturados (arquivo: CODIGOS_CAPTURADOS.md)

**15 Temperaturas Completas (16-30°C)**:
- Cada temperatura tem array `uint16_t` com 255 valores (rawData)
- Estado fixo durante captura: VENTILAR OFF, FAN TURBO, SWING OFF, DISPLAY ON, MUDO OFF, ECO OFF
- Exemplos no arquivo começando linha 23

**Outros Botões Capturados**:
- LIGAR (power on)
- DESLIGAR (power off)
- FAN TURBO
- SWING OFF
- Vários outros (ver arquivo completo)

### 2. Análise do Protocolo (arquivo: ANALISE_RESULTADO.md)

**Conclusão**: 
- ❌ Protocolo proprietário - padrão matemático NÃO encontrado
- ✅ Solução: Usar playback direto (rawData)
- Cada código tem 128 bits, é stateful (contém estado completo do AC)

### 3. Configuração WiFi Solicitada

- **SSID**: `[SEU_WIFI_AQUI]`
- **Senha**: `[SUA_SENHA_AQUI]`

---

## 🚀 O QUE PRECISA SER FEITO AGORA

### TAREFA: Criar main.cpp completo com:

#### 1. **Dual Mode (Receiver + Sender)**
```cpp
// Modo RECEIVER: Capturar novos códigos (GPIO 14)
// Modo SENDER: Transmitir comandos (GPIO 15)
// Alternar via: Web interface ou comando serial
```

#### 2. **WiFi + Web Server**
```cpp
#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "[SEU_WIFI_AQUI]";
const char* password = "[SUA_SENHA_AQUI]";
WebServer server(80);
```

#### 3. **Arrays de Dados (copiar de CODIGOS_CAPTURADOS.md)**
```cpp
// Copiar TODOS os 15 arrays de temperatura:
const uint16_t TEMP_30C[255] PROGMEM = { /* dados da linha 25 */ };
const uint16_t TEMP_29C[255] PROGMEM = { /* dados da linha 33 */ };
// ... até TEMP_16C
```

#### 4. **Função de Transmissão**
```cpp
#include <IRremoteESP8266.h>
#include <IRsend.h>

const uint16_t kIrLedPin = 15;  // GPIO 15
IRsend irsend(kIrLedPin);

void enviarTemperatura(int temp) {
  uint16_t* codigo = nullptr;
  
  switch(temp) {
    case 30: codigo = (uint16_t*)TEMP_30C; break;
    case 29: codigo = (uint16_t*)TEMP_29C; break;
    // ... todos até 16
    default: 
      Serial.println("❌ Temperatura inválida! Use 16-30°C");
      return;
  }
  
  irsend.sendRaw(codigo, 255, 38);  // 38kHz
  Serial.printf("✅ Enviado: %d°C\n", temp);
}
```

#### 5. **Interface Web HTML/CSS/JS**

**Página deve ter**:
- 🌡️ **Slider de Temperatura**: 16°C - 30°C
- 🎛️ **Botões Numéricos**: 16, 17, 18... 30 (clique rápido)
- 🔴 **Power**: LIGAR / DESLIGAR
- 💨 **Ventilador**: AUTO, 1, 2, 3, TURBO (quando capturados)
- 🔄 **Swing**: ON/OFF (quando capturados)
- 🖥️ **Display**: ON/OFF (quando capturados)
- 🔇 **Mudo**: ON/OFF (quando capturados)
- ♻️ **ECO**: ON/OFF (quando capturados)
- ⚡ **Ventilar**: ON/OFF (quando capturados)
- 🔧 **Modo Debug**: Alternar para receiver (capturar códigos)
- 📊 **Status**: Mostra última ação executada

**Design**:
- Responsivo (mobile-friendly)
- Estilo moderno (usar gradientes, sombras)
- Cores: Azul/Cyan para frio, Vermelho/Laranja para quente
- Feedback visual ao clicar botões

**Endpoints da API**:
```
GET  /               → Página HTML principal
POST /temp?value=25  → Envia comando temperatura
POST /power?state=on → Liga/Desliga AC
POST /mode?value=rx  → Alterna para receiver mode
GET  /status         → Retorna JSON com estado atual
```

#### 6. **Modo Receiver (Debug)**

Quando ativado via web:
- Para o web server temporariamente
- Ativa IRrecv no GPIO 14
- Imprime códigos capturados no Serial
- Permite capturar códigos faltantes (FAN, SWING, ECO, etc)
- Botão na web para voltar ao modo sender

---

## 📝 CÓDIGOS FALTANTES (Para capturar depois)

**Já temos**: 15 temperaturas, LIGAR, DESLIGAR, FAN TURBO, SWING OFF

**Faltam** (interface pode ter botões desabilitados por enquanto):
- FAN: AUTO, 1, 2, 3 (já temos TURBO)
- SWING: ON (temos OFF)
- DISPLAY: OFF (temos ON)
- MUDO: ON (temos OFF)
- ECO: ON (temos OFF)
- VENTILAR: ON (temos OFF)

---

## 🎨 EXEMPLO DE ESTRUTURA HTML (Sugestão)

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Controle AC - Morpheus</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      margin: 0;
      padding: 20px;
    }
    .container {
      max-width: 600px;
      margin: 0 auto;
      background: white;
      border-radius: 20px;
      padding: 30px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    .temp-display {
      text-align: center;
      font-size: 72px;
      font-weight: bold;
      color: #667eea;
      margin: 20px 0;
    }
    .slider {
      width: 100%;
      height: 15px;
      border-radius: 10px;
      background: linear-gradient(90deg, #3b82f6 0%, #ef4444 100%);
      outline: none;
    }
    .btn {
      padding: 15px 30px;
      margin: 10px;
      border: none;
      border-radius: 10px;
      font-size: 18px;
      cursor: pointer;
      transition: all 0.3s;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    .btn-power-on { background: #10b981; color: white; }
    .btn-power-off { background: #ef4444; color: white; }
    .status {
      background: #f3f4f6;
      padding: 15px;
      border-radius: 10px;
      margin-top: 20px;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1 style="text-align:center;">❄️ Controle AC</h1>
    
    <div class="temp-display" id="tempDisplay">25°C</div>
    
    <input type="range" min="16" max="30" value="25" 
           class="slider" id="tempSlider">
    
    <div style="text-align:center; margin:20px 0;">
      <button class="btn btn-power-on" onclick="power('on')">🔴 LIGAR</button>
      <button class="btn btn-power-off" onclick="power('off')">⚫ DESLIGAR</button>
    </div>
    
    <!-- Botões numéricos rápidos -->
    <div id="quickButtons" style="display:flex; flex-wrap:wrap; justify-content:center;">
      <!-- Gerar botões 16-30 via JS -->
    </div>
    
    <div class="status" id="status">
      Pronto para uso
    </div>
    
    <button class="btn" onclick="toggleMode()" 
            style="width:100%; background:#6366f1; color:white; margin-top:20px;">
      🔧 Modo Debug (Capturar Códigos)
    </button>
  </div>
  
  <script>
    const slider = document.getElementById('tempSlider');
    const display = document.getElementById('tempDisplay');
    
    slider.oninput = function() {
      display.textContent = this.value + '°C';
    }
    
    slider.onchange = function() {
      sendTemp(this.value);
    }
    
    function sendTemp(temp) {
      fetch('/temp?value=' + temp, {method: 'POST'})
        .then(r => r.text())
        .then(msg => {
          document.getElementById('status').textContent = msg;
        });
    }
    
    function power(state) {
      fetch('/power?state=' + state, {method: 'POST'})
        .then(r => r.text())
        .then(msg => {
          document.getElementById('status').textContent = msg;
        });
    }
    
    // Gerar botões 16-30
    const quickBtns = document.getElementById('quickButtons');
    for(let i = 16; i <= 30; i++) {
      const btn = document.createElement('button');
      btn.className = 'btn';
      btn.textContent = i + '°C';
      btn.style.cssText = 'padding:10px 15px; margin:5px; font-size:14px;';
      btn.onclick = () => {
        slider.value = i;
        display.textContent = i + '°C';
        sendTemp(i);
      };
      quickBtns.appendChild(btn);
    }
  </script>
</body>
</html>
```

---

## ⚠️ PONTOS DE ATENÇÃO

1. **PROGMEM**: Usar `PROGMEM` nos arrays para economizar RAM (15 arrays × 510 bytes = ~7.5KB)
2. **Frequência IR**: 38kHz (padrão para AC)
3. **Tamanho dos arrays**: Todos têm exatamente 255 elementos uint16_t
4. **WiFi**: Testar conexão antes de iniciar web server
5. **Dual mode**: Quando em receiver, web server deve pausar (ou avisar na interface)

---

## 📚 BIBLIOTECAS NECESSÁRIAS (já configuradas)

```ini
# platformio.ini
[env:esp32doit-devkit-v1]
platform = espressif32
board = esp32doit-devkit-v1
framework = arduino
lib_deps = https://github.com/crankyoldgit/IRremoteESP8266.git
monitor_speed = 115200
```

**Includes necessários**:
```cpp
#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <IRremoteESP8266.h>
#include <IRsend.h>
#include <IRrecv.h>
#include <IRutils.h>
```

---

## 🎯 RESULTADO ESPERADO

Após upload do código:
1. ESP32 conecta no WiFi "[SEU_WIFI_AQUI]"
2. Imprime IP no Serial Monitor (ex: `192.168.1.100`)
3. Usuário acessa `http://192.168.1.100` no navegador
4. Interface web carrega com controles do AC
5. Ao mover slider ou clicar temperatura, ESP32 transmite sinal IR
6. AC responde mudando temperatura ✅

---

## 📍 ONDE BUSCAR OS DADOS

**Todos os arrays rawData estão em**: `CODIGOS_CAPTURADOS.md`

- Temperatura 30°C: linha 25
- Temperatura 29°C: linha 33
- Temperatura 28°C: linha 41
- Temperatura 27°C: linha 49
- Temperatura 26°C: linha 57
- Temperatura 25°C: linha 65
- Temperatura 24°C: linha 73
- Temperatura 23°C: linha 81
- Temperatura 22°C: linha 89
- Temperatura 21°C: linha 97
- Temperatura 20°C: linha 105
- Temperatura 19°C: linha 113
- Temperatura 18°C: linha 121
- Temperatura 17°C: linha 129
- Temperatura 16°C: linha 137

**Formato de cada array**:
```cpp
uint16_t tempXXC[255] = {4422, 4330, 796, 442, ...};
```

---

## 🏁 PRÓXIMOS PASSOS (Após este código funcionar)

1. ✅ Testar temperatura 16-30°C com AC real
2. 📸 Capturar códigos faltantes (FAN, SWING, ECO, etc)
3. 🎨 Adicionar botões correspondentes na web interface
4. 🔥 Implementar controle completo do AC
5. 💾 Opcional: Salvar preferências em EEPROM/SPIFFS

---

## 💡 DICAS DE IMPLEMENTAÇÃO

### Web Server Básico:
```cpp
void setup() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi conectado!");
  Serial.print("🌐 IP: ");
  Serial.println(WiFi.localIP());
  
  server.on("/", HTTP_GET, handleRoot);
  server.on("/temp", HTTP_POST, handleTemp);
  server.on("/power", HTTP_POST, handlePower);
  
  server.begin();
  Serial.println("🚀 Web server iniciado!");
}

void loop() {
  server.handleClient();
}
```

### Handler Example:
```cpp
void handleTemp() {
  if (server.hasArg("value")) {
    int temp = server.arg("value").toInt();
    if (temp >= 16 && temp <= 30) {
      enviarTemperatura(temp);
      server.send(200, "text/plain", "✅ Temperatura " + String(temp) + "°C enviada!");
    } else {
      server.send(400, "text/plain", "❌ Temperatura inválida! Use 16-30°C");
    }
  }
}
```

---

## 🐛 DEBUGGING

**Se algo não funcionar**:

1. **WiFi não conecta**: Verificar SSID/senha, distância do roteador
2. **IP não aparece**: Aumentar timeout no `while(WiFi.status()...)`
3. **Página não carrega**: Firewall? Testar com `ping <IP_DO_ESP32>`
4. **IR não transmite**: Verificar GPIO 15, conexão do LED, transistor
5. **AC não responde**: Distância do LED, apontar corretamente, testar códigos

**Monitor Serial é seu amigo**:
- Sempre imprimir status de cada operação
- Log de conexão WiFi
- Log de requisições HTTP recebidas
- Log de transmissões IR

---

## ✨ BOA SORTE!

Este projeto está **95% pronto**. Só falta juntar as peças:
- ✅ Hardware configurado
- ✅ Códigos IR capturados e validados
- ✅ Análise completa do protocolo
- ✅ Decisão de implementação tomada (playback direto)
- ⏳ Falta apenas: escrever o main.cpp com web server + HTML

**Tempo estimado**: 30-60 minutos para IA experiente

**Arquivo principal a criar/editar**: `src/main.cpp`

---

📅 **Data**: 7 de Novembro de 2025  
👤 **Usuário**: Victor  
🏠 **Rede WiFi**: [NOME_DA_REDE] ([SENHA])  
🎯 **Meta**: Controlar AC via interface web no ESP32
