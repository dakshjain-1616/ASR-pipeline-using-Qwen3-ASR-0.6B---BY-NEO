import torch
import logging
import sys
from pathlib import Path
from qwen_asr import Qwen3ASRModel
from typing import Optional, Union

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