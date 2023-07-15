# blockade-skybox-video
Convert your skybox images created using [Blockade Skybox](https://skybox.blockadelabs.com/) to videos!
<div align="center">
    <img src="https://api-documentation.blockadelabs.com/img/logo.jpg" width="200" />
    <img src="https://pingvinus.ru/cr_images/modelImage/application/587-logo-Blender.png" width="200" />
</div>

## Example Usage
```
$ python -m src.main -i {path to your skybox image} -o {path to output video} --config-file {path to config file}
```

### Example Config File
```json
{
	"width": 1920,
	"height": 1080,
	"fps": 60,
	"duration": 10,
	"format": "MPEG4",
	"constant-rate-factor": "HIGH",
	"start-angle": 20,
	"end-angle": 40,
	"start-focal-length": 10,
	"mid-focal-length": 30,
	"end-focal-length": 10,
	"blender": "C:\\Program Files\\Blender Foundation\\Blender 3.6\\blender.exe"
}
```

### Run without config file
```sh
usage: Blockade Skybox Video Converter [-h] --input INPUT [--config-file CONFIG_FILE] [--output OUTPUT] [--height HEIGHT] [--fps FPS] [--duration DURATION] [--format FORMAT]
                                       [--codec CODEC] [--constant-rate-factor CONSTANT_RATE_FACTOR] [--start-angle START_ANGLE] [--end-angle END_ANGLE]
                                       [--start-focal-length START_FOCAL_LENGTH] [--mid-focal-length MID_FOCAL_LENGTH] [--end-focal-length END_FOCAL_LENGTH]
                                       [--save-config-file SAVE_CONFIG_FILE] [--blender BLENDER] [--path-to-script PATH_TO_SCRIPT]
```

## Example Video


https://github.com/upperhands/blockade-skybox-video/assets/107340417/6c8775de-2d93-41a7-bb37-42deb7a39cc4


## Thanks!
Thanks for visiting Blockade Skybox Video Converter! I don't really know much about Blender. With that in mind, I've made this video converter to help people who don't know much about Blender (just like me) to convert their skybox images to videos! If you have any feature requests, please feel free to open up an issue. If you liked this project, you can leave a star :star:! If you would like to contribute, you should feel free to do so!

Thanks again!
