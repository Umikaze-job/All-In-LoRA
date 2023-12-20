from rembg import remove,new_session
from PIL import Image

async def character_trimming(file_path,output_path,model_name,margin):
    session = new_session(model_name)

    alpha_image = remove(Image.open(file_path),session=session)
    
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
    size = Image.open(file_path).size
    alpha_box = alpha_image.getbbox()

    # 座標を個別に取り出して演算
    left = max(0, int(alpha_box[0]) - margin)
    top = max(0, int(alpha_box[1]) - margin)
    right = min(size[0], int(alpha_box[2]) + margin)
    bottom = min(size[1], int(alpha_box[3]) + margin)

    # 新しい座標を使って画像を切り抜く
    image = Image.open(file_path).crop((left, top, right, bottom))

    image.save(output_path)  # PIL画像オブジェクトを指定のフォルダに保存