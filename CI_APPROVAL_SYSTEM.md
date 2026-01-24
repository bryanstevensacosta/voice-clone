# CI Approval System Implementation

## Overview

Sistema implementado para controlar cuándo se ejecuta el CI basado en aprobaciones de PR, con excepción especial para el dueño del repositorio.

## Comportamiento

### Para PRs de @bryanstevensacosta (Owner)
1. ✅ **Auto-aprobación automática**: El workflow `auto-approve.yml` aprueba el PR inmediatamente
2. ✅ **CI corre sin esperar**: El CI detecta que el autor es el owner y ejecuta todos los checks
3. ✅ **Sin delays**: Flujo de trabajo normal sin interrupciones

### Para PRs de Otros Contribuidores
1. ⏳ **CI espera aprobación**: El workflow `ci.yml` detecta que falta aprobación
2. 💬 **Notificación**: Bot comenta en el PR explicando la espera
3. ✅ **Después de aprobación**: CI se ejecuta automáticamente cuando alguien aprueba
4. 🔄 **Re-ejecución**: Si se pushean nuevos commits, CI vuelve a correr (si sigue aprobado)

## Archivos Implementados/Modificados

### Nuevos Archivos
1. ✅ `.github/workflows/auto-approve.yml` - Auto-aprobación para owner
2. ✅ `.github/workflows/README.md` - Documentación de workflows

### Archivos Modificados
1. ✅ `.github/workflows/ci.yml` - Lógica de aprobación agregada
2. ✅ `terraform/main.tf` - Status check `check-approval` agregado

## Workflows de GitHub Actions

### 1. Auto Approve Workflow

**Archivo**: `.github/workflows/auto-approve.yml`

**Trigger**:
- `pull_request_target` (opened, synchronize, reopened)

**Condición**:
```yaml
if: github.event.pull_request.user.login == 'bryanstevensacosta'
```

**Acciones**:
1. Aprueba el PR automáticamente usando `hmarr/auto-approve-action@v3`
2. Agrega comentario indicando auto-aprobación

**Permisos**:
- `pull-requests: write`

### 2. CI Workflow (Modificado)

**Archivo**: `.github/workflows/ci.yml`

**Triggers**:
- `push` a master/main/develop
- `pull_request` a master/main/develop
- `pull_request_review` (cuando se aprueba)

**Nuevo Job**: `check-approval`
```javascript
// Lógica de decisión
const prAuthor = context.payload.pull_request.user.login;
const owner = 'bryanstevensacosta';

if (prAuthor === owner) {
  // Owner: CI corre inmediatamente
  core.setOutput('should_run', 'true');
  return;
}

// Otros: Verificar aprobaciones
const reviews = await github.rest.pulls.listReviews(...);
const hasApproval = reviews.data.some(review => review.state === 'APPROVED');
core.setOutput('should_run', hasApproval ? 'true' : 'false');
```

**Jobs Modificados**: `lint`, `type-check`, `test`
```yaml
needs: [check-approval]
if: |
  github.event_name == 'push' ||
  github.event_name == 'pull_request_review' ||
  (github.event_name == 'pull_request' && needs.check-approval.outputs.should_run == 'true')
```

**Nuevo Job**: `waiting-for-approval`
- Solo corre cuando CI está esperando
- Comenta en el PR para informar al contribuidor

## Configuración de Terraform

### Status Checks Actualizados

Agregado `check-approval` a los status checks requeridos:

```hcl
required_status_checks {
  strict = true
  contexts = [
    "check-approval",      # ← NUEVO
    "lint (3.9)",
    "lint (3.10)",
    "lint (3.11)",
    "type-check (3.9)",
    "type-check (3.10)",
    "type-check (3.11)",
    "test (3.9)",
    "test (3.10)",
    "test (3.11)"
  ]
}
```

Esto asegura que el job `check-approval` debe completarse antes de poder hacer merge.

## Flujo de Trabajo Detallado

### Escenario 1: PR del Owner

```
1. @bryanstevensacosta crea PR
   ↓
2. auto-approve.yml se activa
   ↓
3. PR es aprobado automáticamente ✅
   ↓
4. ci.yml se activa (pull_request event)
   ↓
5. check-approval job:
   - Detecta: author == 'bryanstevensacosta'
   - Output: should_run = 'true'
   ↓
6. lint, type-check, test corren en paralelo
   ↓
7. Todos los checks pasan ✅
   ↓
8. PR listo para merge
```

### Escenario 2: PR de Contribuidor

