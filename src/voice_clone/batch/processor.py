"""Batch processing for script-based audio generation."""

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from voice_clone.audio.processor import AudioProcessor
from voice_clone.model.generator import VoiceGenerator
from voice_clone.model.profile import VoiceProfile
from voice_clone.model.qwen3_generator import Qwen3Generator
from voice_clone.utils.logger import logger


@dataclass
class ScriptSegment:
    """Represents a segment from a script file."""

    marker: str
    text: str
    output_filename: str


class BatchProcessor:
    """Processes script files with multiple segments."""

    def __init__(
        self,
        voice_generator: VoiceGenerator | Qwen3Generator,
        audio_processor: AudioProcessor,
    ):
        """Initialize BatchProcessor.

        Args:
            voice_generator: VoiceGenerator or Qwen3Generator instance
            audio_processor: AudioProcessor instance
        """
        self.voice_generator = voice_generator
        self.audio_processor = audio_processor

    def _parse_script(self, script_path: Path | str) -> list[ScriptSegment]:
        """Parse script file and extract segments.

        Script format:
        [MARKER_NAME]
        Text content here...

        [ANOTHER_MARKER]
        More text...

        Args:
            script_path: Path to script file

        Returns:
            List of ScriptSegment objects
        """
        script_path = Path(script_path)
        segments = []

        with open(script_path) as f:
            content = f.read()

        # Split by markers [MARKER_NAME]
        pattern = r"\[([A-Z_0-9]+)\]\s*\n(.*?)(?=\n\[|$)"
        matches = re.findall(pattern, content, re.DOTALL)

        for marker, text in matches:
            text = text.strip()
            if not text:
                continue

            # Generate output filename from marker
            output_filename = marker.lower() + ".wav"

            segment = ScriptSegment(
                marker=marker, text=text, output_filename=output_filename
            )
            segments.append(segment)

        return segments

    def _create_manifest(
        self,
        segments: list[ScriptSegment],
        output_dir: Path,
        results: dict[str, Any],
    ) -> None:
        """Create manifest.json with metadata.

        Args:
            segments: List of processed segments
            output_dir: Output directory
            results: Processing results
        """
        manifest = {
            "created_at": datetime.now().isoformat(),
            "total_segments": len(segments),
            "successful": results["successful"],
            "failed": results["failed"],
            "segments": [],
        }

        for segment in segments:
            output_path = output_dir / segment.output_filename
            duration = 0.0

            if output_path.exists():
                try:
                    import soundfile as sf

                    info = sf.info(output_path)
                    duration = info.duration
                except Exception:
                    pass

            manifest["segments"].append(
                {
                    "marker": segment.marker,
                    "filename": segment.output_filename,
                    "duration": duration,
                    "text_length": len(segment.text),
                }
            )

        manifest_path = output_dir / "manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        logger.info(f"✓ Manifest saved to: {manifest_path}")

    def process_script(
        self,
        script_path: Path | str,
        voice_profile: VoiceProfile,
        output_dir: Path | str,
    ) -> dict[str, Any]:
        """Process script file and generate audio for all segments.

        Keeps model loaded between segments for efficiency.
        Continues processing even if individual segments fail.

        Args:
            script_path: Path to script file
            voice_profile: Voice profile to use
            output_dir: Directory to save output files

        Returns:
            Dictionary with processing results
        """
        script_path = Path(script_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Parse script
        logger.info(f"Parsing script: {script_path}")
        segments = self._parse_script(script_path)
        logger.info(f"Found {len(segments)} segments")

        if not segments:
            logger.error("No segments found in script")
            return {"successful": 0, "failed": 0, "segments": []}

        # Process each segment
        results: dict[str, Any] = {
            "successful": 0,
            "failed": 0,
            "segments": [],
        }

        for i, segment in enumerate(segments, 1):
            logger.info(f"\n[{i}/{len(segments)}] Processing: {segment.marker}")
            output_path = output_dir / segment.output_filename

            try:
                # Generate audio
                # TODO: Update to support Qwen3Generator interface
                success = self.voice_generator.generate(  # type: ignore[call-arg]
                    text=segment.text,
                    voice_profile=voice_profile,
                    output_path=output_path,
                )

                if success:
                    results["successful"] += 1
                    results["segments"].append(
                        {"marker": segment.marker, "status": "success"}
                    )
                    logger.info(f"✓ Generated: {output_path}")
                else:
                    results["failed"] += 1
                    results["segments"].append(
                        {"marker": segment.marker, "status": "failed"}
                    )
                    logger.error(f"✗ Failed: {segment.marker}")

            except Exception as e:
                results["failed"] += 1
                results["segments"].append(
                    {"marker": segment.marker, "status": "error", "error": str(e)}
                )
                logger.error(f"✗ Error processing {segment.marker}: {str(e)}")
                # Continue with next segment

        # Create manifest
        self._create_manifest(segments, output_dir, results)

        # Summary
        logger.info(f"\n{'='*60}")
        logger.info("Batch processing complete:")
        logger.info(f"  ✓ Successful: {results['successful']}")
        logger.info(f"  ✗ Failed: {results['failed']}")
        logger.info(f"  Total: {len(segments)}")
        logger.info(f"{'='*60}")

        return results
