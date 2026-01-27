# CI/CD Quality Standards

## Overview
Este documento define los estándares de calidad para CI/CD y las medidas preventivas para evitar fallos en el pipeline.

## Lecciones Aprendidas de PR #7

### Problema Identificado
**Fecha**: 27 de enero de 2026
**PR**: #7 - Feature/gradio UI complete implementation
**Fallo**: Lint check falló en Python 3.11 debido a formato inconsistente de código

**Root Cause**:
- Archivo `tests/integration/test_manual_simulation.py` no estaba formateado con Black
- El código pasó localmente pero falló en CI
- Black formatea diferente en Python 3.10 vs 3.11 en algunos casos edge

### Solución Implementada

#### 1. Pre-commit Hooks Obligatorios
Todos los desarrolladores DEBEN instalar y usar pre-commit hooks:

```bash
# Instalar pre-commit
pip install pre-commit

# Instalar hooks
pre-commit install
pre-commit install --hook-type pre-push

# Verificar instalación
pre-commit run --all-files
```

#### 2. Pre-push Format Check
Hook automático que verifica formato antes de push:
- Ejecuta Black en modo check
- Ejecuta Ruff para detectar issues
- Bloquea push si hay problemas de formato
- Ubicación: `scripts/pre-push-format-check.sh`

#### 3. Configuración de Black
Black configurado para Python 3.11 en `pyproject.toml`:

```toml
[tool.black]
line-length = 100
target-version = ['py310', 'py311']
include = '\.pyi?$'
```

**IMPORTANTE**: Siempre incluir `py311` en target-version para consistencia.

## Reglas Obligatorias

### Antes de Hacer Commit

1. **Formatear código automáticamente**:
   ```bash
   black src/ tests/
   ruff check src/ tests/ --fix
   ```

2. **Verificar con pre-commit**:
   ```bash
   pre-commit run --all-files
   ```

3. **Ejecutar tests localmente**:
   ```bash
   pytest tests/ -v
   ```

### Antes de Hacer Push

1. **El pre-push hook se ejecuta automáticamente**
   - Verifica formato con Black
   - Verifica linting con Ruff
   - Bloquea push si hay problemas

2. **Si el hook falla**:
   ```bash
   # Formatear código
   black src/ tests/

   # Fix linting issues
   ruff check src/ tests/ --fix

   # Verificar
   black --check src/ tests/

   # Intentar push nuevamente
   git push
   ```

### Antes de Crear PR

1. **Verificar que CI pasará**:
   ```bash
   # Ejecutar todos los checks localmente
   make lint
   make type-check
   make test
   ```

2. **Verificar formato en ambas versiones de Python**:
   ```bash
   # Si tienes pyenv o múltiples versiones
   python3.10 -m black --check src/ tests/
   python3.11 -m black --check src/ tests/
   ```

## Comandos de Makefile

Agregados comandos para facilitar verificación:

```makefile
# Formatear todo el código
format:
	black src/ tests/
	ruff check src/ tests/ --fix

# Verificar formato sin cambiar archivos
format-check:
	black --check src/ tests/
	ruff check src/ tests/

# Ejecutar todos los checks de CI localmente
ci-check: format-check lint type-check test
```

## Configuración de CI

### GitHub Actions Workflow
El workflow de CI ejecuta los mismos checks:

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11']
    steps:
      - name: Check code formatting with Black
        run: black --check src/ tests/

      - name: Lint with Ruff
        run: ruff check src/ tests/
```

**CRÍTICO**: Los checks de CI deben ser idénticos a los pre-commit hooks locales.

## Prevención de Fallos Futuros

### Checklist para Desarrolladores

Antes de cada commit:
- [ ] Código formateado con Black
- [ ] Imports ordenados con Ruff
- [ ] Pre-commit hooks ejecutados
- [ ] Tests pasando localmente

Antes de cada push:
- [ ] Pre-push hook pasó exitosamente
- [ ] Todos los tests pasan
- [ ] No hay warnings de Ruff

Antes de crear PR:
- [ ] `make ci-check` pasa exitosamente
- [ ] Código revisado manualmente
- [ ] Commits tienen mensajes descriptivos
- [ ] Branch actualizado con master/main

### Automatización

1. **Pre-commit hooks**: Formatean código automáticamente en cada commit
2. **Pre-push hooks**: Verifican formato antes de push
3. **CI checks**: Validan en múltiples versiones de Python
4. **Branch protection**: Requiere que CI pase antes de merge

## Troubleshooting

### "Black would reformat files" en pre-push

**Problema**: El hook de pre-push detectó archivos sin formatear

**Solución**:
```bash
# Formatear archivos
black src/ tests/

# Agregar cambios
git add -u

# Hacer commit
git commit -m "style: format code with black"

# Intentar push nuevamente
git push
```

### Diferencias de formato entre Python 3.10 y 3.11

**Problema**: Black formatea diferente en distintas versiones

**Solución**:
- Siempre usar Python 3.11 para desarrollo
- Configurar `target-version = ['py310', 'py311']` en pyproject.toml
- Ejecutar `black --check` en ambas versiones antes de PR

### Pre-commit hooks no se ejecutan

**Problema**: Los hooks no corren automáticamente

**Solución**:
```bash
# Reinstalar hooks
pre-commit uninstall
pre-commit install
pre-commit install --hook-type pre-push

# Verificar instalación
ls -la .git/hooks/
```

## Métricas de Calidad

### Objetivos
- **Formato**: 100% de archivos formateados con Black
- **Linting**: 0 errores de Ruff
- **Type checking**: 0 errores de Mypy (excepto tests)
- **Tests**: >80% coverage, 0 fallos

### Monitoreo
- CI debe pasar en todas las versiones de Python (3.10, 3.11)
- Pre-commit hooks deben estar instalados en todos los entornos de desarrollo
- Revisión de código debe verificar calidad antes de aprobar PR

## Referencias

- [Black Documentation](https://black.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Git Workflow Guide](docs/git-workflow.md)

## Historial de Cambios

### 2026-01-27
- **Creado**: Documento de estándares de CI/CD
- **Agregado**: Pre-push format check hook
- **Actualizado**: Configuración de Black para Python 3.11
- **Documentado**: Lecciones aprendidas de PR #7
