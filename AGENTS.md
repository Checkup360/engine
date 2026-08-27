# Reglas y Guía para Agentes: Checkup360 Engine

Este documento define las reglas de diseño, arquitectura y estándares obligatorios que todo agente o desarrollador debe seguir al agregar, modificar o extender modelos de evaluación y cálculo de scores de riesgo en el repositorio `engine`.

---

## 1. Arquitectura Hexagonal (Ports & Adapters)

El proyecto sigue estrictamente una **Arquitectura Hexagonal (Clean Architecture)** para garantizar la total independencia de la lógica de negocio respecto a frameworks web, bases de datos o adaptadores externos.

```
┌─────────────────────────────────────────────────────────┐
│                     PRESENTATION                        │
│   FastAPI, Routers, Request/Response Models (Pydantic)  │
│   app/presentation/                                     │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                      APPLICATION                        │
│   Use Cases, DTOs, Commands                             │
│   app/application/                                      │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                        DOMAIN                           │
│   Entities, Value Objects, Calculators, Exceptions      │
│   app/domain/                                           │
└─────────────────────────────────────────────────────────┘
```

### Reglas de Dependencia por Capa:
1. **Capa de Dominio (`app/domain/`)**:
   - **Núcleo puro**: Debe ser 100% Python estándar.
   - **Prohibido**: Importar librerías de infraestructura o presentación (e.g. `fastapi`, `pydantic`, `sqlalchemy`, `requests`).
   - Contiene:
     - Entidades específicas por score: `app/domain/entities/{score_name}_data.py`
     - Value Objects: `app/domain/value_objects/score_result.py`
     - Interfaz Genérica de Calculadoras: `app/domain/services/risk_score_calculator.py`
     - Calculadoras concretas: `app/domain/calculators/{score_name}.py`
     - Servicios de dominio: `app/domain/services/scoring_engine.py`
     - Excepciones de dominio: `app/domain/exceptions.py`
2. **Capa de Aplicación (`app/application/`)**:
   - Orquesta los casos de uso del motor (`app/application/use_cases/`).
   - Invoca los servicios de dominio pasando las entidades de dominio correspondientes.
3. **Capa de Presentación (`app/presentation/`)**:
   - Adaptador primario/de entrada HTTP mediante FastAPI.
   - Valida la entrada HTTP a través de modelos Pydantic específicos por score (`app/presentation/api/request_models/scores/{score_name}_request.py`).
   - Transforma los datos validados directamente a la entidad de dominio (`to_domain()`).
   - Mantiene el registro dinámico de modelos (`app/presentation/api/request_models/registry.py`).
   - Expone los endpoints (`app/presentation/api/routers/`) y gestiona la inyección de dependencias (`app/presentation/api/dependencies.py`).

---

## 2. Tipado Estricto y Formato Único por Dato

Para evitar ambigüedades, inconsistencias clínicas y fallos silenciosos:

1. **Un solo tipo y formato por dato**:
   - Cada parámetro de salud tiene una única unidad de medida y un único tipo de dato oficial en todo el sistema:
     - **Edad**: Entero en años (`int`).
     - **Sexo**: String con valores canónicos estrictos (`"M"` o `"F"`).
     - **Peso**: Decimal en kilogramos (`float`, e.g. `70.5`).
     - **Altura**: Decimal en metros (`float`, e.g. `1.75`). *No se aceptan centímetros ni mezclas de unidades sin normalizar.*
     - **Perímetros (cintura, cuello)**: Decimal en centímetros (`float`).
     - **Presión / Analítica (colesterol, glucosa, etc.)**: Decimal en sus unidades estándar clínicas (`float`).
     - **Variables dicotómicas/síntomas**: Booleanos estrictos (`bool`, e.g. `True` / `False`).
2. **Manejo de Tipos y Formatos Inválidos**:
   - Si un dato proporcionado no cumple con el tipo esperado, posee un formato inválido o viola las reglas de dominio, **se debe lanzar una excepción de dominio** (`InvalidHealthDataError` o una excepción especializada que herede de `EngineDomainError` en `app/domain/exceptions.py`).
   - El mensaje de la excepción debe indicar explícitamente qué campo es incorrecto y el motivo (e.g. `InvalidHealthDataError("Field 'height' must be in meters (float between 0.5 and 2.5), got: ...")`).
3. **Datos Faltantes vs Datos Inválidos**:
   - Si un dato es `None` (no provisto), el calculador que lo requiera no debe lanzar excepción, sino retornar un `ScoreResult` con estado `CalculationStatus.NOT_CALCULABLE` y una explicación informativa en `explanation`.
   - Si un dato está presente pero con formato/tipo erróneo o un valor biológicamente imposible, se debe disparar la excepción correspondiente.

---

## 3. Implementación Obligatoria de la Interfaz de Riesgo (`RiskScoreCalculator`)

