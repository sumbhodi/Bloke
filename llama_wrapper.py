"""Minimal llama.cpp wrapper using ctypes"""
import ctypes
from pathlib import Path

class Llama:
    """Minimal wrapper for llama.cpp"""
    
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.lib = None
        self._load_library()
    
    def _load_library(self):
        """Try to load libllama.so"""
        lib_paths = [
            Path("/data/app/org.bloke.app/lib/arm64"),
            Path("/data/data/org.bloke.app/lib"),
            Path(__file__).parent / "lib" / "arm64-v8a",
        ]
        
        for lib_dir in lib_paths:
            lib_file = lib_dir / "libllama.so"
            if lib_file.exists():
                try:
                    self.lib = ctypes.CDLL(str(lib_file))
                    print(f"✅ Loaded libllama.so from {lib_dir}")
                    return
                except Exception as e:
                    print(f"❌ Failed to load from {lib_dir}: {e}")
        
        print("⚠️ libllama.so not found - running in stub mode")
    
    def generate(self, prompt, max_tokens=100):
        """Generate text (placeholder for now)"""
        if not self.lib:
            return "Model not loaded. Please ensure .so files are packaged correctly."
        
        # TODO: Implement actual llama.cpp C API calls
        return f"Echo: {prompt}\n\n(Actual inference coming soon - .so files are loaded!)"
