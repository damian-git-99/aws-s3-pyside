# disable-dark-mode Specification

## Purpose
Garantizar que la aplicación PySide6 utilice siempre un tema claro, ignorando la configuración de tema del sistema operativo (especialmente importante en Windows donde el modo dark causa problemas visuales).

## Requirements

### Requirement: Forzar tema claro en aplicación PySide6
La aplicación DEBE usar el estilo "Fusion" con paleta clara explícita al iniciar, ignorando el tema del sistema operativo.

#### Scenario: Aplicación inicia en Windows con tema dark
- **WHEN** la aplicación se inicia en Windows con tema dark del sistema habilitado
- **THEN** la interfaz se muestra con estilo claro (light) en lugar de heredar el tema dark

#### Scenario: Aplicación inicia en Linux
- **WHEN** la aplicación se inicia en Linux
- **THEN** la interfaz se muestra consistentemente con estilo claro independientemente del tema del escritorio

#### Scenario: Cambio de tema del SO durante ejecución
- **WHEN** el usuario cambia el tema del sistema operativo mientras la aplicación está en ejecución
- **THEN** la aplicación mantiene el estilo claro y no reacciona al cambio
