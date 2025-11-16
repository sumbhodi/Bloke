"""Bloke - Local LLM Chat on Android"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.core.window import Window

try:
    from llama_wrapper import Llama
    print("✅ Using llama_wrapper")
except ImportError:
    print("❌ llama_wrapper not found")
    Llama = None


class BlokeApp(App):
    def build(self):
        self.title = "Bloke"
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Chat history
        self.chat_scroll = ScrollView(size_hint=(1, 0.8))
        self.chat_history = Label(
            text="Bloke v0.1 - Local LLM Chat\n\n",
            size_hint_y=None,
            markup=True,
            halign='left',
            valign='top'
        )
        self.chat_history.bind(texture_size=self.chat_history.setter('size'))
        self.chat_scroll.add_widget(self.chat_history)
        layout.add_widget(self.chat_scroll)
        
        # Input area
        input_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        
        self.user_input = TextInput(
            hint_text='Type your message...',
            multiline=False,
            size_hint=(0.8, 1)
        )
        self.user_input.bind(on_text_validate=self.send_message)
        
        send_btn = Button(text='Send', size_hint=(0.2, 1))
        send_btn.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.user_input)
        input_layout.add_widget(send_btn)
        layout.add_widget(input_layout)
        
        # Initialize model (placeholder)
        self.model = None
        self.init_model()
        
        return layout
    
    def init_model(self):
        """Initialize the LLM (placeholder for now)"""
        if Llama:
            try:
                self.model = Llama()
                self.add_message("System", "Model loaded successfully!")
            except Exception as e:
                self.add_message("Error", f"Failed to load model: {e}")
        else:
            self.add_message("System", "llama_wrapper not available. Install a model to get started.")
    
    def send_message(self, *args):
        """Handle sending a message"""
        user_text = self.user_input.text.strip()
        if not user_text:
            return
        
        # Add user message
        self.add_message("You", user_text)
        self.user_input.text = ""
        
        # Generate response (placeholder)
        if self.model:
            try:
                response = self.model.generate(user_text)
                self.add_message("Bloke", response)
            except Exception as e:
                self.add_message("Error", str(e))
        else:
            self.add_message("Bloke", "Model not loaded. Please load a GGUF model first.")
    
    def add_message(self, sender, text):
        """Add a message to chat history"""
        self.chat_history.text += f"[b]{sender}:[/b] {text}\n\n"
        self.chat_scroll.scroll_y = 0  # Scroll to bottom


if __name__ == '__main__':
    BlokeApp().run()
