from app.modules.Chatbot_core.chatbot_model import llm_model, load_chromadb
import asyncio

chromadb_path="app/db"
embedding_model="all-MiniLM-L6-v2"
async def test():
    vectordb = load_chromadb(chromadb_path, embedding_model)
    # data = " trần tuân đạt, bệnh lý, nhức đầu, thuốc paradon extra: uống 1 ngày 2 lần mỗi lần một viên, pradone cetamon uống 2 lần 1 ngày sáng tối mỗi lần 1 ống, bác sĩ: lê thị hoa, bệnh viện hùng vương. lưu ý không dùng quá liều ảnh hưởng đến sức khỏe, uống từ ngày 18/2/2024 29/2/2024"
    data = "Bostccet Buxton"
    data_gen = await llm_model.data_generator(data, vectordb)
    # data_final = await llm_model.Json_tracking("dattran", "0001", data_gen)
    # print("Data final: ", data_final)
    print(data_gen)

asyncio.run(test())
