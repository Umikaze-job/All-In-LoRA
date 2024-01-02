from numpy import ndarray
from rembg import remove,new_session
from PIL import Image

async def character_trimming(base_image:Image.Image,data) -> Image.Image:
    session = new_session(data["modelname"])

    alpha_image:Image.Image = remove(base_image,session=session,alpha_matting=True,
                         alpha_matting_foreground_threshold=data["foreground_threshold"],
                         alpha_matting_background_threshold=data["background_threshold"],
                         alpha_matting_erode_size=data["erode_size"])
    # 一定値以下のアルファ値を0にするしきい値を設定
    threshold = 128  # この値を必要に応じて調整

    # 画像のアルファチャンネルを取得
    alpha_channel = alpha_image.split()[3]

    # 一定値以下のアルファ値を0に設定
    alpha_data = alpha_channel.getdata()
    new_alpha_data = [(0 if alpha <= threshold else alpha) for alpha in alpha_data]

    # 新しいアルファチャンネルを設定
    alpha_channel.putdata(new_alpha_data)

    # 元の画像に新しいアルファチャンネルを設定
    alpha_image.putalpha(alpha_channel)
    # ちょっと大きくする
    size = base_image.size
    alpha_box:tuple[int, int, int, int] = alpha_image.getbbox()

    margin = data["spread"]

    # 座標を個別に取り出して演算
    left = max(0, int(alpha_box[0]) - margin)
    top = max(0, int(alpha_box[1]) - margin)
    right = min(size[0], int(alpha_box[2]) + margin)
    bottom = min(size[1], int(alpha_box[3]) + margin)

    new_image = base_image.crop((left, top, right, bottom))
    # 新しい座標を使って画像を切り抜く
    return new_image