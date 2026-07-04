export type DocumentTemplate =
  | 'Carta formal'
  | 'Propuesta comercial'
  | 'Plan de clase'
  | 'Contrato simple'
  | 'Descripcion de producto'
  | 'Correo profesional';

export function generateMockDocument(template: string, prompt: string) {
  const cleanPrompt = prompt.trim() || 'Sin instrucciones especificas.';

  return `# ${template}

## Contexto
${cleanPrompt}

## Borrador generado
Este es un primer borrador creado por Forge Documents AI en modo simulacion. En la version conectada a IA real, este contenido sera generado por Forge AI Router usando el mejor proveedor disponible para la tarea.

## Estructura sugerida
1. Introduccion clara.
2. Desarrollo del contenido principal.
3. Puntos clave o beneficios.
4. Cierre profesional.

## Siguiente accion
Revisar el texto, ajustar el tono y exportar el documento cuando este listo.`;
}
