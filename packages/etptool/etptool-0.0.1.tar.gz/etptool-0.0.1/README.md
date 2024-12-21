# Embedded Tester Protocol (ETP) Tool - `etptool` <!-- omit in toc -->

> NOTE: This project is still in development and is not yet ready for production use.

## Setup <!-- omit in toc -->

```
pip install etptool
```

## Manual <!-- omit in toc -->
- [Flash ETP firmware](#flash-etp-firmware)
- [Configure transport](#configure-transport)
- [Verify connection \& firmware version](#verify-connection--firmware-version)
- [GPIO](#gpio)
  - [Get GPIO information](#get-gpio-information)
  - [Initialize GPIO](#initialize-gpio)
  - [Read GPIO](#read-gpio)
  - [Write GPIO](#write-gpio)
- [ADC](#adc)
  - [Get ADC information](#get-adc-information)
  - [Initialize ADC](#initialize-adc)
  - [Read ADC](#read-adc)
- [PWM](#pwm)
  - [Get PWM information](#get-pwm-information)
  - [Initialize PWM](#initialize-pwm)
  - [Set PWM duty cycle](#set-pwm-duty-cycle)
- [I2C](#i2c)
  - [Get I2C information](#get-i2c-information)
  - [Initialize I2C bus](#initialize-i2c-bus)
  - [Scan I2C bus](#scan-i2c-bus)
  - [I2C read](#i2c-read)
  - [I2C Write](#i2c-write)
  - [Register read I2C](#register-read-i2c)
  - [Register write I2C](#register-write-i2c)
- [SPI](#spi)
  - [Get SPI information](#get-spi-information)
  - [Initialize SPI bus](#initialize-spi-bus)
  - [SPI transfer](#spi-transfer)

## Usage <!-- omit in toc -->

### Flash ETP firmware

See [etplib README](https://github.com/embeddedcompany/etplib-python-next/blob/main/README.md#flashing-etp-firmware) for instructions on flashing the ETP firmware.

### Configure transport

```
etptool cfg save transport serial:COM4:115200
```
Replace `COM4` with the serial port of the ETP device.

### Verify connection & firmware version

```
etptool fw info
```

### GPIO

#### Get GPIO information

```
etptool gpio info
```

#### Initialize GPIO

- Configure GPIO pin `_13` as output
```
etptool gpio init _13:output
```

- Configure GPIO pin `_3` as input
```
etptool gpio init _3:input
```

#### Read GPIO

- Read GPIO pin `_3`
```
etptool gpio read _3
```

- Monitor GPIO pin `_3`
```
etptool gpio read --monitor _3
```

#### Write GPIO

- Write `1` to GPIO pin `_13`
```
etptool gpio write _13:1
```

- Write `0` to GPIO pin `_13`
```
etptool gpio write _13:0
```

> NOTE: On an Arduino board, `1` will turn *OFF* the LED and `0` will turn *ON* the LED.

### ADC

#### Get ADC information

```
etptool adc info
```

#### Initialize ADC

- Enable ADC pin `a0`
```
etptool adc init a0:en
```

- Disable ADC pin `a0`
```
etptool adc init a0:dis
```

#### Read ADC

- Read ADC pin `a0`
```
etptool adc read a0
```

- Monitor ADC pin `a0`
```
etptool adc read --monitor a0
```

### PWM

#### Get PWM information

```
etptool pwm info
```

#### Initialize PWM
```
etptool pwm init _3:en
```

#### Set PWM duty cycle
```
etptool pwm ctrl _3:50
```

### I2C

#### Get I2C information

```
etptool i2c info
```

#### Initialize I2C bus

- Initialize I2C bus 0 with 100 kHz speed
```
etptool i2c init 0 100
```

Alternatively, you can use `--bus` and `--speed` options
```
etptool i2c init --bus 0 --speed 100
```

#### Scan I2C bus

```
etptool i2c scan 0
```

or

```
etptool i2c scan --bus 0
```

#### I2C read

- Read 2 bytes from I2C device `0x68`

```
etptool i2c read 0 104 2
```
or

```
etptool i2c read --bus 0 --addr 104 --len 2
```

#### I2C Write

- Write 2 bytes to I2C device `0x68`

```
etptool i2c write 0 104 10 20
```

or

```
etptool i2c write --bus 0 --addr 104 --data 10 20
```

#### Register read I2C

- Read 4 bytes from I2C device `0x68` register `0x02`

```
etptool i2c read_reg 0 104 2 4
```

or

```
etptool i2c read_reg --bus 0 --addr 104 --reg 2 --len 4
```

#### Register write I2C

- Write 4 bytes to I2C device `0x68` register `0x02`

```

etptool i2c write_reg 0 104 2 10 20 30 40
```

or

```
etptool i2c write_reg --bus 0 --addr 104 --reg 2 --data 10 20 30 40
```

### SPI

#### Get SPI information

```
etptool spi info
```

#### Initialize SPI bus

- Initialize SPI bus 0 with 1 MHz speed and mode 0
```
etptool spi init 0 1000000 0
```

Alternatively, you can use `--bus`, `--speed`, and `--mode` options
```
etptool spi init --bus 0 --speed 1000000 --mode 0
```

#### SPI transfer

- Transfer 2 bytes on SPI bus 0
```
etptool spi transfer 0 10 20
```

or

```
etptool spi transfer --bus 0 --data 10 20
```