# pictureframe
An eink picture frame that automatically grabs photos from PhotoPrism.

Hardware requirements:
* A [Raspberry Pi], _without_ headers - a [Zero 2 W] works
* Some [extra long headers]
* An [Inky Impression 13.3"]
* A [Witty Pi 4 L3V7]
* A compatible battery, such as this [LiIon 3.7V 6600mAh]

## Installation
```bash
# clone
git clone --recurse-submodules https://github.com/bmatcuk/pictureframe.git
cd pictureframe/inky

# Install inky software
# When asked to copy the examples, answer "no"
# When asked to install dependencies for examples, answer "no"
# When asked to generate documentation, answer "no"
./install.sh

# Install pictureframe dependencies
source ~/.virtualenvs/pimoroni/bin/activate
cd ..
pip3 install -r requirements.txt
```

Next, copy the `.env.example` file to `.env` and edit it to include your
PhotoPrism API key.

[extra long headers]: https://www.amazon.com/dp/B07DJY6HT8?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1
[Inky Impression 13.3"]: https://shop.pimoroni.com/products/inky-impression-7-3?variant=55186435277179
[LiIon 3.7V 6600mAh]: https://www.adafruit.com/product/353
[Raspberry Pi]: https://www.raspberrypi.com/
[Witty Pi 4 L3V7]: https://www.adafruit.com/product/5705
[Zero 2 W]: https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/
