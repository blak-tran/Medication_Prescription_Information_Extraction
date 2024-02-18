from app.modules.Chatbot_core.chatbot_model import llm_model
import asyncio
async def test():
    data = " trần tuân đạt, bệnh lý, nhức đầu, thuốc paradon extra: uống 1 ngày 2 lần mỗi lần một viên, pradone cetamon uống 2 lần 1 ngày sáng tối mỗi lần 1 ống, bác sĩ: lê thị hoa, bệnh viện hùng vương. lưu ý không dùng quá liều ảnh hưởng đến sức khỏe, uống từ ngày 18/2/2024 29/2/2024"
    data_gen = await llm_model.data_generator(data)
    data_final = await llm_model.Json_tracking("dattran", "0001", data_gen)
    print("Data final: ", data_final)

asyncio.run(test())
