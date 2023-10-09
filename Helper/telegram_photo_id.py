'''@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f"ID данной картинки:\n{message.photo[-1].file_id}")'''