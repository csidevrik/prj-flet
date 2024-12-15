# CONTROL Y SEGUIMIENTO DE GARANTÍAS DE FIEL CUMPLIMIENTO

## A. INFORMACIÓN GENERAL

| N° | Contratista | RUC/ID Fiscal | N° de Contrato | Proyecto/Obra |
|----|-------------|---------------|----------------|---------------|
| 1  |             |               |                |               |
| 2  |             |               |                |               |

## B. DETALLES DE LA GARANTÍA

| N° | Tipo de Garantía | N° de Garantía | Entidad Emisora | Monto Original | Moneda |
|----|------------------|----------------|-----------------|----------------|---------|
| 1  |                  |                |                 |                |         |
| 2  |                  |                |                 |                |         |

## C. VIGENCIA Y CONTROL

| N° | Fecha de Emisión | Fecha de Inicio | Fecha de Vencimiento | Días para Vencer | Estado |
|----|------------------|-----------------|---------------------|------------------|---------|
| 1  |                  |                 |                     | =FÓRMULA         |         |
| 2  |                  |                 |                     | =FÓRMULA         |         |

## D. RENOVACIONES Y SEGUIMIENTO

| N° | Fecha Última Renovación | Nuevo Vencimiento | Monto Actualizado | Observaciones |
|----|------------------------|-------------------|-------------------|----------------|
| 1  |                        |                   |                   |                |
| 2  |                        |                   |                   |                |

## E. CONTROLES ADICIONALES

| N° | Responsable Seguimiento | Última Revisión | Próxima Revisión | Alertas |
|----|------------------------|-----------------|------------------|---------|
| 1  |                        |                 |                  |         |
| 2  |                        |                 |                  |         |

## FÓRMULAS Y VALIDACIONES RECOMENDADAS

1. Días para Vencer = `DIAS(HOY(),Fecha_Vencimiento)`
2. Estado = `SI(Días_para_Vencer<=30,"ALERTA",SI(Días_para_Vencer<=90,"PRÓXIMO","VIGENTE"))`

## INSTRUCCIONES DE USO

1. Completar la información en orden secuencial
2. Actualizar diariamente la revisión de vencimientos
3. Mantener un código de colores para estados:
   - 🔴 Rojo: Vence en menos de 30 días
   - 🟡 Amarillo: Vence en menos de 90 días
   - 🟢 Verde: Vigente
4. Realizar backup semanal del archivo