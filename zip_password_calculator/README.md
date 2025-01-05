# Calculate the password for a Hyundai/Kia `update_package.zip` file

As described in [this blog post](https://xakcop.com/post/hyundai-hack/) by the original author.

His settings are as follows:
```
ro.product.model=daudioplus
ro.product.brand=hyundai
ro.product.name=tlfl_eu
ro.product.device=daudiopluslow_tlfl_eu
ro.product.board=daudio
ro.product.cpu.abi=armeabi-v7a
ro.product.cpu.abi2=armeabi
ro.product.manufacturer=mobis
ro.product.locale.language=en
ro.product.locale.region=GB
```
Most of these values should be either static or guessable with a bit of detective work.

Example:
```sh
$ ./zip_password_calculator.sh build.prop.TEST
15DAA85C8D44B3979CD152A387F6
```

```sh
$ node ./zip_password_calculator.mjs build.prop.TEST
15DAA85C8D44B3979CD152A387F6
```

Run this tool against a file containing the settings for your head unit and get the password, potentially avoiding the need for `bkcrack`.

## USA region, Display Audio Gen 1 (without Nav)

Below you can find the passwords for the US versions of Hyundai and Kia Display Audio Gen 1 systems (without Nav) contributed by [@dracode](https://github.com/dracode).

### Kia

| Model | CodeName | Password |
|---|---|---|
| 2021 Sportage | ql21 | BCB60611A698181DA14BDFAB1A3E |
| 2018-19 Niro Plug-In Hybrid | dephev | 4478E55BE0BBE61E88AAACAC5E42 |
| 2017-2019 Optima | jfpe | F227C64CEF26B3A61B1C17474E20 |
| 2019-2020 Optima Hybrid | jfpehev | CBAACF9A9BA7C52646AC317AB633 |
| 2019-2020 Sportage | qlpe | 4E0BCC50EE902A3E52A514B86C81 |
| 2020 Telluride | on | DF1B2E573F9671D828B52E7A81B3 |
| 2019 Niro Electric | deev | 2D4A796BD01B08A927BDA2A444C1 |


### Hyundai

| Model | CodeName | Password |
|---|---|---|
| 2017-18 Elantra | adn | 3364B7EBD4FD897975B08F2CC489 |
| 2019-20 Elantra | adpe | 6A44DB6CCE1E2CEFF4E6B9C849E1 |
| 2017-19 Ioniq Electric | aeev | FC73F597B4D20C900FD342B446D9 |
| 2017-19 Ioniq Hybrid | aehev | B005DA3618E91BFi61A9D5F7F997A |
| 2020 Ioniq Electric | aepeev | 8344ADA46822DB2614D25394036A |
| 2020 Ioniq Hybrid | aepehev | 2BE5E0E4875216AF90DB667E43B9 |
| 2020 Ioniq Plug-In Hybrid | aepephev | CAC36CF64EDF95BCB9305D8E94D3 |
| 2018-19 Ioniq Plug-In Hybrid | aephev | 9A5330709463A18D504EEBD6D613 |
| 2019-21 Veloster | js | 5D920825E2A81862DF1C8B274870 |
| 2019-21 Veloster N | jsn | 93BDA8C21C411927F8E446F69B3B |
| 2018-19 Sonata | lffl | 2C6AEF5A4A531FAC3CD22FB973B4 |
| 2018-19 Sonata Hybrid | lfflhev | B82C9A9399B74891D1258DBAD4A2 |
| 2019 Sonata Plug-In Hybrid | lfflphev | EEE972FCCBBEEFD68E0A12181B27 |
| 2019 Kona | os19my | BF9A627B09FCC658C313D56CAF05 |
| 2019 Kona Electric | osev | 9E68A5EE79C27611BB20EDDA5393 |
| 2019-20 Tucson | tlfl | A65BECA9245C29233AB390144B50 |
| 2019-20 Santa Fe (5 seat) | tm | 0CDFDB6FE41291C58B55421F2D1B |
| 2017-18 Santa Fe | an | +Ekfrl51Qkshsk#@zpdhkdWkd~-f |
| 2016-17 Sonata | lf | +Ekfrl51Qkshsk#@zpdhkdWkd~-f |
| 2017 Sonata Hybrid | lfhev | +Ekfrl51Qkshsk#@zpdhkdWkd~-f |
| 2019 Santa Fe (7 seat) | nc | +Ekfrl51Qkshsk#@zpdhkdWkd~-f |
| 2017-18 Elantra | ad | +Ekfrl51Qkshsk#@zpdhkdWkd~-f |

## EUR region, Display Audio Gen 1 Plus (with Nav)

### Hyundai

| Vehicle | Model | CodeName | Password |
|---|---|---|---|
| i20 | 2018-20 i20 | gb | 6F5510C2134ECF51179C3AC9BCAA |
| Tucson | Tucson (TLe FL) | tlfl | 15DAA85C8D44B3979CD152A387F6 |