```
1. Contribuidor crea PR
   ↓
2. ci.yml se activa (pull_request event)
   ↓
3. check-approval job:
   - Detecta: author != owner
   - Verifica aprobaciones: ninguna
   - Output: should_run = 'false'
   ↓
4. lint, type-check, test NO corren ⏸️
   ↓
5. waiting-for-approval job corre:
   - Comenta: "⏳ CI is waiting for approval"
   ↓
6. Reviewer aprueba el PR ✅
   ↓
7. ci.yml se activa (pull_request_review event)
   ↓
8. check-approval job:
   - Verifica aprobaciones: 1 encontrada
   - Output: should_run = 'true'
   ↓
9. lint, type-check, test corren en paralelo
   ↓
10. Todos los checks pasan ✅
    ↓
11. PR listo para merge
```

## Configuración Requerida en GitHub

### 1. Workflow Permissions

**Settings → Actions → General → Workflow permissions**:
- ✅ Select: "Read and write permissions"
- ✅ Check: "Allow GitHub Actions to create and approve pull requests"

Sin esto, el auto-approve no funcionará.

### 2. Branch Protection (via Terraform)

Ya configurado en `terraform/main.tf`:
- ✅ `required_approving_review_count = 1`
- ✅ `enforce_admins = false` (permite que owner bypasee si necesario)
- ✅ Status checks incluyen `check-approval`

## Testing

### Test 1: PR del Owner

```bash
# Como @bryanstevensacosta
git checkout -b test/owner-flow
echo "test" >> test.txt
git add test.txt
git commit -m "test: owner PR flow"
git push origin test/owner-flow

# Crear PR en GitHub
# Verificar:
# 1. Auto-approve corre y aprueba ✅
# 2. CI corre inmediatamente ✅
# 3. No hay mensaje de "waiting for approval" ✅
```

### Test 2: PR de Contribuidor

```bash
# Como contribuidor (o simular con otra cuenta)
git checkout -b test/contributor-flow
echo "test" >> test.txt
git add test.txt
git commit -m "test: contributor PR flow"
git push origin test/contributor-flow

# Crear PR en GitHub
# Verificar:
# 1. CI NO corre inicialmente ⏸️
# 2. Bot comenta "waiting for approval" 💬
# 3. Después de aprobar, CI corre ✅
```

## Troubleshooting

### Auto-approve no funciona

**Síntomas**: PR del owner no se aprueba automáticamente

**Soluciones**:
1. Verificar workflow permissions (ver arriba)
2. Verificar que el username es correcto: `bryanstevensacosta`
3. Verificar que el workflow está en la rama base (master/main)
4. Revisar logs del workflow: `gh run list --workflow=auto-approve.yml`

### CI corre antes de aprobación para contribuidores

**Síntomas**: CI corre inmediatamente para PRs de contribuidores

**Soluciones**:
1. Verificar la lógica en `check-approval` job
2. Verificar que el evento es `pull_request` y no `push`
3. Revisar logs: `gh run view <run-id>`

### CI no corre después de aprobación

**Síntomas**: Después de aprobar, CI sigue sin correr

**Soluciones**:
1. Verificar que el trigger `pull_request_review` está configurado
2. Verificar que la aprobación es de tipo "APPROVED" (no solo comentario)
3. Puede necesitar un push adicional para re-trigger

## Mantenimiento

### Cambiar el Owner

Actualizar en dos lugares:

1. `.github/workflows/auto-approve.yml`:
```yaml
if: github.event.pull_request.user.login == 'nuevo-username'
```

2. `.github/workflows/ci.yml`:
```javascript
const owner = 'nuevo-username';
```

### Cambiar Requisitos de Aprobación

Para requerir 2 aprobaciones en lugar de 1:

1. `.github/workflows/ci.yml`:
```javascript
const approvalCount = reviews.data.filter(r => r.state === 'APPROVED').length;
const hasApproval = approvalCount >= 2;
```

2. `terraform/main.tf`:
```hcl
required_approving_review_count = 2
```

3. Aplicar Terraform:
```bash
cd terraform
terraform apply
```

## Seguridad

### pull_request_target

El workflow de auto-approve usa `pull_request_target` en lugar de `pull_request`:
- ✅ Corre en contexto de la rama base (tiene permisos)
- ✅ Tiene acceso a secrets
- ✅ Seguro porque solo corre para el owner (hardcoded)

### Token Permissions

- `auto-approve.yml`: Necesita `pull-requests: write`
- `ci.yml`: Solo necesita permisos de lectura (default)

## Beneficios

1. ✅ **Seguridad**: Código de contribuidores es revisado antes de correr CI
2. ✅ **Eficiencia**: Owner no tiene delays en su workflow
3. ✅ **Transparencia**: Contribuidores saben por qué CI no corre
4. ✅ **Automatización**: Todo es automático, sin intervención manual
5. ✅ **Flexible**: Fácil de ajustar requisitos de aprobación

## Referencias

- [GitHub Actions: pull_request_target](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#pull_request_target)
- [GitHub Script Action](https://github.com/actions/github-script)
- [Auto Approve Action](https://github.com/hmarr/auto-approve-action)
- [Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
