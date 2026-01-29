"""
Property-based tests for use cases.

Tests use case properties and idempotency using Hypothesis.
"""

from pathlib import Path
from unittest.mock import Mock

import pytest
from app.use_cases.create_voice_profile import CreateVoiceProfileUseCase
from app.use_cases.generate_audio import GenerateAudioUseCase
from app.use_cases.list_voice_profiles import ListVoiceProfilesUseCase
from domain.exceptions import InvalidSampleException
from domain.models.audio_sample import AudioSample
from domain.models.voice_profile import VoiceProfile
from domain.ports.audio_processor import AudioProcessor
from domain.ports.profile_repository import ProfileRepository
from domain.ports.tts_engine import TTSEngine
from hypothesis import given
from hypothesis import strategies as st


class TestCreateVoiceProfileProperties:
    """Property-based tests for CreateVoiceProfileUseCase."""

    @pytest.fixture
    def mock_audio_processor(self):
        """Create a mock audio processor."""
        processor = Mock(spec=AudioProcessor)
        processor.validate_sample.return_value = True
        processor.process_sample.return_value = AudioSample(
            file_path=Path("test.wav"),
            duration=10.0,
            sample_rate=12000,
            channels=1,
            bit_depth=16,
        )
        return processor

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository."""
        repository = Mock(spec=ProfileRepository)
        repository.save.return_value = None
        return repository

    @given(
        name=st.text(
            min_size=1, max_size=50, alphabet=st.characters(blacklist_characters="\x00")
        ),
        sample_count=st.integers(min_value=1, max_value=5),
    )
    def test_create_profile_preserves_name(
        self, mock_audio_processor, mock_repository, name, sample_count
    ):
        """Property: Created profile should preserve the given name."""
        use_case = CreateVoiceProfileUseCase(
            audio_processor=mock_audio_processor, profile_repository=mock_repository
        )

        sample_paths = [Path(f"sample_{i}.wav") for i in range(sample_count)]

        result = use_case.execute(name=name, sample_paths=sample_paths)

        assert result.name == name

    @given(sample_count=st.integers(min_value=1, max_value=10))
    def test_create_profile_sample_count_matches(
        self, mock_audio_processor, mock_repository, sample_count
    ):
        """Property: Created profile should have correct number of samples."""
        use_case = CreateVoiceProfileUseCase(
            audio_processor=mock_audio_processor, profile_repository=mock_repository
        )

        sample_paths = [Path(f"sample_{i}.wav") for i in range(sample_count)]

        result = use_case.execute(name="test", sample_paths=sample_paths)

        assert result.samples == sample_count

    @given(
        name=st.text(
            min_size=1, max_size=50, alphabet=st.characters(blacklist_characters="\x00")
        ),
        sample_count=st.integers(min_value=1, max_value=5),
    )
    def test_create_profile_calls_repository_save(
        self, mock_audio_processor, mock_repository, name, sample_count
    ):
        """Property: Creating profile should always call repository.save()."""
        use_case = CreateVoiceProfileUseCase(
            audio_processor=mock_audio_processor, profile_repository=mock_repository
        )

        sample_paths = [Path(f"sample_{i}.wav") for i in range(sample_count)]

        use_case.execute(name=name, sample_paths=sample_paths)

        # Should have called save exactly once
        assert mock_repository.save.call_count == 1


class TestGenerateAudioProperties:
    """Property-based tests for GenerateAudioUseCase."""

    @pytest.fixture
    def mock_tts_engine(self):
        """Create a mock TTS engine."""
        engine = Mock(spec=TTSEngine)
        engine.generate_audio.return_value = Path("output.wav")
        return engine

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository."""
        repository = Mock(spec=ProfileRepository)
        profile = VoiceProfile(
            id="test-id",
            name="test",
            samples=[],
            created_at="2024-01-01T00:00:00",
            total_duration=10.0,
            language="es",
        )
        repository.find_by_name.return_value = profile
        return repository

    @given(
        text=st.text(
            min_size=1,
            max_size=500,
            alphabet=st.characters(blacklist_categories=("Cc", "Cs")),
        ),
        temperature=st.floats(min_value=0.5, max_value=1.0),
        speed=st.floats(min_value=0.8, max_value=1.2),
    )
    def test_generate_audio_with_valid_parameters(
        self, mock_tts_engine, mock_repository, text, temperature, speed
    ):
        """Property: Generate audio should succeed with valid parameters."""
        use_case = GenerateAudioUseCase(
            tts_engine=mock_tts_engine, profile_repository=mock_repository
        )

        result = use_case.execute(
            profile_name="test", text=text, temperature=temperature, speed=speed
        )

        assert result.audio_path == Path("output.wav")
        assert result.text == text

    @given(
        text=st.text(
            min_size=1,
            max_size=500,
            alphabet=st.characters(blacklist_categories=("Cc", "Cs")),
        )
    )
    def test_generate_audio_calls_engine_once(
        self, mock_tts_engine, mock_repository, text
    ):
        """Property: Generate audio should call TTS engine exactly once."""
        use_case = GenerateAudioUseCase(
            tts_engine=mock_tts_engine, profile_repository=mock_repository
        )

        use_case.execute(profile_name="test", text=text, temperature=0.75, speed=1.0)

        # Should have called generate_audio exactly once
        assert mock_tts_engine.generate_audio.call_count == 1

    @given(
        text=st.text(
            min_size=1,
            max_size=500,
            alphabet=st.characters(blacklist_categories=("Cc", "Cs")),
        )
    )
    def test_generate_audio_loads_profile_once(
        self, mock_tts_engine, mock_repository, text
    ):
        """Property: Generate audio should load profile exactly once."""
        use_case = GenerateAudioUseCase(
            tts_engine=mock_tts_engine, profile_repository=mock_repository
        )

        use_case.execute(profile_name="test", text=text, temperature=0.75, speed=1.0)

        # Should have called find_by_name exactly once
        assert mock_repository.find_by_name.call_count == 1


class TestListVoiceProfilesProperties:
    """Property-based tests for ListVoiceProfilesUseCase."""

    @given(profile_count=st.integers(min_value=0, max_value=20))
    def test_list_profiles_count_matches(self, profile_count):
        """Property: Listed profiles count should match repository count."""
        # Create mock repository with profiles
        repository = Mock(spec=ProfileRepository)
        profiles = []
        for i in range(profile_count):
            profile = VoiceProfile(
                id=f"test-id-{i}",
                name=f"test-{i}",
                samples=[],
                created_at="2024-01-01T00:00:00",
                total_duration=10.0,
                language="es",
            )
            profiles.append(profile)

        repository.list_all.return_value = profiles

        use_case = ListVoiceProfilesUseCase(profile_repository=repository)

        result = use_case.execute()

        assert len(result) == profile_count

    @given(profile_count=st.integers(min_value=1, max_value=10))
    def test_list_profiles_preserves_names(self, profile_count):
        """Property: Listed profiles should preserve all names."""
        repository = Mock(spec=ProfileRepository)
        profiles = []
        expected_names = []

        for i in range(profile_count):
            name = f"test-{i}"
            expected_names.append(name)
            profile = VoiceProfile(
                id=f"test-id-{i}",
                name=name,
                samples=[],
                created_at="2024-01-01T00:00:00",
                total_duration=10.0,
                language="es",
            )
            profiles.append(profile)

        repository.list_all.return_value = profiles

        use_case = ListVoiceProfilesUseCase(profile_repository=repository)

        result = use_case.execute()

        result_names = [dto.name for dto in result]
        assert result_names == expected_names