Cada score de riesgo debe ser una clase concreta que implemente la interfaz genérica `RiskScoreCalculator[TData]` definida en `app/domain/services/risk_score_calculator.py`.

### Contrato de la Interfaz:
```python
from dataclasses import dataclass
from app.domain.services.risk_score_calculator import RiskScoreCalculator
from app.domain.value_objects.score_result import (
    CalculationStatus,
    ScoreResult,
)


@dataclass(frozen=True)
class MyCustomScoreData:
    age: int | None = None
    weight: float | None = None


class MyCustomScoreCalculator(RiskScoreCalculator[MyCustomScoreData]):
    """Calculador de riesgo para [Nombre del Score]."""

    @property
    def score_id(self) -> str:
        """Identificador único en formato snake_case."""
        return "my_custom_score"

    def calculate(self, data: MyCustomScoreData) -> ScoreResult:
        # 1. Validación de presencia de datos requeridos
        if data.age is None or data.weight is None:
            return ScoreResult(
                score_id=self.score_id,
                score_name="My Custom Score",
                domain="Cardiovascular",  # o Diabetes, Sleep Apnea, etc.
                status=CalculationStatus.NOT_CALCULABLE,
                explanation="Missing required data for My Custom Score",
            )

        # 2. Validación de tipos/formatos y reglas de dominio (si aplica)
        # Lanzar InvalidHealthDataError si los datos presentes son inválidos

        # 3. Lógica de cálculo determinista
        factors: dict[str, float] = {}
        # ... cálculo de factores ...

        total_score = sum(factors.values())
        risk_level = "Low"  # según la escala médica oficial

        # 4. Retornar ScoreResult estandarizado
        return ScoreResult(
            score_id=self.score_id,
            score_name="My Custom Score",
            domain="Cardiovascular",
            status=CalculationStatus.CALCULATED,
            raw_value=total_score,
            risk_level=risk_level,
            contributing_factors=factors,
        )
```

---

## 4. Reglas de Diseño y Principios de Software

1. **Stateless (Sin Estado)**:
   - Las calculadoras deben ser completamente sin estado. El método `calculate` debe ser una función determinista y pura respecto a su entidad clínica de datos.
2. **Inmutabilidad y Aislamiento**:
   - Las entidades y value objects (`FindriscData`, `StopBangData`, `ScoreResult`) deben mantenerse inmutables utilizando `@dataclass(frozen=True)`. No se comparten entidades monolíticas entre scores independientes.
3. **Open/Closed Principle (OCP)**:
   - Para añadir un nuevo score de riesgo, nunca se debe modificar el código interno de calculadoras existentes ni del `ScoringEngine`. Se crea una nueva clase `RiskScoreCalculator`, su entidad de dominio, su request model, y se registra.
4. **Single Responsibility Principle (SRP)**:
   - Cada calculadora solo es responsable de su propio algoritmo clínico y de mapear sus factores determinantes en `contributing_factors`.

---

## 5. Dónde se Agrega Cada Score (Checklist de Implementación)

Al agregar un nuevo score `X`, se deben tocar y verificar los siguientes archivos en orden:

| Capa | Archivo | Responsabilidad |
|---|---|---|
| **Domain (Entidad)** | `app/domain/entities/{score_name}_data.py` | Definir la entidad `@dataclass(frozen=True)` con los campos exclusivos del score. |
| **Domain (Calculador)** | `app/domain/calculators/{score_name}.py` | Implementar `RiskScoreCalculator[{ScoreName}Data]`. |
| **Domain (Excepciones)** | `app/domain/exceptions.py` | Definir excepciones de dominio específicas si aplican. |
| **Presentation (Request)**| `app/presentation/api/request_models/scores/{score_name}_request.py` | Definir `{ScoreName}Request` (Pydantic) con validaciones y método `to_domain()`. |
| **Presentation (Registry)**| `app/presentation/api/request_models/registry.py` | Registrar `{score_name}: {ScoreName}Request` en `SCORE_REQUEST_REGISTRY`. |
| **Presentation (DI)** | `app/presentation/api/dependencies.py` | Instanciar el nuevo calculador dentro de `get_scoring_engine()`. |
| **Documentation** | `docs/calculators/{score_name}.md` | Documentar la base clínica, fórmula, puntajes, factores y bibliografía del score. |
| **Tests** | `tests/unit/domain/calculators/test_{score_name}.py` | Pruebas unitarias de: cálculo completo, datos faltantes (`NOT_CALCULABLE`), casos borde y validación de tipos erróneos. |
| **Tests (Request)** | `tests/unit/presentation/test_score_requests.py` | Pruebas de validación y conversión `to_domain()`. |

---

## 6. Verificación y Calidad de Código

Antes de finalizar cualquier implementación, ejecutar la suite de verificación completa:

```bash
# Ejecutar tests y cobertura
uv run pytest

# Verificación de linter y formateo
uv run ruff check app tests
uv run ruff format --check app tests

# Verificación estática de tipos
uv run pyright
```
