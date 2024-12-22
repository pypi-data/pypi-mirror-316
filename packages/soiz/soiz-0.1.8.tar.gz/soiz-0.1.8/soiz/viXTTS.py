# -*- coding: utf-8 -*-
import os
import sys
import locale
import torch
import torchaudio
from keys.modules.TTS.tts.configs.xtts_config import XttsConfig
from keys.modules.TTS.tts.models.xtts import Xtts
from vinorm import TTSnorm
import time

# Cấu hình encoding cho Windows
if sys.platform.startswith("win"):
    # Đặt encoding cho console
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    # Thử set locale cho Windows
    try:
        locale.setlocale(locale.LC_ALL, "Vietnamese_Vietnam.1258")
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, "vi_VN.UTF-8")
        except locale.Error:
            try:
                locale.setlocale(locale.LC_ALL, "")  # Sử dụng default locale
            except locale.Error:
                print("Warning: Không thể đặt locale, sử dụng locale mặc định")


class LocalTTS:
    def __init__(self):
        # Đường dẫn tới thư mục chứa model
        self.checkpoint_dir = "model/"

        # Kiểm tra và tạo thư mục model nếu chưa có
        os.makedirs(self.checkpoint_dir, exist_ok=True)

        # Load config
        xtts_config = os.path.join(self.checkpoint_dir, "config.json")
        self.config = XttsConfig()
        self.config.load_json(xtts_config)

        # Khởi tạo model
        self.model = Xtts.init_from_config(self.config)
        self.model.load_checkpoint(
            self.config, checkpoint_dir=self.checkpoint_dir, use_deepspeed=False
        )

        # Chuyển model lên GPU nếu có
        if torch.cuda.is_available():
            self.model.cuda()

        # Thêm ngôn ngữ tiếng Việt nếu chưa có
        self.supported_languages = self.config.languages
        if "vi" not in self.supported_languages:
            self.supported_languages.append("vi")

    def normalize_vietnamese_text(self, text):
        """
        Chuẩn hóa văn bản tiếng Việt và chuyển đổi số thành chữ
        """
        try:
            # Đảm bảo text là UTF-8
            if isinstance(text, bytes):
                text = text.decode("utf-8")

            # Dictionary ánh xạ số sang chữ
            number_mapping = {
                "0": "Không ",
                "1": "Một ",
                "2": "Hai ",
                "3": "Ba ",
                "4": "Bốn ",
                "5": "Năm ",
                "6": "Sáu ",
                "7": "Bảy ",
                "8": "Tám ",
                "9": "Chín ",
            }

            # Thay thế số bằng chữ trước
            for digit, word in number_mapping.items():
                text = text.replace(digit, word)

            # Sau đó mới normalize
            normalized = (
                text.replace("..", ".")
                .replace("!.", "!")
                .replace("?.", "?")
                .replace(" .", ".")
                .replace(" ,", ",")
                .replace('"', "")
                .replace("'", "")
                .replace("AI", "Ây Ai")
                .replace("A.I", "Ây Ai")
            )

            return normalized

        except Exception as e:
            print(f"Error normalizing text: {str(e)}")
            return text  # Trả về text gốc nếu có lỗi

    def calculate_keep_len(self, text, lang):
        """Tính toán độ dài giữ lại cho câu ngắn"""
        if lang in ["ja", "zh-cn"]:
            return -1

        word_count = len(text.split())
        num_punct = (
            text.count(".") + text.count("!") + text.count("?") + text.count(",")
        )

        if word_count < 5:
            return 15000 * word_count + 2000 * num_punct
        elif word_count < 10:
            return 13000 * word_count + 2000 * num_punct
        return -1

    def generate_speech(
        self,
        text,
        language="vi",
        reference_audio="model/samples/nu-luu-loat.wav",
        normalize_text=True,
        output_path="output.wav",
    ):
        """
        Tạo file âm thanh từ văn bản

        Parameters:
        - text: văn bản cần chuyển thành giọng nói
        - language: ngôn ngữ của văn bản (mặc định: "vi")
        - reference_audio: đường dẫn tới file âm thanh tham chiếu
        - normalize_text: có chuẩn hóa văn bản tiếng Việt hay không
        - output_path: đường dẫn lưu file âm thanh đầu ra
        """
        try:
            # Kiểm tra ngôn ngữ hợp lệ
            if language not in self.supported_languages:
                raise ValueError(f"Ngôn ngữ {language} không được hỗ trợ")

            # Kiểm tra độ dài văn bản
            if len(text) < 2:
                raise ValueError("Văn bản quá ngắn")

            # Đảm bảo text là UTF-8
            if isinstance(text, bytes):
                text = text.decode("utf-8")

            # Lấy conditioning latents
            t_latent = time.time()
            gpt_cond_latent, speaker_embedding = self.model.get_conditioning_latents(
                audio_path=reference_audio,
                gpt_cond_len=30,
                gpt_cond_chunk_len=4,
                max_ref_length=60,
            )

            # Chuẩn hóa văn bản nếu cần
            if normalize_text and language == "vi":
                text = self.normalize_vietnamese_text(text)

            print("Đang tạo âm thanh...")
            t0 = time.time()

            # Tạo âm thanh
            out = self.model.inference(
                text,
                language,
                gpt_cond_latent,
                speaker_embedding,
                repetition_penalty=5.0,
                temperature=0.75,
                enable_text_splitting=True,
            )

            # Tính thời gian xử lý
            inference_time = time.time() - t0
            print(f"Thời gian tạo âm thanh: {round(inference_time*1000)} milliseconds")

            # Tính real-time factor
            real_time_factor = (time.time() - t0) / out["wav"].shape[-1] * 24000
            print(f"Real-time factor (RTF): {real_time_factor:.2f}")

            # Điều chỉnh độ dài cho câu ngắn
            keep_len = self.calculate_keep_len(text, language)
            if keep_len > 0:
                out["wav"] = out["wav"][:keep_len]

            # Đảm bảo output_path là UTF-8
            if isinstance(output_path, bytes):
                output_path = output_path.decode("utf-8")

            # Lưu file âm thanh
            try:
                torchaudio.save(
                    str(output_path),  # Convert to string to avoid path issues
                    torch.tensor(out["wav"]).unsqueeze(0),
                    24000,
                )
                print(f"Đã lưu file âm thanh tại: {output_path}")
                return True
            except Exception as e:
                print(f"Lỗi khi lưu file âm thanh: {str(e)}")
                # Thử lưu với tên file không dấu
                import unicodedata

                output_path_ascii = (
                    unicodedata.normalize("NFKD", output_path)
                    .encode("ASCII", "ignore")
                    .decode("ASCII")
                )
                torchaudio.save(
                    str(output_path_ascii), torch.tensor(out["wav"]).unsqueeze(0), 24000
                )
                print(
                    f"Đã lưu file âm thanh với tên không dấu tại: {output_path_ascii}"
                )
                return True

        except Exception as e:
            print(f"Lỗi: {str(e)}")
            return False


