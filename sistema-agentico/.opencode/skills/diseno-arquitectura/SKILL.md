---
name: diseno-arquitectura
description: Reglas para estructurar módulos, separación de responsabilidades, flujo de datos y elección de patrones de diseño.
---

# Diseño de arquitectura

## Estructura de módulos
- Un módulo debe tener una sola responsabilidad de negocio cohesionada.
- Un archivo debe tener una única razón para existir; si crece, se divide.

## Separación de responsabilidades
- La lógica de negocio no conoce detalles de UI ni de persistencia.
- Cada componente o función tiene una responsabilidad clara y acotada.

## Flujo de datos
- Entrada → validación → procesamiento → salida.
- Pasar datos explícitos por parámetros; evitar estado oculto en variables globales.
- Un camino de flujo por función.

## Patrones de diseño
- Elegir el patrón por necesidad real (Strategy, Factory, Repository...), no por moda.
- Preferir composición sobre herencia.
