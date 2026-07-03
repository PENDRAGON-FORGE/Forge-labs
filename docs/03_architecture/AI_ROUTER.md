# Forge AI Router v0.1

## Objetivo

Evitar dependencia de un solo proveedor de IA y seleccionar el mejor modelo segun la tarea.

## Proveedores iniciales

- Modelo principal para razonamiento, codigo y documentos.
- Modelo para integraciones con Google y contexto largo.
- Modelo para documentos extensos y escritura profunda.
- Modelos open source para privacidad y reduccion de costos.
- Modelos 3D futuros para generacion de assets.

## Flujo

Usuario -> Forge Core -> Forge AI Router -> Proveedor elegido -> Validador de calidad -> Resultado.

## Regla

Si un proveedor falla o da baja calidad, Forge AI Router debe poder cambiar de modelo.
