import torch
import logging
import sys
import numpy as np
import tempfile
from pathlib import Path
from qwen_asr import Qwen3ASRModel
from typing import Optional, Union
import soundfile as sf

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


class QwenASRPipeline:
    """
    ASR Pipeline for Qwen3-ASR-0.6B model.
    
    This class provides a simple interface for automatic speech recognition
    using the Qwen3-ASR-0.6B model from Hugging Face.
    """
    
    def __init__(
        self,
        model_name: str = "Qwen/Qwen3-ASR-0.6B",
        device: Optional[str] = None,
        max_inference_batch_size: int = 32,
        max_new_tokens: int = 256
    ):
        """
        Initialize the ASR pipeline.
        
        Args:
            model_name: Hugging Face model identifier
            device: Device to run inference on ('cuda:0' or 'cpu'). Auto-detected if None.
            max_inference_batch_size: Maximum batch size for inference
            max_new_tokens: Maximum number of tokens to generate
        """
        self.model_name = model_name
        
        if device is None:
            if torch.cuda.is_available():
                self.device = "cuda:0"
            else:
                self.device = "cpu"
        else:
            self.device = device
            
        logger.info(f"Initializing QwenASRPipeline on device: {self.device}")
        
        if "cuda" in self.device and torch.cuda.is_available():
            logger.info(f"GPU Device: {torch.cuda.get_device_name(0)}")
            logger.info(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        
        try:
            logger.info(f"Loading model: {self.model_name}")
            
            dtype = torch.bfloat16 if "cuda" in self.device else torch.float32
            
            self.model = Qwen3ASRModel.from_pretrained(
                model_name,
                dtype=dtype,
                device_map=self.device,
                max_inference_batch_size=max_inference_batch_size,
                max_new_tokens=max_new_tokens,
            )
            
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
    
    def transcribe(
        self,
        audio_path: Union[str, Path],
        language: Optional[str] = None
    ) -> str:
        """
        Transcribe audio file to text.
        
        Args:
            audio_path: Path to audio file or URL
            language: Optional language hint (e.g., "English", "Chinese"). 
                     If None, language will be auto-detected.
            
        Returns:
            Transcribed text
        """
        audio_path = Path(audio_path) if not str(audio_path).startswith("http") else str(audio_path)
        
        if isinstance(audio_path, Path) and not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        logger.info(f"Transcribing audio from: {audio_path}")
        
        try:
            results = self.model.transcribe(
                audio=str(audio_path),
                language=language,
            )
            
            transcription = results[0].text
            detected_language = results[0].language
            
            logger.info(f"Detected language: {detected_language}")
            logger.info(f"Transcription complete: {len(transcription)} characters")
            
            return transcription
            
        except FileNotFoundError as e:
            logger.error(str(e))
            raise
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise
    
    def transcribe_numpy(
        self,
        audio_array: np.ndarray,
        sampling_rate: int,
        language: Optional[str] = None
    ) -> str:
        """
        Transcribe audio from numpy array to text.
        
        Args:
            audio_array: Numpy array containing audio data (1D float array)
            sampling_rate: Sampling rate of the audio
            language: Optional language hint (e.g., "English", "Chinese"). 
                     If None, language will be auto-detected.
            
        Returns:
            Transcribed text
        """
        logger.info(f"Transcribing audio from numpy array: shape={audio_array.shape}, sr={sampling_rate}")
        
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                temp_path = temp_audio.name
                sf.write(temp_path, audio_array, sampling_rate)
                logger.debug(f"Temporary audio file created: {temp_path}")
            
            try:
                results = self.model.transcribe(
                    audio=temp_path,
                    language=language,
                )
                
                transcription = results[0].text
                detected_language = results[0].language
                
                logger.info(f"Detected language: {detected_language}")
                logger.info(f"Transcription complete: {len(transcription)} characters")
                
                return transcription
                
            finally:
                Path(temp_path).unlink(missing_ok=True)
                logger.debug(f"Temporary file cleaned up: {temp_path}")
            
        except Exception as e:
            logger.error(f"Transcription from numpy array failed: {str(e)}")
            raise
    
    def transcribe_numpy(
        self,
        audio_array: np.ndarray,
        sampling_rate: int,
        language: Optional[str] = None
    ) -> str:
        """
        Transcribe audio from numpy array (in-memory processing).
        
        Args:
            audio_array: Audio data as numpy array (mono, float32 or int16)
            sampling_rate: Sample rate of the audio data
            language: Optional language hint (e.g., "English", "Chinese").
                     If None, language will be auto-detected.
            
        Returns:
            Transcribed text
        """
        logger.info(f"Transcribing audio from memory (shape: {audio_array.shape}, sr: {sampling_rate}Hz)")
        
        try:
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                tmp_path = tmp_file.name
                
            if audio_array.dtype == np.int16:
                audio_array = audio_array.astype(np.float32) / 32768.0
            
            sf.write(tmp_path, audio_array, sampling_rate)
            
            try:
                results = self.model.transcribe(
                    audio=tmp_path,
                    language=language,
                )
                
                transcription = results[0].text
                detected_language = results[0].language
                
                logger.info(f"Detected language: {detected_language}")
                logger.info(f"Transcription complete: {len(transcription)} characters")
                
                return transcription
                
            finally:
                Path(tmp_path).unlink(missing_ok=True)
            
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise