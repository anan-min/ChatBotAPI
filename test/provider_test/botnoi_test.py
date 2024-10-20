import pytest
import asyncio
from pathlib import Path
from app.providers.botnoi_provider import BotnoiProvider

@pytest.fixture
def provider():
    return BotnoiProvider()

@pytest.mark.asyncio
async def test_speech_synthesis_real_api(provider):
    text = "ทดสอบวันนี้อากาศดีมาก อย่าลืมออกไปเดินเล่นนะคะ"
    synthesized_audio = await provider.speech_synthesis(text)

    assert type(synthesized_audio) == bytes
    assert len(synthesized_audio) > 0