class TestUseCaseIdempotency:
    """Test idempotent operations in use cases."""

    @given(
        name=st.text(
            min_size=1, max_size=50, alphabet=st.characters(blacklist_characters="\x00")
        )
    )
    def test_list_profiles_is_idempotent(self, name):
        """Property: Listing profiles multiple times should return same result."""
        repository = Mock(spec=ProfileRepository)
        profile = VoiceProfile(
            id="test-id",
            name=name,
            samples=[],
            created_at="2024-01-01T00:00:00",
            total_duration=10.0,
            language="es",
        )
        repository.list_all.return_value = [profile]

        use_case = ListVoiceProfilesUseCase(profile_repository=repository)

        # Call multiple times
        result1 = use_case.execute()
        result2 = use_case.execute()
        result3 = use_case.execute()

        # Results should be identical
        assert len(result1) == len(result2) == len(result3)
        assert result1[0].name == result2[0].name == result3[0].name


class TestUseCaseErrorHandling:
    """Test error handling properties in use cases."""

    @given(
        text=st.text(
            min_size=1,
            max_size=500,
            alphabet=st.characters(blacklist_categories=("Cc", "Cs")),
        )
    )
    def test_generate_audio_with_nonexistent_profile_raises_error(self, text):
        """Property: Generating with nonexistent profile should raise error."""
        engine = Mock(spec=TTSEngine)
        repository = Mock(spec=ProfileRepository)
        repository.find_by_name.return_value = None  # Profile not found

        use_case = GenerateAudioUseCase(
            tts_engine=engine, profile_repository=repository
        )

        with pytest.raises((ValueError, KeyError, AttributeError)):
            use_case.execute(
                profile_name="nonexistent", text=text, temperature=0.75, speed=1.0
            )

    @given(sample_count=st.integers(min_value=1, max_value=5))
    def test_create_profile_with_invalid_samples_raises_error(self, sample_count):
        """Property: Creating profile with invalid samples should raise error."""
        processor = Mock(spec=AudioProcessor)
        processor.validate_sample.return_value = False  # All samples invalid

        repository = Mock(spec=ProfileRepository)

        use_case = CreateVoiceProfileUseCase(
            audio_processor=processor, profile_repository=repository
        )

        sample_paths = [Path(f"sample_{i}.wav") for i in range(sample_count)]

        with pytest.raises((ValueError, InvalidSampleException)):
            use_case.execute(name="test", sample_paths=sample_paths)


class TestParameterBoundaries:
    """Test parameter boundary conditions."""

    @pytest.fixture
    def mock_tts_engine(self):
        """Create a mock TTS engine."""
        engine = Mock(spec=TTSEngine)
        engine.generate_audio.return_value = Path("output.wav")
        return engine

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository."""
        repository = Mock(spec=ProfileRepository)
        profile = VoiceProfile(
            id="test-id",
            name="test",
            samples=[],
            created_at="2024-01-01T00:00:00",
            total_duration=10.0,
            language="es",
        )
        repository.find_by_name.return_value = profile
        return repository

    @given(temperature=st.floats(min_value=0.5, max_value=1.0))
    def test_temperature_within_valid_range(
        self, mock_tts_engine, mock_repository, temperature
    ):
        """Property: Temperature within 0.5-1.0 should be accepted."""
        use_case = GenerateAudioUseCase(
            tts_engine=mock_tts_engine, profile_repository=mock_repository
        )

        result = use_case.execute(
            profile_name="test", text="test", temperature=temperature, speed=1.0
        )

        assert result.audio_path == Path("output.wav")

    @given(speed=st.floats(min_value=0.8, max_value=1.2))
    def test_speed_within_valid_range(self, mock_tts_engine, mock_repository, speed):
        """Property: Speed within 0.8-1.2 should be accepted."""
        use_case = GenerateAudioUseCase(
            tts_engine=mock_tts_engine, profile_repository=mock_repository
        )

        result = use_case.execute(
            profile_name="test", text="test", temperature=0.75, speed=speed
        )

        assert result.audio_path == Path("output.wav")
