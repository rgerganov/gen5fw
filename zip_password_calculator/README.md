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
```
$ ./zip_password_calculator.sh build.prop.TEST
15DAA85C8D44B3979CD152A387F6
```

Run this tool against a file containing the settings for your head unit and get the password, potentially avoiding the need for `bkcrack`.

