# 💬 SIMBA Chat CLI - Guía de Uso

¡Chatea con SIMBA directamente desde tu terminal!

## 🚀 Inicio Rápido (Modo Demo)

```bash
cd /home/user/simbai/backend
python scripts/chat_cli.py
```

Eso es todo! El chat funciona inmediatamente en modo DEMO con respuestas simuladas.

## 🎮 Cómo Usar

1. **Selecciona un asistente** (1-4)
   - SIMBA Assistant (general)
   - Code Assistant (programación)
   - Research Assistant (investigación)
   - Creative Assistant (creatividad)

2. **Escribe tus mensajes** y presiona Enter

3. **Comandos disponibles:**
   - `help` - Ver ayuda
   - `clear` - Limpiar pantalla
   - `status` - Ver estado
   - `exit` o `quit` - Salir

## ⚡ Modo REAL con LLMs

Para usar OpenAI o Anthropic en lugar del modo demo:

### Opción 1: OpenAI (GPT-4)

```bash
# Crear archivo .env
cat > .env << EOF
OPENAI_API_KEY=sk-tu-key-aqui
EOF

# Ejecutar chat
python scripts/chat_cli.py
```

### Opción 2: Anthropic (Claude)

```bash
# Crear archivo .env
cat > .env << EOF
ANTHROPIC_API_KEY=sk-ant-tu-key-aqui
EOF

# Ejecutar chat
python scripts/chat_cli.py
```

## 📊 Ejemplo de Uso

```
======================================================================
  SIMBA - Sistema Inteligente de Mensajería con Backend Avanzado
  Interactive Chat CLI
======================================================================

Asistentes disponibles:
  1. SIMBA Assistant
  2. Code Assistant
  3. Research Assistant
  4. Creative Assistant

Selecciona un asistente (1-4): 1

✓ Asistente seleccionado: SIMBA Assistant
✓ Conversación creada: abc-123

💬 Chateando con SIMBA Assistant
======================================================================

🧑 Tú: Hola, ¿cómo estás?

🤖 SIMBA Assistant: ¡Hola! Estoy muy bien, gracias por preguntar...

🧑 Tú: exit

👋 ¡Hasta luego!
📊 Estadísticas finales:
   Total de mensajes: 2
```

## 🔧 Troubleshooting

**"Usuario de prueba no encontrado"**
```bash
python scripts/seed_data.py
```

**Quiero ver menos logs**
- Los logs en desarrollo son normales
- Para producción, cambia DEBUG=False en config.py

**Quiero probar diferentes modelos**
- Cada asistente puede tener un modelo diferente
- Edita en scripts/seed_data.py

## 🎯 Características

- ✅ Chat interactivo en tiempo real
- ✅ Streaming de respuestas (palabra por palabra)
- ✅ Múltiples asistentes con personalidades diferentes
- ✅ Modo demo sin API keys
- ✅ Soporte para OpenAI y Anthropic
- ✅ Historial de conversaciones guardado en BD
- ✅ Estadísticas de uso

## 📝 Notas

- Todas las conversaciones se guardan en la base de datos SQLite
- Puedes ver el historial ejecutando los scripts de test
- El streaming simula un chat real, palabra por palabra
- En modo demo, las respuestas son educativas sobre cómo configurar API keys

---

**¿Preguntas?** Revisa el código en `scripts/chat_cli.py` o ejecuta los tests en `scripts/test_chat_mock.py`
