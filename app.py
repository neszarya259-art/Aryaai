"""
AryaAI - Website AI Paling Canggih & Keren
Full-Stack Advanced AI Platform dengan Python
Semua fitur AI terbaru dalam satu aplikasi!
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
import os
import json
import asyncio
from dotenv import load_dotenv
import openai
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from datetime import datetime
import aiofiles
import io
from pathlib import Path

load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="AryaAI - Website AI Paling Canggih",
    description="Platform AI Terdepan dengan Teknologi Terbaru",
    version="2.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI Configuration
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-your-key-here")

# ==================== DATABASE SIMULATION ====================
database = {
    "users": [],
    "conversations": [],
    "generated_images": [],
    "history": []
}

# ==================== MODELS ====================
class TextRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 1000
    style: str = "normal"

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    user_id: Optional[str] = None

class ImageRequest(BaseModel):
    prompt: str
    size: str = "1024x1024"
    n: int = 1
    style: str = "realistic"

class CodeRequest(BaseModel):
    description: str
    language: str = "python"
    complexity: str = "medium"

class AudioRequest(BaseModel):
    text: str
    voice: str = "alloy"
    speed: float = 1.0

class TranslateRequest(BaseModel):
    text: str
    target_language: str = "id"

class SEORequest(BaseModel):
    content: str
    keywords: List[str]

class UserProfile(BaseModel):
    name: str
    email: str
    api_key: Optional[str] = None

# ==================== ROUTES ====================

@app.get("/")
async def root():
    """Root endpoint dengan informasi lengkap"""
    return {
        "status": "🚀 RUNNING",
        "name": "AryaAI - Website AI Paling Canggih & Keren",
        "version": "2.0.0",
        "author": "neszarya259-art",
        "features": [
            "✨ Text Generation Advanced",
            "💬 Chat AI Real-time",
            "🖼️ Image Generation (DALL-E)",
            "💻 Code Generation",
            "🎤 Voice Synthesis",
            "🌍 Translation",
            "📊 SEO Optimization",
            "🔍 Text Analysis",
            "📈 Data Insights",
            "⚡ Streaming Response"
        ],
        "api_endpoints": {
            "dashboard": "/dashboard",
            "ai": {
                "text": "/api/ai/text",
                "chat": "/api/ai/chat",
                "image": "/api/ai/image",
                "code": "/api/ai/code",
                "voice": "/api/ai/voice",
                "translate": "/api/ai/translate",
                "seo": "/api/ai/seo",
                "analyze": "/api/ai/analyze"
            },
            "user": {
                "profile": "/api/user/profile",
                "history": "/api/user/history",
                "conversations": "/api/user/conversations"
            }
        },
        "docs": "/docs",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "✅ Healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "stable"
    }

# ==================== TEXT GENERATION ====================

@app.post("/api/ai/text")
async def generate_text(request: TextRequest):
    """Generate teks dengan berbagai style"""
    try:
        style_prompts = {
            "creative": "Be creative and imaginative",
            "formal": "Write in formal professional tone",
            "casual": "Write in casual friendly tone",
            "technical": "Write in technical detailed tone",
            "poetic": "Write in poetic artistic style"
        }
        
        system_message = style_prompts.get(request.style, "Be helpful")
        
        response = openai.ChatCompletion.create(
            model=request.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": request.prompt}
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        result = response.choices[0].message['content']
        
        # Save to history
        database["history"].append({
            "type": "text_generation",
            "prompt": request.prompt,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "status": "✅ Success",
            "prompt": request.prompt,
            "response": result,
            "style": request.style,
            "model": request.model,
            "tokens": response.usage.total_tokens,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== CHAT AI ====================

@app.post("/api/ai/chat")
async def chat_with_ai(request: ChatRequest):
    """Advanced chat dengan konteks dan history"""
    try:
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]
        
        response = openai.ChatCompletion.create(
            model=request.model,
            messages=messages,
            temperature=request.temperature,
            stream=False
        )
        
        ai_response = response.choices[0].message['content']
        
        # Save conversation
        if request.user_id:
            database["conversations"].append({
                "user_id": request.user_id,
                "messages": messages,
                "response": ai_response,
                "timestamp": datetime.now().isoformat()
            })
        
        return {
            "status": "✅ Success",
            "response": ai_response,
            "model": request.model,
            "tokens": response.usage.total_tokens,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== IMAGE GENERATION ====================

@app.post("/api/ai/image")
async def generate_image(request: ImageRequest):
    """Generate gambar dengan DALL-E"""
    try:
        style_modifiers = {
            "realistic": "photorealistic, 8k, high quality",
            "artistic": "artistic painting, oil painting style",
            "cartoon": "cartoon style, colorful",
            "3d": "3D render, 3D modeling",
            "cyberpunk": "cyberpunk style, neon colors"
        }
        
        enhanced_prompt = f"{request.prompt}, {style_modifiers.get(request.style, '')}"
        
        response = openai.Image.create(
            prompt=enhanced_prompt,
            n=request.n,
            size=request.size
        )
        
        images = response['data']
        
        # Save to database
        database["generated_images"].append({
            "prompt": request.prompt,
            "style": request.style,
            "size": request.size,
            "images": images,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "status": "✅ Success",
            "prompt": request.prompt,
            "style": request.style,
            "images": images,
            "count": len(images),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== CODE GENERATION ====================

@app.post("/api/ai/code")
async def generate_code(request: CodeRequest):
    """Generate kode dengan berbagai bahasa"""
    try:
        complexity_levels = {
            "easy": "Buat kode yang sederhana dan mudah dipahami",
            "medium": "Buat kode yang moderate dengan best practices",
            "advanced": "Buat kode yang advanced dengan optimasi dan design patterns"
        }
        
        prompt = f"""
        Generate {request.language} code untuk: {request.description}
        Complexity: {complexity_levels.get(request.complexity, 'medium')}
        Include comments dalam bahasa Indonesia.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are expert {request.language} developer"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        code = response.choices[0].message['content']
        
        return {
            "status": "✅ Success",
            "description": request.description,
            "language": request.language,
            "complexity": request.complexity,
            "code": code,
            "tokens": response.usage.total_tokens,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== VOICE SYNTHESIS ====================

@app.post("/api/ai/voice")
async def text_to_speech(request: AudioRequest):
    """Text to Speech synthesis"""
    try:
        response = openai.Audio.create(
            model="tts-1",
            voice=request.voice,
            input=request.text,
            speed=request.speed
        )
        
        # Return audio sebagai stream
        audio_data = response.content if hasattr(response, 'content') else b''
        
        return {
            "status": "✅ Success",
            "text": request.text,
            "voice": request.voice,
            "speed": request.speed,
            "message": "Audio berhasil dibuat",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== TRANSLATION ====================

@app.post("/api/ai/translate")
async def translate_text(request: TranslateRequest):
    """Translate teks ke bahasa lain"""
    try:
        prompt = f"Translate this text to {request.target_language}:\n{request.text}"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional translator"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        translated = response.choices[0].message['content']
        
        return {
            "status": "✅ Success",
            "original": request.text,
            "translated": translated,
            "target_language": request.target_language,
            "tokens": response.usage.total_tokens,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== SEO OPTIMIZATION ====================

@app.post("/api/ai/seo")
async def optimize_seo(request: SEORequest):
    """Optimize content untuk SEO"""
    try:
        keywords_str = ", ".join(request.keywords)
        prompt = f"""
        Analyze this content for SEO and provide optimization suggestions:
        Content: {request.content}
        Target Keywords: {keywords_str}
        
        Provide:
        1. SEO Score (1-100)
        2. Keyword density analysis
        3. Optimization suggestions
        4. Meta description
        5. Meta title
        6. Internal linking suggestions
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an SEO expert"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1500
        )
        
        analysis = response.choices[0].message['content']
        
        return {
            "status": "✅ Success",
            "keywords": request.keywords,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== TEXT ANALYSIS ====================

@app.post("/api/ai/analyze")
async def analyze_text(text: str):
    """Advanced text analysis"""
    try:
        prompt = f"""
        Analyze this text comprehensively:
        {text}
        
        Provide in JSON format:
        - sentiment: positive/negative/neutral
        - emotion: list of detected emotions
        - topics: main topics
        - summary: brief summary
        - keywords: important keywords
        - readability: readability score
        - tone: tone of the text
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert text analyst. Always respond in valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        analysis_text = response.choices[0].message['content']
        
        try:
            analysis = json.loads(analysis_text)
        except:
            analysis = {"raw_analysis": analysis_text}
        
        return {
            "status": "✅ Success",
            "text": text[:100] + "...",
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== USER PROFILE ====================

@app.post("/api/user/profile")
async def create_user_profile(profile: UserProfile):
    """Create user profile"""
    try:
        user_data = {
            "id": len(database["users"]) + 1,
            "name": profile.name,
            "email": profile.email,
            "created_at": datetime.now().isoformat(),
            "usage": 0
        }
        
        database["users"].append(user_data)
        
        return {
            "status": "✅ Success",
            "user": user_data,
            "message": "Profile berhasil dibuat"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/history")
async def get_user_history(user_id: str = None):
    """Get user activity history"""
    return {
        "status": "✅ Success",
        "history": database["history"][-10:],
        "total": len(database["history"])
    }

@app.get("/api/user/conversations")
async def get_conversations(user_id: str = None):
    """Get saved conversations"""
    return {
        "status": "✅ Success",
        "conversations": database["conversations"][-5:],
        "total": len(database["conversations"])
    }

# ==================== DASHBOARD ====================

@app.get("/dashboard")
async def dashboard():
    """Dashboard dengan statistik"""
    return {
        "status": "✅ Success",
        "stats": {
            "total_users": len(database["users"]),
            "total_conversations": len(database["conversations"]),
            "total_images_generated": len(database["generated_images"]),
            "total_requests": len(database["history"])
        },
        "recent_activity": database["history"][-5:],
        "timestamp": datetime.now().isoformat()
    }

# ==================== FILE UPLOAD ====================

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload dan analyze file"""
    try:
        os.makedirs("uploads", exist_ok=True)
        
        file_path = f"uploads/{file.filename}"
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        return {
            "status": "✅ Success",
            "filename": file.filename,
            "size": len(content),
            "path": file_path,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== BATCH PROCESSING ====================

@app.post("/api/batch/process")
async def batch_process(prompts: List[str]):
    """Process multiple prompts sekaligus"""
    try:
        results = []
        
        for prompt in prompts:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            results.append({
                "prompt": prompt,
                "response": response.choices[0].message['content']
            })
        
        return {
            "status": "✅ Success",
            "total_processed": len(results),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ADVANCED FEATURES ====================

@app.get("/api/models")
async def get_available_models():
    """Get list of available AI models"""
    return {
        "status": "✅ Success",
        "models": {
            "text": ["gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"],
            "image": ["dall-e-3", "dall-e-2"],
            "voice": ["tts-1", "tts-1-hd"],
            "embedding": ["text-embedding-3-large", "text-embedding-3-small"]
        },
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/ai/summary")
async def summarize_text(text: str, style: str = "concise"):
    """Summarize long text"""
    try:
        style_prompts = {
            "concise": "Buat summary yang sangat singkat (1-2 kalimat)",
            "detailed": "Buat summary yang detail (3-4 paragraf)",
            "bullet_points": "Buat summary dalam bentuk bullet points"
        }
        
        prompt = f"{style_prompts.get(style, 'Buat summary')}\n\nText:\n{text}"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert summarizer"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.5
        )
        
        summary = response.choices[0].message['content']
        
        return {
            "status": "✅ Success",
            "original_length": len(text),
            "summary": summary,
            "style": style,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== MAIN ====================

if __name__ == "__main__":
    print("""
    
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║          🚀 AryaAI - Website AI Paling Canggih 🚀        ║
    ║                                                           ║
    ║    Platform AI Terdepan dengan Teknologi Terbaru         ║
    ║                                                           ║
    ║    ✨ Akses: http://localhost:8000                       ║
    ║    📚 Docs: http://localhost:8000/docs                   ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
