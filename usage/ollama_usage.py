import os 
import time
import csv
from pathlib import Path
from app.providers.ollama_provider import OllamaProvider
from app.utils.word_utils import count_thai_words
import asyncio



reports_path = Path(__file__).parent.parent / 'app' / 'data' / 'report' 
sample_voices_path = Path(__file__).parent.parent / 'app' / 'data' / 'sample' 
eng_questions =  [
        "What are the benefits of meditation?",
        "How does the stock market work?",
        "What is the impact of climate change on wildlife?",
        "Explain the theory of relativity in simple terms.",
        "What are some effective time management strategies?",
        "How does photosynthesis work in plants?",
        "What are the causes and effects of global warming?",
        "Can you describe the process of cellular respiration?",
        "What are the main differences between capitalism and socialism?",
        "How do vaccines work to protect against diseases?",
        "What are the key principles of design thinking?",
        "Explain the significance of the Magna Carta.",
        "What are the stages of human development?",
        "How does blockchain technology function?",
        "What are the advantages and disadvantages of renewable energy?",
        "What is the role of DNA in heredity?",
        "How do social media platforms affect communication?",
        "What are some tips for effective public speaking?",
        "Explain the concept of artificial intelligence.",
        "What are the historical roots of the Internet?",
        "How do different cultures view mental health?",
        "What are the major themes in Shakespeare's plays?",
        "How does the human brain process information?",
        "What is the importance of biodiversity in ecosystems?",
        "How do you measure economic growth?",
        "What are the effects of deforestation on the environment?",
        "Can you explain the process of natural selection?",
        "What are some common cognitive biases?",
        "How do cultural differences influence negotiation styles?",
        "What are the potential impacts of automation on jobs?",
        "Explain the significance of the scientific method.",
        "What are the main causes of poverty around the world?",
        "How does advertising influence consumer behavior?",
        "What is the history of the civil rights movement in the US?",
        "How do our emotions affect our decision-making?",
        "What are the principles of sustainable development?",
        "What is the role of government in regulating the economy?",
        "How does stress affect physical health?",
        "Explain the concept of supply and demand.",
        "What are the challenges of urbanization?",
        "How do different religions approach the concept of morality?",
        "What are the main theories of motivation in psychology?",
        "How do you define success in life?",
        "What is the relationship between education and income?",
        "How does globalization affect local cultures?",
        "What are the main functions of the immune system?",
        "Explain the process of photosynthesis.",
        "What are the key elements of effective leadership?",
        "How do you foster creativity in the workplace?",
        "What is the impact of social media on society?",
        "How do you create a budget and stick to it?",
        "What are the major advancements in medical technology?",
        "How does one become a successful entrepreneur?",
        "What are the effects of exercise on mental health?",
        "What are the key differences between qualitative and quantitative research?",
        "How do you effectively manage conflict in a team?",
        "What are the benefits of reading regularly?",
        "Explain the role of enzymes in biological reactions.",
        "What are the ethical implications of genetic engineering?",
        "How do you develop a growth mindset?",
        "What are the stages of group development?",
        "How does music influence human emotions?",
        "What is the significance of cultural heritage?",
        "How do you build strong relationships?",
        "What are the key components of a healthy diet?",
        "Explain the impact of technology on education.",
        "What are the characteristics of effective teams?",
        "How do you define and measure happiness?",
        "What are the major challenges facing the global economy?",
        "How does the brain control movement?",
        "What are the key principles of effective marketing?",
        "How does one achieve work-life balance?",
        "What are the historical milestones in the fight for women's rights?",
        "How do you identify and overcome limiting beliefs?",
        "What are the environmental impacts of fast fashion?",
        "How does one effectively set and achieve goals?",
        "What are the key features of democratic governance?",
        "How do psychological factors influence consumer spending?",
        "What are the implications of climate change for future generations?",
        "How do you create a positive workplace culture?",
        "What are the benefits of volunteering?",
        "Explain the significance of emotional intelligence.",
        "What are the key elements of a successful marketing strategy?",
        "How does one develop resilience in the face of adversity?",
        "What are the psychological effects of trauma?",
        "What is the significance of art in society?",
        "How do you foster inclusivity in the workplace?",
        "What are the main components of a balanced diet?",
        "Explain the role of government in public health.",
        "What are the effects of media on public perception?",
        "How do you create an effective learning environment?",
        "What are the benefits of critical thinking?",
        "How does one manage time effectively?",
        "What are the key factors that contribute to poverty?",
        "How do cultural norms shape behavior?",
        "What is the impact of urban design on community well-being?",
        "How does one develop effective study habits?",
        "What are the ethical challenges in business?",
        "How does one cultivate empathy in relationships?",
        "What are the benefits of lifelong learning?",
        "What are the benefits of meditation?",
        "How does the stock market work?",
        "What is the impact of climate change on wildlife?",
        "Explain the theory of relativity in simple terms.",
        "What are some effective time management strategies?",
        "How does photosynthesis work in plants?",
        "What are the causes and effects of global warming?",
        "Can you describe the process of cellular respiration?",
        "What are the main differences between capitalism and socialism?",
        "How do vaccines work to protect against diseases?",
        "What are the key principles of design thinking?",
        "Explain the significance of the Magna Carta.",
        "What are the stages of human development?",
        "How does blockchain technology function?",
        "What are the advantages and disadvantages of renewable energy?",
        "What is the role of DNA in heredity?",
        "How do social media platforms affect communication?",
        "What are some tips for effective public speaking?",
        "Explain the concept of artificial intelligence.",
        "What are the historical roots of the Internet?",
        "How do different cultures view mental health?",
        "What are the major themes in Shakespeare's plays?",
        "How does the human brain process information?",
        "What is the importance of biodiversity in ecosystems?",
        "How do you measure economic growth?",
        "What are the effects of deforestation on the environment?",
        "Can you explain the process of natural selection?",
        "What are some common cognitive biases?",
        "How do cultural differences influence negotiation styles?",
        "What are the potential impacts of automation on jobs?",
        "Explain the significance of the scientific method.",
        "What are the main causes of poverty around the world?",
        "How does advertising influence consumer behavior?",
        "What is the history of the civil rights movement in the US?",
        "How do our emotions affect our decision-making?",
        "What are the principles of sustainable development?",
        "What is the role of government in regulating the economy?",
        "How does stress affect physical health?",
        "Explain the concept of supply and demand.",
        "What are the challenges of urbanization?",
        "How do different religions approach the concept of morality?",
        "What are the main theories of motivation in psychology?",
        "How do you define success in life?",
        "What is the relationship between education and income?",
        "How does globalization affect local cultures?",
        "What are the main functions of the immune system?",
        "Explain the process of photosynthesis.",
        "What are the key elements of effective leadership?",
        "How do you foster creativity in the workplace?",
        "What is the impact of social media on society?",
        "How do you create a budget and stick to it?",
        "What are the major advancements in medical technology?",
        "How does one become a successful entrepreneur?",
        "What are the effects of exercise on mental health?",
        "What are the key differences between qualitative and quantitative research?",
        "How do you effectively manage conflict in a team?",
        "What are the benefits of reading regularly?",
        "Explain the role of enzymes in biological reactions.",
        "What are the ethical implications of genetic engineering?",
        "How do you develop a growth mindset?",
        "What are the stages of group development?",
        "How does music influence human emotions?",
        "What is the significance of cultural heritage?",
        "How do you build strong relationships?",
        "What are the key components of a healthy diet?",
        "Explain the impact of technology on education.",
        "What are the characteristics of effective teams?",
        "How do you define and measure happiness?",
        "What are the major challenges facing the global economy?",
        "How does the brain control movement?",
        "What are the key principles of effective marketing?",
        "How does one achieve work-life balance?",
        "What are the historical milestones in the fight for women's rights?",
        "How do you identify and overcome limiting beliefs?",
        "What are the environmental impacts of fast fashion?",
        "How does one effectively set and achieve goals?",
        "What are the key features of democratic governance?",
        "How do psychological factors influence consumer spending?",
        "What are the implications of climate change for future generations?",
        "How do you create a positive workplace culture?",
        "What are the benefits of volunteering?",
        "Explain the significance of emotional intelligence.",
        "What are the key elements of a successful marketing strategy?",
        "How does one develop resilience in the face of adversity?",
        "What are the psychological effects of trauma?",
        "What is the significance of art in society?",
        "How do you foster inclusivity in the workplace?",
        "What are the main components of a balanced diet?",
        "Explain the role of government in public health.",
        "What are the effects of media on public perception?",
        "How do you create an effective learning environment?",
        "What are the benefits of critical thinking?",
        "How does one manage time effectively?",
        "What are the key factors that contribute to poverty?",
        "How do cultural norms shape behavior?",
        "What is the impact of urban design on community well-being?",
        "How does one develop effective study habits?",
        "What are the ethical challenges in business?",
        "How does one cultivate empathy in relationships?",
        "What are the benefits of lifelong learning?"
    ]