# Ví dụ sử dụng
if __name__ == "__main__":
    # Khởi tạo TTS
    tts = LocalTTS()

    # Văn bản mẫu
    text = """Định lý Bayes: Lý tưởng hợp lý
    Định lý Bayes có lẽ là điều quan trọng nhất mà bất kỳ người muốn trở thành người lý trí nào cũng có thể học được. Rất nhiều cuộc tranh luận và bất đồng quan điểm mà chúng ta đưa ra là vì chúng ta không hiểu định lý Bayes, hoặc lý trí của con người thường hoạt động như thế nào.

    Định lý Bayes được đặt theo tên của nhà toán học Thomas Bayes vào thế kỷ 18 và về cơ bản, đây là công thức đặt ra câu hỏi: Khi bạn được trình bày với tất cả bằng chứng về một điều gì đó, bạn nên tin vào điều đó đến mức nào?

    Định lý Bayes dạy chúng ta rằng niềm tin của chúng ta không cố định; chúng là xác suất. Niềm tin của chúng ta thay đổi khi chúng ta cân nhắc bằng chứng mới so với các giả định của mình, hay "tiền nghiệm" của mình. Nói cách khác, tất cả chúng ta đều mang theo mình những ý tưởng nhất định về cách thế giới vận hành và bằng chứng mới sẽ thách thức chúng ta. Ví dụ, ai đó có thể tin rằng "hút thuốc là an toàn", rằng "Vitamin C ngăn ngừa bệnh tật" hoặc rằng "hoạt động của con người không liên quan đến biến đổi khí hậu". Đây là những tiền nghiệm của họ: niềm tin hiện tại của họ, được hình thành bởi văn hóa, thành kiến và thông tin mà họ đã gặp phải."""

    # Tạo âm thanh
    tts.generate_speech(
        text=text,
        language="vi",
        reference_audio="model/samples/nu-calm.wav",
        normalize_text=True,
        output_path="output.wav",
    )
