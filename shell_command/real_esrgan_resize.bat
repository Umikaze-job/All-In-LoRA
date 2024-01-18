call cd D:\ai\My_AI\dataset_edit\All-In-Lora\All-In-Lora 
call .\venv\Scripts\activate 
call cd D:\ai\My_AI\dataset_edit\All-In-Lora\All-In-Lora\tools\Real-ESRGAN
call python inference_realesrgan.py -i D:\ai\My_AI\dataset_edit\All-In-Lora\All-In-Lora\savefiles\data02\character_trimming_folder\temp\derestefeet01_face000.webp -o D:\ai\My_AI\dataset_edit\All-In-Lora\All-In-Lora\savefiles\data02\character_trimming_folder\temp -n RealESRGAN_x4plus_anime_6B -s 2
pause