th_questions = [
        "การทำสมาธิมีประโยชน์อย่างไร?",
        "ตลาดหุ้นทำงานอย่างไร?",
        "การเปลี่ยนแปลงสภาพภูมิอากาศส่งผลกระทบต่อสิ่งมีชีวิตอย่างไร?",
        "อธิบายทฤษฎีสัมพัทธ์ในแบบที่เข้าใจง่าย.",
        "กลยุทธ์การบริหารเวลาที่มีประสิทธิภาพมีอะไรบ้าง?",
        "การสังเคราะห์แสงทำงานอย่างไรในพืช?",
        "สาเหตุและผลกระทบของภาวะโลกร้อนคืออะไร?",
        "คุณสามารถอธิบายกระบวนการหายใจในเซลล์ได้ไหม?",
        "ความแตกต่างระหว่างระบบเศรษฐกิจทุนนิยมและสังคมนิยมคืออะไร?",
        "วัคซีนทำงานอย่างไรเพื่อป้องกันโรค?",
        "หลักการสำคัญของการคิดเชิงออกแบบคืออะไร?",
        "อธิบายความสำคัญของรัฐธรรมนูญ.",
        "มีขั้นตอนอะไรบ้างในพัฒนาการของมนุษย์?",
        "เทคโนโลยีบล็อกเชนทำงานอย่างไร?",
        "ข้อดีและข้อเสียของพลังงานทดแทนมีอะไรบ้าง?",
        "DNA มีบทบาทอย่างไรในพันธุกรรม?",
        "แพลตฟอร์มโซเชียลมีเดียมีผลต่อการสื่อสารอย่างไร?",
        "มีเคล็ดลับอะไรบ้างสำหรับการพูดในที่สาธารณะอย่างมีประสิทธิภาพ?",
        "อธิบายแนวคิดของปัญญาประดิษฐ์.",
        "รากฐานทางประวัติศาสตร์ของอินเทอร์เน็ตคืออะไร?",
        "วัฒนธรรมต่างๆ มองสุขภาพจิตอย่างไร?",
        "ธีมหลักในบทละครของเช็คสเปียร์มีอะไรบ้าง?",
        "สมองของมนุษย์ประมวลผลข้อมูลอย่างไร?",
        "ความสำคัญของความหลากหลายทางชีวภาพในระบบนิเวศคืออะไร?",
        "คุณวัดการเติบโตทางเศรษฐกิจได้อย่างไร?",
        "ผลกระทบของการตัดไม้ทำลายป่าต่อสิ่งแวดล้อมมีอะไรบ้าง?",
        "คุณสามารถอธิบายกระบวนการคัดเลือกตามธรรมชาติได้ไหม?",
        "มีอคติทางความคิดที่พบบ่อยอะไรบ้าง?",
        "ความแตกต่างทางวัฒนธรรมมีผลต่อรูปแบบการเจรจาอย่างไร?",
        "ผลกระทบที่เป็นไปได้ของการใช้เทคโนโลยีอัตโนมัติต่ออาชีพคืออะไร?",
        "อธิบายความสำคัญของวิธีวิทยาศาสตร์.",
        "สาเหตุหลักของความยากจนทั่วโลกมีอะไรบ้าง?",
        "โฆษณามีอิทธิพลต่อพฤติกรรมของผู้บริโภคอย่างไร?",
        "ประวัติศาสตร์ของการเคลื่อนไหวสิทธิพลเมืองในสหรัฐอเมริกาคืออะไร?",
        "อารมณ์ของเรามีผลต่อการตัดสินใจอย่างไร?",
        "หลักการของการพัฒนาที่ยั่งยืนคืออะไร?",
        "รัฐบาลมีบทบาทอย่างไรในการควบคุมเศรษฐกิจ?",
        "ความเครียดมีผลกระทบต่อสุขภาพร่างกายอย่างไร?",
        "อธิบายแนวคิดของอุปสงค์และอุปทาน.",
        "ความท้าทายของการเมืองเมืองคืออะไร?",
        "ศาสนาต่างๆ มีแนวทางอย่างไรต่อแนวคิดด้านศีลธรรม?",
        "ทฤษฎีหลักของแรงจูงใจในจิตวิทยามีอะไรบ้าง?",
        "คุณนิยามความสำเร็จในชีวิตอย่างไร?",
        "ความสัมพันธ์ระหว่างการศึกษาและรายได้คืออะไร?",
        "โลกาภิวัตน์มีผลต่อวัฒนธรรมท้องถิ่นอย่างไร?",
        "หน้าที่หลักของระบบภูมิคุ้มกันคืออะไร?",
        "อธิบายกระบวนการสังเคราะห์แสง.",
        "องค์ประกอบหลักของการเป็นผู้นำที่มีประสิทธิภาพคืออะไร?",
        "คุณกระตุ้นความคิดสร้างสรรค์ในที่ทำงานอย่างไร?",
        "โซเชียลมีเดียมีผลกระทบต่อสังคมอย่างไร?",
        "คุณสร้างงบประมาณและปฏิบัติตามได้อย่างไร?",
        "ความก้าวหน้าทางเทคโนโลยีทางการแพทย์มีอะไรบ้าง?",
        "ทำไมคนถึงเป็นผู้ประกอบการที่ประสบความสำเร็จ?",
        "การออกกำลังกายมีผลต่อสุขภาพจิตอย่างไร?",
        "ความแตกต่างระหว่างการวิจัยเชิงคุณภาพและเชิงปริมาณคืออะไร?",
        "คุณจัดการความขัดแย้งในทีมได้อย่างไร?",
        "การอ่านหนังสือมีประโยชน์อย่างไร?",
        "อธิบายบทบาทของเอนไซม์ในปฏิกิริยาชีวภาพ.",
        "ข้อกฎหมายด้านจริยธรรมของการตัดต่อพันธุกรรมมีอะไรบ้าง?",
        "คุณพัฒนากรอบความคิดที่ดีได้อย่างไร?",
        "มีขั้นตอนอะไรบ้างในการพัฒนากลุ่ม?",
        "ดนตรีมีอิทธิพลต่ออารมณ์ของมนุษย์อย่างไร?",
        "ความสำคัญของมรดกทางวัฒนธรรมคืออะไร?",
        "คุณสร้างความสัมพันธ์ที่แข็งแกร่งได้อย่างไร?",
        "ส่วนประกอบหลักของอาหารที่มีสุขภาพดีคืออะไร?",
        "อธิบายผลกระทบของเทคโนโลยีต่อการศึกษา.",
        "ลักษณะของทีมที่มีประสิทธิภาพมีอะไรบ้าง?",
        "คุณนิยามและวัดความสุขได้อย่างไร?",
        "ความท้าทายที่สำคัญในเศรษฐกิจโลกคืออะไร?",
        "สมองควบคุมการเคลื่อนไหวได้อย่างไร?",
        "หลักการสำคัญของการตลาดที่มีประสิทธิภาพคืออะไร?",
        "คุณสร้างสมดุลระหว่างงานและชีวิตได้อย่างไร?",
        "เหตุการณ์สำคัญในประวัติศาสตร์การต่อสู้เพื่อสิทธิสตรีมีอะไรบ้าง?",
        "คุณระบุและเอาชนะความเชื่อที่จำกัดได้อย่างไร?",
        "ผลกระทบต่อสิ่งแวดล้อมจากแฟชั่นที่รวดเร็วคืออะไร?",
        "คุณตั้งเป้าหมายและบรรลุเป้าหมายได้อย่างไร?",
        "ลักษณะสำคัญของการปกครองระบอบประชาธิปไตยมีอะไรบ้าง?",
        "ปัจจัยทางจิตวิทยามีอิทธิพลต่อการใช้จ่ายของผู้บริโภคอย่างไร?",
        "ผลกระทบของการเปลี่ยนแปลงสภาพภูมิอากาศต่อคนรุ่นถัดไปคืออะไร?",
        "คุณสร้างวัฒนธรรมการทำงานที่ดีได้อย่างไร?",
        "ประโยชน์ของการทำงานอาสาสมัครคืออะไร?",
        "อธิบายความสำคัญของความฉลาดทางอารมณ์.",
        "ส่วนประกอบหลักของกลยุทธ์การตลาดที่ประสบความสำเร็จคืออะไร?",
        "คุณพัฒนาความยืดหยุ่นในเผชิญกับความยากลำบากได้อย่างไร?",
        "ผลกระทบทางจิตวิทยาของการบาดเจ็บคืออะไร?",
        "ความสำคัญของศิลปะในสังคมคืออะไร?",
        "คุณส่งเสริมความหลากหลายได้อย่างไรในที่ทำงาน?",
        "ส่วนประกอบหลักของอาหารที่สมดุลคืออะไร?",
        "อธิบายบทบาทของรัฐบาลในสุขภาพประชาชน.",
        "ผลกระทบของสื่อที่มีต่อการรับรู้ของประชาชนคืออะไร?",
        "คุณสร้างสภาพแวดล้อมการเรียนรู้ที่มีประสิทธิภาพได้อย่างไร?",
        "ประโยชน์ของการคิดอย่างมีวิจารณญาณคืออะไร?",
        "คุณจัดการเวลาอย่างมีประสิทธิภาพได้อย่างไร?",
        "ปัจจัยสำคัญที่ส่งผลต่อความยากจนคืออะไร?",
        "บรรทัดฐานทางวัฒนธรรมมีผลต่อพฤติกรรมอย่างไร?",
        "ผลกระทบของการออกแบบเมืองต่อความเป็นอยู่ของชุมชนคืออะไร?",
        "คุณพัฒนานิสัยการเรียนที่มีประสิทธิภาพได้อย่างไร?",
        "ความท้าทายในด้านธุรกิจมีอะไรบ้าง?",
        "คุณพัฒนาความเห็นอกเห็นใจในความสัมพันธ์ได้อย่างไร?",
        "ประโยชน์ของการเรียนรู้ตลอดชีวิตคืออะไร?"
    ]

