# Pre-commit Hooks Best Practices

## Overview
Este documento describe las mejores prácticas para configurar pre-commit hooks que auto-corrijan problemas en lugar de solo detectarlos.

## Problema Común: Hooks que Fallan Después de Corregir

### Síntoma
Los pre-commit hooks detectan problemas, los corrigen automáticamente, pero luego **fallan** el commit, requiriendo que el desarrollador haga commit nuevamente.

### Causa Raíz
Uso incorrecto del flag `--exit-non-zero-on-fix` en herramientas como Ruff.

### Ejemplo Incorrecto ❌

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.1.9
  hooks:
    - id: ruff
      args: ['--fix', '--exit-non-zero-on-fix']  # ❌ MALO
```

**Comportamiento**:
1. Ruff detecta imports desordenados
2. Ruff los corrige automáticamente
3. Ruff retorna exit code 1 (fallo)
4. Pre-commit hook falla
5. Desarrollador debe hacer `git add` y `git commit` nuevamente

**Resultado**: Fricción innecesaria, los problemas no se detectan hasta CI.

### Ejemplo Correcto ✅

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.1.9
  hooks:
    - id: ruff
      args: ['--fix']  # ✅ BUENO
```

**Comportamiento**:
1. Ruff detecta imports desordenados
2. Ruff los corrige automáticamente
3. Ruff retorna exit code 0 (éxito)
4. Pre-commit hook continúa
5. Commit se completa con código corregido

**Resultado**: Experiencia fluida, código siempre formateado correctamente.

## Filosofía de Auto-corrección

### Principio
> **Los hooks deben corregir problemas automáticamente, no solo detectarlos.**

### Razones
1. **Mejor experiencia de desarrollador**: No interrumpe el flujo de trabajo
2. **Prevención temprana**: Los problemas se corrigen antes de llegar a CI
3. **Consistencia**: Todo el código pasa por el mismo proceso de corrección
4. **Menos fricción**: No requiere intervención manual repetitiva

## Configuración Recomendada

### Black (Formatter)
```yaml
- repo: https://github.com/psf/black
  rev: 24.1.1
  hooks:
    - id: black
      language_version: python3.11
      args: ['--config=pyproject.toml']
```

**Comportamiento**: Formatea código automáticamente sin fallar.

### Ruff (Linter + Import Sorter)
```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.1.9
  hooks:
    - id: ruff
      args: ['--fix']  # Auto-fix sin fallar
    - id: ruff-format  # Formateo adicional
```

**Comportamiento**: Corrige imports, linting issues, y formatea sin fallar.

### Prettier (JavaScript/TypeScript)
```yaml
- repo: https://github.com/pre-commit/mirrors-prettier
  rev: v3.1.0
  hooks:
    - id: prettier
      types_or: [javascript, jsx, ts, tsx, json, yaml, markdown]
```

**Comportamiento**: Formatea archivos automáticamente sin fallar.

## Cuándo Usar Exit-Non-Zero

### Casos Válidos
Solo usar `--exit-non-zero-on-fix` en **pre-push hooks** o **CI**, nunca en pre-commit:

```yaml
# Pre-push hook (scripts/pre-push-format-check.sh)
#!/bin/bash
# Verificar que no haya cambios pendientes de formato
black --check src/ tests/
ruff check src/ tests/  # Sin --fix, solo check

if [ $? -ne 0 ]; then
  echo "❌ Code is not formatted. Run: black src/ tests/ && ruff check --fix src/ tests/"
  exit 1
fi
```

**Razón**: En pre-push queremos **detectar** si algo se escapó, no corregirlo.

## Lecciones Aprendidas - PR #7

### Problema
- Imports desordenados no se corregían localmente
- Pasaban pre-commit pero fallaban en CI
- Desarrolladores tenían que hacer múltiples commits

### Causa
```yaml
# Configuración incorrecta
- id: ruff
  args: ['--fix', '--exit-non-zero-on-fix']  # ❌
```

### Solución
```yaml
# Configuración correcta
- id: ruff
  args: ['--fix']  # ✅
```

### Resultado
- Imports se corrigen automáticamente en cada commit
- No más fallos en CI por imports desordenados
- Mejor experiencia de desarrollador

## Checklist de Configuración

Al configurar pre-commit hooks:

- [ ] Hooks formatean/corrigen automáticamente
- [ ] Hooks NO fallan después de aplicar correcciones
- [ ] Hooks son rápidos (<5 segundos para cambios típicos)
- [ ] Configuración es idéntica entre local y CI
- [ ] Documentación explica qué hace cada hook

## Testing de Hooks

### Verificar Comportamiento
```bash
# 1. Crear archivo con problema intencional
echo "import sys\nimport os" > test_imports.py

# 2. Agregar al staging
git add test_imports.py

# 3. Intentar commit
git commit -m "test: verify hook behavior"

# 4. Verificar resultado
# ✅ Esperado: Commit exitoso, imports corregidos
# ❌ Problema: Commit falla, requiere re-commit
```

### Verificar Correcciones
```bash
# Ver qué cambió el hook
git diff test_imports.py

# Debería mostrar imports ordenados:
# import os
# import sys
```

## Referencias

- [Pre-commit Documentation](https://pre-commit.com/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Black Documentation](https://black.readthedocs.io/)
- [Git Workflow Guide](git-workflow.md)

## Resumen

**TL;DR**:
- ✅ Usa `--fix` en pre-commit hooks para auto-corregir
- ❌ NO uses `--exit-non-zero-on-fix` en pre-commit
- ✅ Usa `--check` (sin fix) en pre-push/CI para detectar
- 🎯 Objetivo: Código siempre correcto, sin fricción

---

**Última actualización**: 28 de enero de 2026
