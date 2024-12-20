# U-Phy Controller

This contain a python based U-Phy device controller that act as a fieldbus master/controller.

Supported fieldbuses:

- modbus-tcp

## Install

```sh
uv pip install uphy-controller
```

## Workflow

```sh
# Start up controller against an existing device
uphy-controller modbus-tcp --model [PATH_TO_MODEL] --target [UUID]:[HOST]:[PORT]
```
