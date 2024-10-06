from app.providers.botnoi_provider import BotnoiProvider
from pathlib import Path
from app.providers.amazon_provider import AmazonProvider


SAVE_PATH = Path(__file__).parent.parent / 'app' / 'data' / 'test' / 'speech.wav'


AUDIO_FILE_PATH = Path(__file__).parent.parent / 'app' / 'data' / 'test' / 'voice.wav'

thai_text = """แน่นอน! นี่คือประโยคภาษาไทยที่ยาวและซับซ้อนสำหรับใช้ในการทดสอบระบบสังเคราะห์เสียงพูด:

"ในวันที่อากาศสดใสและท้องฟ้าแจ่มใสนั้น กลุ่มนักเรียนจากโรงเรียนประจำจังหวัดได้ออกเดินทางไปยังสวนสาธารณะเพื่อทำกิจกรรมการเรียนรู้นอกห้องเรียน ซึ่งรวมถึงการเล่นเกมที่ส่งเสริมการทำงานเป็นทีม การสำรวจธรรมชาติ การวาดภาพ และการเรียนรู้เกี่ยวกับพืชและสัตว์ต่างๆ ในสวนสาธารณะนั้น นอกจากจะเป็นการเสริมสร้างทักษะและความรู้แล้วยังเป็นโอกาสที่ดีในการสร้างความสัมพันธ์ที่ดีกับเพื่อนร่วมชั้นและครูผู้สอนอีกด้วย"""


if __name__ == '__main__':
    botnoi = BotnoiProvider()
    botnoi.download_audio_file(botnoi.speech_synthesis(thai_text), SAVE_PATH)

    amazon = AmazonProvider('speech-to-text-storage')
    transcribe_text = amazon.transcribe_audio_file(SAVE_PATH)
    print(transcribe_text)
