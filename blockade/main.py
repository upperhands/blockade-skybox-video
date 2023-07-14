import bpy
import os
import math
import platform
import sys
import json


def getConfig(video_config_file: str = None) -> dict:
    if video_config_file:
        config: str = json.load(open(video_config_file))
        return config
    system: str = platform.system()
    if system == 'Windows':
        app_data: str = os.environ.get('AppData')
        config_dir: str = os.path.join(app_data, 'blockade-skybox-video')
    elif system == 'Linux':
        config_dir = os.path.join(
            os.path.expanduser('~'),
            '.config'
        )
    else:
        print('This platform is not supported yet!')
        sys.exit(1)

    config_file: str = os.path.join(config_dir, 'config.json')
    config: dict = json.load(open(config_file, 'r'))
    return config


def setCameraAnimation(config: dict) -> None:

    if bpy.context.scene.camera:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.camera.select_set(True)
        bpy.ops.object.delete()

    bpy.ops.object.camera_add(rotation=(math.radians(90), 0, 0))
    camera = bpy.context.object

    bpy.context.scene.camera = camera

    camera.rotation_mode = 'XYZ'

    number_of_frames: int = config['duration'] * config['fps']

    start_angle = config['start-angle']
    end_angle = config['end-angle']

    start_angle_rad = math.radians(start_angle)
    end_angle_rad = math.radians(end_angle)

    camera.rotation_euler[2] = start_angle_rad
    camera.keyframe_insert(data_path="rotation_euler", frame=1)

    camera.rotation_euler[2] = end_angle_rad
    camera.keyframe_insert(data_path="rotation_euler", frame=number_of_frames)

    for fcurve in camera.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'LINEAR'

    middle_frame = number_of_frames / 2
    start_focal_length = config['start-focal-length']
    mid_focal_length = config['mid-focal-length']
    end_focal_length = config['end-focal-length']

    camera.data.lens = start_focal_length
    camera.data.keyframe_insert(data_path="lens", frame=1)

    camera.data.lens = mid_focal_length
    camera.data.keyframe_insert(data_path="lens", frame=middle_frame)

    camera.data.lens = end_focal_length
    camera.data.keyframe_insert(data_path="lens", frame=number_of_frames)

    for fcurve in camera.data.animation_data.action.fcurves:
        if fcurve.data_path == 'lens':
            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = 'LINEAR'


def setSkyTexture(config: dict) -> None:
    world = bpy.context.scene.world
    node_tree = world.node_tree

    sky_nodes = [node for node in node_tree.nodes if node.type == 'TEX_SKY']
    node_tree.nodes.clear()
    for node in sky_nodes:
        node_tree.nodes.remove(node)

    bg_node = node_tree.nodes.new('ShaderNodeBackground')
    bg_node.location = (0, 0)

    output_node = node_tree.nodes.new('ShaderNodeOutputWorld')
    output_node.location = (400, 0)

    env_node = node_tree.nodes.new('ShaderNodeTexEnvironment')
    env_node.location = (200, 0)

    image = bpy.data.images.load(config['input'])
    env_node.image = image

    node_tree.links.new(env_node.outputs['Color'], bg_node.inputs['Color'])
    node_tree.links.new(
        bg_node.outputs['Background'], output_node.inputs['Surface'])

    node_tree.nodes.active = env_node


def deleteCollectionItems(collection_name: str, config: dict) -> None:
    scene = bpy.context.scene

    collection = scene.collection.children.get(collection_name)
    if collection is None:
        print(f"Collection '{collection_name}' not found.")
        return

    for obj in collection.objects:
        bpy.data.objects.remove(obj, do_unlink=True)

    print(f"All items in collection '{collection_name}' have been deleted.")


def setRenderingOptions(config: dict) -> None:
    bpy.context.scene.frame_end = config['duration'] * config['fps']
    bpy.context.scene.render.resolution_x = config['width']
    bpy.context.scene.render.resolution_y = config['height']
    bpy.context.scene.render.fps = config['fps']
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = config['format']
    bpy.context.scene.render.ffmpeg.codec = config['codec']
    bpy.context.scene.render.ffmpeg.constant_rate_factor \
        = config['constant-rate-factor']

    output_file = config['output']
    bpy.context.scene.render.filepath = output_file


def renderAnimation() -> None:
    bpy.ops.render.render(animation=True)


if __name__ == '__main__':
    try:
        video_config_file: str = sys.argv[sys.argv.index(
            '--blockade-config-file') + 1]
    except ValueError:
        video_config_file: str = None
        print('No file is provided, default config file will be used')
    config: dict = getConfig(video_config_file)
    setRenderingOptions(config)
    deleteCollectionItems('Collection', config)
    setSkyTexture(config)
    setCameraAnimation(config)
    print(bpy.context.scene.frame_end)
    print(bpy.context.scene.render.resolution_x)
    print(bpy.context.scene.render.resolution_y)
    print(bpy.context.scene.render.fps)
    print(bpy.context.scene.render.image_settings.file_format)
    print(bpy.context.scene.render.ffmpeg.format)
    print(bpy.context.scene.render.ffmpeg.codec)
    print(bpy.context.scene.render.ffmpeg.constant_rate_factor)
    renderAnimation()