questions = th_questions + eng_questions


def is_thai(text):
    """Check if the given text contains Thai characters."""
    for char in text:
        if '\u0E00' <= char <= '\u0E7F':
            return True
    return False

async def ollama_report():
    csv_filename = 'ollama_report.csv'
    csv_file_path =  reports_path / csv_filename # Store in the current directory

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Input Text', 'Provider', 'Model', 
                         'Time Taken (s)', 'Input Word Count', 
                         'Output Word Count', 'Language'])

        for question in questions:
            language = ('English' if not is_thai(question) else 'Thai')
            await process_and_write_row(writer, question, language)

            print(f"Processed question: {question} | Language: {language}")

        # Optionally, flush writer at the end to ensure all data is written

    print(f'Report generated at: {csv_file_path}')

async def process_and_write_row(writer, question, language):
    """Query the question and write the result to the CSV."""
    ollama = OllamaProvider()
    # Query Ollama for the response
    start_time = time.time()
    response = await ollama.query_text_file(text=question)
    time_taken = time.time() - start_time
    print("time taken", time_taken)

    # Extract provider and model details
    provider = 'Ollama'
    model = 'llama3.2 3b latest 2GB'

    # Calculate word counts
    input_word_count = (
        len(question.split()) if language == 'English' else count_thai_words(question)
    )
    output_word_count = (
        len(response.split()) if language == 'English' else count_thai_words(response)
    )

    # Write the data to the CSV
    writer.writerow([
        question, provider, model, time_taken, 
        input_word_count, output_word_count, language
    ])
    
    # Flush after each write (optional)



if __name__ == '__main__':
    print(reports_path)
    asyncio.run(ollama_report())